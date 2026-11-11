"""逐字比對證據卡引用的英文原文，確認真的出現在論文PDF裡。

用法：python3 scripts/check_quotes.py [--root 路徑]
需要pdftotext（poppler-utils）。PDF放在raw/<文獻id>.pdf，不上傳，所以只有手上有PDF的人能跑；
沒有PDF的文獻會列出「無法比對」，不算通過也不算失敗。
比對前會把換行、連字號斷行、引號和空白統一，其他字必須完全一樣。
掃描檔（PDF裡沒有文字）會改用OCR（需要pdftoppm和tesseract）。OCR會認錯字，所以只能做
近似比對：在OCR文字裡找最像的一段，相似度 >= 0.9 列為「OCR近似」，跟逐字找到的分開計算；
低於0.9算找不到。OCR近似的引用，仍然要有人對照PDF頁面圖片確認。
"""
import argparse
import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import parse  # noqa: E402


def normalize(text):
    text = text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-").replace("−", "-")
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


OCR_MIN = 0.9


def pdf_text(pdf):
    """回傳 (文字, 是否OCR)。"""
    raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                         text=True, encoding="utf-8", errors="replace").stdout
    if len(raw.strip()) >= 500:
        return normalize(raw), False
    if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
        return "", True
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "300", "-gray", str(pdf), f"{d}/p"], check=True)
        parts = []
        for img in sorted(Path(d).glob("p-*.pgm"), key=lambda x: int(x.stem.split("-")[1])):
            parts.append(subprocess.run(["tesseract", str(img), "-", "-l", "eng"], capture_output=True,
                                        text=True, encoding="utf-8", errors="replace").stdout)
    return normalize("\n".join(parts)), True


def best_ratio(q, text):
    words, qn = text.split(" "), len(q.split(" "))
    best = 0.0
    for i in range(0, max(1, len(words) - qn + 1)):
        for span in (qn - 1, qn, qn + 1):
            cand = " ".join(words[i:i + span])
            r = difflib.SequenceMatcher(None, q.lower(), cand.lower()).ratio()
            best = max(best, r)
    return best


def quotes(body):
    out, cur = [], []
    for line in body.splitlines() + [""]:
        if line.startswith(">"):
            cur.append(line[1:].strip())
        elif cur:
            out.append(" ".join(cur))
            cur = []
    return [q for q in out if q]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    root = Path(ap.parse_args().root).resolve()
    if not shutil.which("pdftotext"):
        print("[錯誤] 找不到pdftotext，沒辦法比對")
        return 1
    texts, ok, near, bad, skipped = {}, 0, 0, 0, 0
    for card in sorted((root / "wiki" / "cards").glob("*.md")):
        if card.name == "_template.md":
            continue
        meta, body = parse(card)
        if not meta:
            continue
        src = meta.get("source", "")
        for q in quotes(body):
            pdf = root / "raw" / f"{src}.pdf"
            if not pdf.is_file():
                print(f"[無法比對] {card.name}：raw/{src}.pdf 不在這台電腦上")
                skipped += 1
                continue
            if src not in texts:
                texts[src] = pdf_text(pdf)
            text, ocr = texts[src]
            if not text:
                print(f"[無法比對] {card.name}：{src}是掃描檔，這台電腦沒有OCR工具")
                skipped += 1
            elif normalize(q) in text:
                ok += 1
            elif ocr and (r := best_ratio(normalize(q), text)) >= OCR_MIN:
                print(f"[OCR近似] {card.name}：相似度 {r:.2f}，要對照PDF頁面確認：{q}")
                near += 1
            else:
                print(f"[錯誤] {card.name}：PDF裡找不到這段引用：{q}")
                bad += 1
    print(f"\n引用 {ok + near + bad + skipped} 段：逐字找到 {ok}，OCR近似 {near}，"
          f"找不到 {bad}，無法比對 {skipped}。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
