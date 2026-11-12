---
id: ours-smoothing-target-speed
type: our_simulation
source: runs/logs/2026-11-12-model-smoothing.log
locator: 測試M9（model/explore_smoothing.py）
conditions: model/ovm.py；同R3的情境；目標速度U=V(2)×0.9、1.0、1.05、1.1、1.2
units: 無因次
status: confirmed
related: ours-smoothing-r3, stern2018-wave-returns
---

## 主張

在我們的模型裡，R3平滑車的目標速度設得越快，剩下的車速波動越大：U=V(2)時是原本的42%，×1.05是49%，×1.1是55%，×1.2是63%；但這幾組都沒有重新形成塞車。U設得比大家慢（×0.9）時，車流反而完全均勻，平均車速0.868。

## 原文依據

這是我們的模擬。這是我們自己設計的平滑車規則，不是Stern 2018的控制器。M9事先寫明不預設結果。

## 限制

- 沒有重新形成塞車，所以**不能**說我們的模型重現了Stern實驗A「目標速度調太快波又回來」的結果。
- 這是我們自己設計的平滑車規則，不是Stern 2018的控制器。
- 這組模擬在第3版求解器修正（煞車改用整數步數）之前跑的；回歸測試R7證明沒有用煞車的模擬，修正前後逐位元相同（含R3平滑車的情境，`runs/logs/2026-11-12-model-v3-regression.log`）。
