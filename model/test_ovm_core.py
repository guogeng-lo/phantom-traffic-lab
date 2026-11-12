"""核心求解器的回歸測試R1～R7（標準見model/CRITERIA.md「第3版修改」）。

用法：python3 model/test_ovm_core.py
結束代碼：有任何一項沒通過就是1。R7要用git讀出修改前的model/ovm.py（commit 556de5e）。
"""
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ovm  # noqa: E402
from explore_smoothing import TargetRule  # noqa: E402
from run_v2 import ClickDemo, analytic  # noqa: E402

fails = 0


def check(name, ok, detail):
    global fails
    fails += not ok
    print(f"[{'通過' if ok else '沒通過'}] {name}：{detail}", flush=True)


def record_braking(ring, n_steps):
    """跑n_steps步，記下每一步四次加速度評估的煞車狀態。"""
    log = {}
    orig = ring.accel

    def spy(x, v, braking):
        log.setdefault(ring._steps, []).append(braking)
        return orig(x, v, braking)
    ring.accel = spy
    for _ in range(n_steps):
        ring.step()
    ring.accel = orig
    return log


def r1_to_r4():
    r = ovm.Ring(22, 44.0, 1.0)
    r.brake = (0, 20.0, 0.5, 0.25)
    log = record_braking(r, 420)
    on = sorted(k for k, calls in log.items() if any(c is not None for c in calls))
    check("R1 起點", on[0] == 400 and all(c is None for c in log[399]),
          f"第一個煞車步是第{on[0]}步；第399步的四次評估：{log[399]}")
    check("R2 終點", on[-1] == 409 and all(c is None for c in log[410]),
          f"最後一個煞車步是第{on[-1]}步；第410步的四次評估：{log[410]}")
    check("R3 步數", len(on) == 10, f"有煞車的完整步：{len(on)}個（第{on[0]}～{on[-1]}步）")
    consistent = all(len(calls) == 4 and len(set(map(repr, calls))) == 1 for calls in log.values())
    check("R4 一致", consistent, f"{len(log)}個步，每一步四次評估的煞車狀態{'都一樣' if consistent else '有不一樣的'}")


def r5():
    msgs = []
    for brake in ((0, 20.01, 0.5, 0.25), (0, 20.0, 0.52, 0.25)):
        r = ovm.Ring(22, 44.0, 1.0)
        r.brake = brake
        try:
            r.step()
            msgs.append(f"{brake[1:3]}沒有報錯")
        except ValueError as e:
            msgs.append(f"{brake[1:3]}報錯：{e}")
    check("R5 不是整數就報錯", all("報錯：" in m for m in msgs), "；".join(msgs))


def r6():
    N, L, t0 = 22, 44.0, 123.456
    demo = ClickDemo(N, L, 1.0)
    xa, va = analytic(N, L, t0)
    demo.click(t0, 0, 0.5, 0.25)
    dx = max(abs(p - q) for p, q in zip(demo.ring.x, xa))
    dv = max(abs(p - q) for p, q in zip(demo.ring.v, va))
    t_show = demo.time()
    log = record_braking(demo.ring, 30)
    on = sorted(k for k, calls in log.items() if any(c is not None for c in calls))
    t_after = demo.time()
    ok = dx <= 1e-12 and dv <= 1e-12 and t_show == t0 and on == list(range(10)) and t_after == t0 + 30 * ovm.DT
    check("R6 任意時間點擊", ok,
          f"位置差 {dx:.1e}、速度差 {dv:.1e}；切換時顯示時間 {t_show!r}；煞車步 {on}；30步後顯示時間 {t_after!r}（應為{t0 + 30 * ovm.DT!r}）")


def load_old():
    src = subprocess.run(["git", "show", "556de5e:model/ovm.py"], cwd=HERE.parent, capture_output=True,
                         text=True, encoding="utf-8", check=True).stdout
    d = tempfile.mkdtemp()
    path = Path(d) / "ovm_old.py"
    path.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("ovm_old", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def compare(make, steps, switch=None):
    """make(模組)回傳一個Ring；兩個版本各跑steps步，回傳每一步位置和速度的最大差。switch=(步數, 規則工廠)。"""
    old, new = make(OLD), make(ovm)
    worst = 0.0
    for s in range(steps):
        if switch and s == switch[0]:
            old.smooth, new.smooth = (0, switch[1]()), (0, switch[1]())
        old.step()
        new.step()
        worst = max(worst, max(abs(p - q) for p, q in zip(old.x, new.x)), max(abs(p - q) for p, q in zip(old.v, new.v)))
    return worst


def offset_ring(m):
    x = [n * 2.0 for n in range(22)]
    x[0] += 0.1
    return m.Ring(22, 44.0, 1.0, x=x)


def r7():
    cases = [
        ("44台均勻跑到1000", lambda m: m.Ring(44, 44.0, 1.0), 20000, None),
        ("22台k=1擾動跑到2100", lambda m: m.mode_ring(22, 44.0, 1.0), 42000, None),
        ("22台ε=0.1跑到1000", offset_ring, 20000, None),
        ("22台R3平滑車t=300起跑到1500", offset_ring, 30000, (6000, lambda: TargetRule(ovm.V(2.0)))),
    ]
    for name, make, steps, switch in cases:
        w = compare(make, steps, switch)
        check(f"R7 沒有煞車的模擬不變：{name}", w == 0.0, f"修改前後每一步位置和速度的最大差 {w!r}（要剛好0）")


if __name__ == "__main__":
    OLD = load_old()
    r1_to_r4()
    r5()
    r6()
    r7()
    print(f"\n沒通過 {fails} 項。")
    sys.exit(1 if fails else 0)
