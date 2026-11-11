"""逐字比對證據卡引用的英文原文，確認真的出現在論文PDF裡。

用法：python3 scripts/check_quotes.py [--root 路徑]
需要pdftotext（poppler-utils）。PDF放在raw/<文獻id>.pdf，不上傳，所以只有手上有PDF的人能跑；
沒有PDF的文獻會列出「無法比對」，不算通過也不算失敗。
比對前會把換行、連字號斷行、引號、空白和排版合字（ﬁ、ﬂ等）統一，其他字必須完全一樣。
比對順序：
1. 先在PDF的文字層逐字找，找到就是「逐字找到」。
2. 找不到時才做OCR（需要pdftoppm和tesseract），並用「三個連續英文字」的重疊比例判斷文字層可不可靠
   （OCR文字裡的三字組有多少也出現在文字層）。重疊 >= 0.8 代表文字層可靠，引用找不到就是錯誤。
   這個門檻是先量了Sugiyama 2008（0.96）、Tadaki 2013（0.96）、NaSch 1992（0.39，字序被打亂）、
   Bando 1995（0.00，掃描檔）四份PDF的文字層品質才定的，那時新卡片還沒拿去比對。
3. 文字層不可靠時，在OCR文字裡逐字找，找到是「OCR逐字」；找不到再做近似比對：相似度 >= 0.9、
   而且引用裡的數字、否定詞（not、no、never、without等）和un開頭的字（例如unstable）都跟找到的
   那段完全相同，才算「OCR近似」，否則是錯誤。（否定詞這條是用故意改壞的引用測出漏洞後才加的。）
OCR逐字和OCR近似都要有人對照PDF頁面圖片確認，報告裡要照實寫查核方式，不能寫成逐字驗證。
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
    for lig, plain in (("\ufb00", "ff"), ("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb03", "ffi"), ("\ufb04", "ffl")):
        text = text.replace(lig, plain)
    text = text.replace("—", "-").replace("–", "-").replace("−", "-")
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


OCR_MIN = 0.9
LAYER_OK = 0.8


def layer_text(pdf):
    raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                         text=True, encoding="utf-8", errors="replace").stdout
    return normalize(raw)


def trigrams(text):
    w = re.findall(r"[a-z]{3,}", text.lower())
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}


def ocr_text(pdf):
    if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
        return ""
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "300", "-gray", str(pdf), f"{d}/p"], check=True)
        parts = []
        for img in sorted(Path(d).glob("p-*.pgm"), key=lambda x: int(x.stem.split("-")[1])):
            parts.append(subprocess.run(["tesseract", str(img), "-", "-l", "eng"], capture_output=True,
                                        text=True, encoding="utf-8", errors="replace").stdout)
    return normalize("\n".join(parts))


NEGATIONS = {"not", "no", "never", "nor", "without", "cannot", "neither", "none"}


def digits(s):
    return re.findall(r"\d+", s)


def key_words(s):
    w = re.findall(r"[a-z']+", s.lower())
    return sorted(x for x in w if x in NEGATIONS or x.endswith("n't") or (x.startswith("un") and len(x) > 4))


def best_match(q, text):
    words, qn = text.split(" "), len(q.split(" "))
    best, best_cand = 0.0, ""
    for i in range(0, max(1, len(words) - qn + 1)):
        for span in (qn - 1, qn, qn + 1):
            cand = " ".join(words[i:i + span])
            r = difflib.SequenceMatcher(None, q.lower(), cand.lower()).ratio()
            if r > best:
                best, best_cand = r, cand
    return best, best_cand


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
    layers, ocrs, reliable = {}, {}, {}
    ok, ocr_exact, near, bad, skipped = 0, 0, 0, 0, 0
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
            nq = normalize(q)
            if src not in layers:
                layers[src] = layer_text(pdf)
            if nq in layers[src]:
                ok += 1
                continue
            if src not in ocrs:
                ocrs[src] = ocr_text(pdf)
                to = trigrams(ocrs[src])
                overlap = len(to & trigrams(layers[src])) / max(1, len(to))
                reliable[src] = overlap >= LAYER_OK
                print(f"[說明] {src}：文字層和OCR的三字組重疊 {overlap:.2f}，"
                      f"{'文字層可靠' if reliable[src] else '文字層不可靠，改用OCR'}")
            if not ocrs[src]:
                print(f"[無法比對] {card.name}：文字層找不到，這台電腦也沒有OCR工具")
                skipped += 1
            elif reliable[src]:
                print(f"[錯誤] {card.name}：PDF裡找不到這段引用：{q}")
                bad += 1
            elif nq in ocrs[src]:
                print(f"[OCR逐字] {card.name}：要對照PDF頁面確認：{q}")
                ocr_exact += 1
            else:
                r, cand = best_match(nq, ocrs[src])
                if r >= OCR_MIN and digits(nq) == digits(cand) and key_words(nq) == key_words(cand):
                    print(f"[OCR近似] {card.name}：相似度 {r:.2f}，要對照PDF頁面確認：{q}")
                    near += 1
                else:
                    print(f"[錯誤] {card.name}：PDF裡找不到這段引用（最接近的相似度 {r:.2f}）：{q}")
                    bad += 1
    print(f"\n引用 {ok + ocr_exact + near + bad + skipped} 段：逐字找到 {ok}，OCR逐字 {ocr_exact}，"
          f"OCR近似 {near}，找不到 {bad}，無法比對 {skipped}。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
