"""視覺風格樣本用的資料：用Python參考模型（model/ovm.py第3版、run_v2.py的ClickDemo）算一次第2頁的點擊，存成sample-data.js。

這只是給風格樣本畫圖用的，不是瀏覽器版模擬，也不是對答案。正式的瀏覽器模擬要等選定風格之後，
照AGENTS第0節第7條先寫好對答案的標準再做。

用法：python3 pipeline/style-samples/export_sample_data.py
輸出：pipeline/style-samples/sample-data.js

設定跟ours-model-click-brake一樣：N=22、L=44、a=1，第0台在模型時間0被點，β=0.25、τ=0.5；
每0.5模型時間取樣一次，存點擊後0到400。
存的是每台車偏離均勻車流的位置 d = x − (n·b + V(b)·s)，和車速v。
因為均勻車流對每台車、每個時間都一樣，讀者點第j台、在時間t_c點，畫面上的位置就是把這份資料轉j格、再平移V(b)·t_c。
塞車團的軌跡用run_v2.py的track_wave（M6v2的追蹤規則）從同一份資料算。
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "model"))
from ovm import V, fit_slope  # noqa: E402
from run_v2 import ClickDemo, track_wave  # noqa: E402

N, L, A = 22, 44.0, 1.0
BETA, TAU = 0.25, 0.5
S_END, EVERY = 400.0, 0.5


def main():
    b = L / N
    vb = V(b)
    demo = ClickDemo(N, L, A)
    demo.click(0.0, 0, TAU, BETA)
    r = demo.ring
    every = int(round(EVERY / 0.05))
    samples = [(r.t, r.x[:], r.v[:])]
    steps = 0
    while r.t < S_END - 1e-9:
        r.step()
        steps += 1
        if steps % every == 0:
            samples.append((r.t, r.x[:], r.v[:]))
    if not r.sane():
        raise SystemExit("物理檢查沒通過，不輸出")
    d = [[round(x[n] - (n * b + vb * t), 4) for n in range(N)] for t, x, _ in samples]
    v = [[round(vv[n], 4) for n in range(N)] for _, _, vv in samples]
    jam_t = next(t for t, _, vv in samples if min(vv) < 0.1)
    first = []
    for n in range(N):
        ts = [t for t, _, vv in samples if vv[n] < 0.1]
        first.append(ts[0] if ts else None)
    highlight = min((t, n) for n, t in enumerate(first) if t is not None)[1]
    tr = track_wave(samples, N, L)
    c = fit_slope(tr)
    data = {
        "source": "model/ovm.py第3版、model/run_v2.py的ClickDemo和track_wave；pipeline/style-samples/export_sample_data.py產生",
        "N": N, "L": L, "a": A, "beta": BETA, "tau": TAU, "every": EVERY, "vb": round(vb, 10),
        "jamAfterClick": round(jam_t, 2), "highlightCar": highlight,
        "track": [[round(t, 2), round(p, 3)] for t, p in tr[::4]], "trackSlope": round(c, 4),
        "d": d, "v": v,
    }
    out = Path(__file__).resolve().parent / "sample-data.js"
    out.write_text("// 自動產生，不要手改。見export_sample_data.py\nwindow.SAMPLE = " +
                   json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"取樣 {len(samples)} 個；點擊後 {jam_t:.1f} 出現車速低於0.1；先慢到0.1以下的是第{highlight}台；"
          f"塞車團軌跡 {len(tr)} 點，斜率 {c:+.4f}；{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
