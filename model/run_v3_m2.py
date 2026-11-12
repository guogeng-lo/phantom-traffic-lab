"""M2的補測：只補N = 20、21，初始擾動1e−7和1e−8（標準見model/CRITERIA.md「第3版修改」）。

停止條件、有效長度 ≥ 200、容許誤差、物理檢查都跟M2v2一樣，用的是同一個measure_v2。
其他56個N保留第2版的結果，不重跑。
用法：python3 model/run_v3_m2.py
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ovm import theory_sigma  # noqa: E402
from run_v2 import measure_v2, tol  # noqa: E402


def main():
    L, a = 44.0, 1.0
    verdicts = {}
    for N in (20, 21):
        st = theory_sigma(a, L / N, N)
        runs = []
        for eps in (1e-7, 1e-8):
            sm, stop, length, reason, r = measure_v2(N, L, a, eps)
            enough = length >= 200
            match = (sm > 0) == (st > 0) and abs(sm - st) <= tol(st) and r.sane()
            runs.append((enough, match))
            print(f"    N={N} ε={eps:.0e}：σ_meas {sm:+.4e} 理論 {st:+.4e} 差 {sm - st:+.2e}（容許 {tol(st):.2e}） "
                  f"有效長度 {length:.0f} 停止 t={stop:.0f}（{reason}） "
                  f"{'資料足夠' if enough else '資料不足'}{'、相符' if enough and match else ('、不符' if enough else '')}；"
                  f"S {'OK' if r.sane() else '失敗'}", flush=True)
        sufficient = [m for e, m in runs if e]
        if not sufficient:
            v = "數值無法判定"
        elif all(sufficient):
            v = "相符"
        else:
            v = "不符"
        verdicts[N] = v
        print(f"[{'通過' if v == '相符' else ('沒通過' if v == '不符' else '無法判定')}] M2補測 N={N}：{v}", flush=True)
    bad = [N for N, v in verdicts.items() if v != "相符"]
    print(f"\nN=20：{verdicts[20]}；N=21：{verdicts[21]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
