"""視覺回歸：把新截圖跟基準截圖比。

用法：python3 tests/compare_shots.py tests/visual-baseline <新截圖資料夾>
      python3 tests/compare_shots.py --update tests/visual-baseline <新截圖資料夾>   # 把新截圖存成基準（要在紀錄寫為什麼更新）

標準（跑之前定好）：
- 圖的大小（寬、高）要一樣；高度不一樣代表版面長短變了，算沒通過。
- 同一個位置，三個顏色通道裡差最多的超過32（0到255）算「不同的像素」；不同的像素不能超過全部的0.2%。
沒通過的會在新截圖資料夾存一張diff-*.png，不同的地方標成紅色。
"""
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops

THRESH, MAX_FRAC = 32, 0.002


def main():
    args = sys.argv[1:]
    update = "--update" in args
    args = [a for a in args if a != "--update"]
    base, new = Path(args[0]), Path(args[1])
    shots = sorted(new.glob("*.png"))
    shots = [p for p in shots if not p.name.startswith("diff-")]
    if update:
        base.mkdir(parents=True, exist_ok=True)
        for p in shots:
            shutil.copy(p, base / p.name)
        print(f"已把{len(shots)}張截圖存成基準：{base}")
        return 0
    bad = 0
    for p in shots:
        b = base / p.name
        if not b.exists():
            print(f"沒通過｜{p.name}：沒有基準截圖")
            bad += 1
            continue
        A, B = Image.open(b).convert("RGB"), Image.open(p).convert("RGB")
        if A.size != B.size:
            print(f"沒通過｜{p.name}：大小不同，基準{A.size}、新的{B.size}")
            bad += 1
            continue
        d = ImageChops.difference(A, B)
        r, g, bl = d.split()
        mx = ImageChops.lighter(ImageChops.lighter(r, g), bl)
        mask = mx.point(lambda v: 255 if v > THRESH else 0)
        n = mask.histogram()[255]
        frac = n / (A.size[0] * A.size[1])
        ok = frac <= MAX_FRAC
        print(f"{'通過' if ok else '沒通過'}｜{p.name}：不同的像素{n}個（{frac * 100:.3f}%，上限{MAX_FRAC * 100}%）")
        if not ok:
            bad += 1
            over = B.copy()
            over.paste((230, 0, 0), mask=mask)
            over.save(new / f"diff-{p.name}")
    missing = [b.name for b in sorted(base.glob("*.png")) if not (new / b.name).exists()]
    for m in missing:
        print(f"沒通過｜{m}：這次沒有截到")
        bad += 1
    print(f"\n共{len(shots)}張，沒通過{bad}張。")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
