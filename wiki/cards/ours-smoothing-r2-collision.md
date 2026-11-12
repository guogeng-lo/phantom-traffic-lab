---
id: ours-smoothing-r2-collision
type: our_simulation
source: runs/logs/2026-11-12-model-smoothing.log
locator: 測試M8的R2（model/explore_smoothing.py）
conditions: model/ovm.py；N=22、L=44、a=1；同R3的情境；規則：照原本的模型，但加速度限制在±0.05
units: 無因次
status: confirmed
related: ours-smoothing-r3
---

## 主張

在我們的模型裡，只限制平滑車的加速度、沒有安全機制時會撞車（最小車距變成−14.5，物理檢查失敗）。車速波動雖然剩50%，但這是失敗的規則，不能當可用的策略。

## 原文依據

這是我們的模擬。這是我們自己設計的平滑車規則，不是Stern 2018的控制器。照`model/CRITERIA.md`的M8判定為無效。

## 限制

- 只能當失敗案例。
- 這組模擬在第3版求解器修正（煞車改用整數步數）之前跑的；回歸測試R7證明沒有用煞車的模擬，修正前後逐位元相同（含R3平滑車的情境，`runs/logs/2026-11-12-model-v3-regression.log`）。
