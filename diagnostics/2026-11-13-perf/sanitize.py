"""把診斷輸出（gzip和json、txt）裡的本機路徑換成<tmp>、<chromium>、<home>、<repo>，其他內容不動（AGENTS第0節第6條）。
用法：python3 sanitize.py <診斷輸出資料夾>"""
import gzip, re, sys
from pathlib import Path
REPO = str(Path(__file__).resolve().parents[2]).encode()   # repo位置在執行時才算，原始碼裡不寫本機路徑
PAT = [(re.compile(re.escape(REPO)), b"<repo>"), (re.compile(rb"/tmp/[A-Za-z0-9._/-]*"), b"<tmp>"),
       (re.compile(rb"/opt/[A-Za-z0-9._/-]*"), b"<chromium>"), (re.compile(rb"/(root|home)/[A-Za-z0-9._/-]*"), b"<home>")]
def clean(b):
    n = 0
    for p, r in PAT:
        b, k = p.subn(r, b); n += k
    return b, n
tot = 0
for f in sorted(Path(sys.argv[1]).iterdir()):
    if f.suffix == ".gz":
        b, n = clean(gzip.decompress(f.read_bytes()))
        if n: f.write_bytes(gzip.compress(b))
    elif f.suffix in (".json", ".txt"):
        b, n = clean(f.read_bytes())
        if n: f.write_bytes(b)
    else:
        continue
    tot += n
    if n: print(f"{f.name}：換掉{n}處")
print(f"共換掉{tot}處")
