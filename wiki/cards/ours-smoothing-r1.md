---
id: ours-smoothing-r1
type: our_simulation
source: runs/logs/2026-11-12-model-smoothing.log
locator: 測試M8的R1（model/explore_smoothing.py）
conditions: model/ovm.py；N=22、L=44、a=1；同R3的情境；規則：a_s·(min(U_avg, V(h))−v)，U_avg是自己過去50的平均速度，a_s=1
units: 無因次
status: confirmed
related: ours-smoothing-r3, stern2018-results
---

## 主張

在我們的模型裡，平滑車改成照自己過去的平均速度開時，分三方面看：車速波動完全消失（剩0%），整條車流變成均勻；但平均車速從0.966降到0.763，少了約21%；安全方面，最小車距0.325，沒有撞車。

## 原文依據

這是我們的模擬。這是我們自己設計的平滑車規則，不是Stern 2018的控制器。照`model/CRITERIA.md`的M8判定為有效、有教學價值。

## 限制

- 這是我們自己設計的平滑車規則，不是Stern 2018的控制器。
- 波動消失的代價是整條車流變慢，要一起講。
- Stern實驗C的通過量也小降，但那是真實實驗的另一個指標，不能跟我們的平均車速直接比數字。
- 這組模擬在第3版求解器修正（煞車改用整數步數）之前跑的；回歸測試R7證明沒有用煞車的模擬，修正前後逐位元相同（含R3平滑車的情境，`runs/logs/2026-11-12-model-v3-regression.log`）。
