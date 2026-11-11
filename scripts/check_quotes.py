"""逐字比對證據卡引用的英文原文，確認真的出現在論文PDF裡。

用法：python3 scripts/check_quotes.py [--root 路徑]
需要pdftotext（poppler-utils）。PDF放在raw/<文獻id>.pdf，不上傳，所以只有手上有PDF的人能跑；
沒有PDF的文獻會列出「無法比對」，不算通過也不算失敗。
比對前會把換行、連字號斷行、引號和空白統一，其他字必須完全一樣。
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import parse  # noqa: E402


def normalize(text):
    text = text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    text = text.replace("—", "-").replace("–", "-").replace("−", "-")
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


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
    texts, ok, bad, skipped = {}, 0, 0, 0
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
                raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True,
                                     text=True, encoding="utf-8", errors="replace").stdout
                texts[src] = normalize(raw)
            if normalize(q) in texts[src]:
                ok += 1
            else:
                print(f"[錯誤] {card.name}：PDF裡找不到這段引用：{q}")
                bad += 1
    print(f"\n引用 {ok + bad + skipped} 段：找到 {ok}，找不到 {bad}，無法比對 {skipped}。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
