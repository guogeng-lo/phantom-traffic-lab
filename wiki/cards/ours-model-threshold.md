---
id: ours-model-threshold
type: our_simulation
source: runs/logs/2026-11-12-model-core.log
locator: 測試M1（model/run_core.py）
conditions: model/ovm.py；V=tanh(h−2)+tanh2；N=22、L=44（車距2）；RK4，dt=0.05；只加k=1的小擾動（10^−6）；沒有延遲
units: 無因次
status: confirmed
related: ours-finite-n-threshold, ours-finite-n-simulation, bando1995-linear-stability
---

## 主張

正式模型用二分法量出22台、車距2的分界a是1.959494，公式是1.959493。分界附近7個a值，量到的成長率跟理論的差都在1e−5以下，而且正負號一致。

## 原文依據

這是我們的模擬，不是論文。`model/CRITERIA.md`的M1，在寫程式之前就定好量法和容許誤差（分界差5e−4以內，成長率差2e−5＋2%以內）。結果在`runs/logs/2026-11-12-model-core.log`。

## 限制

- 只對很小的擾動成立。
- 只驗證我們的模擬跟我們的推導（`ours-finite-n-threshold`）一致，不代表真實駕駛也有這條分界。
- a是無因次的「調整速度有多快」，不是反應時間。
