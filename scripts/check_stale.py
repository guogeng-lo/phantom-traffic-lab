"""比對檢查紀錄裡記的檔案SHA-256跟現在的檔案（graph.md「上游改了，下游怎麼辦」）。

用法：python3 scripts/check_stale.py                     # 列出runs/裡每一份有SHA-256表格的紀錄，是「最新」還是「已過期」
      python3 scripts/check_stale.py runs/某份紀錄.md ...   # 只看指定的紀錄；有任何一份過期，結束代碼是1

紀錄裡的表格要長這樣（表頭第一欄是「檔案」、第二欄是「SHA-256」）：
| 檔案 | SHA-256 |
|---|---|
| `wiki/slide-map.md` | `64位十六進位` |
舊的紀錄過期是正常的（後來又改過）；最終交件看的是每一關最後那份紀錄。
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`")


def table(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out, on = [], False
    for ln in lines:
        if re.match(r"^\|\s*檔案\s*\|\s*SHA-256", ln):
            on = True
            continue
        if on:
            if re.match(r"^\|[-\s|]+\|$", ln):
                continue
            m = ROW.match(ln)
            if m:
                out.append((m.group(1), m.group(2)))
            else:
                on = False
    return out


def status(path):
    rows, stale = table(path), []
    for f, h in rows:
        p = ROOT / f
        now = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        if now != h:
            stale.append(f + ("（檔案不見了）" if now is None else ""))
    return rows, stale


def main():
    given = [Path(a) for a in sys.argv[1:]]
    recs = given or sorted((ROOT / "runs").glob("*.md"))
    bad = 0
    for r in recs:
        r = r if r.is_absolute() else ROOT / r
        rows, stale = status(r)
        if not rows:
            if given:
                print(f"沒有SHA-256表格｜{r.relative_to(ROOT)}")
                bad += 1
            continue
        if stale:
            bad += 1
            print(f"已過期｜{r.relative_to(ROOT)}：{len(stale)}／{len(rows)}個檔案改過：{'、'.join(stale)}")
        else:
            print(f"最新｜{r.relative_to(ROOT)}：{len(rows)}個檔案都跟紀錄一樣")
    return 1 if (given and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
