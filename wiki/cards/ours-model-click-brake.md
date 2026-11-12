---
id: ours-model-click-brake
type: our_simulation
source: runs/2026-11-12-model-v3-r1.md
locator: 測試M5a v2、M5b（model/run_v2.py、model/run_core.py）
conditions: model/ovm.py第3版（煞車用整數步數判定）；N=22、L=44、a=1；點擊前用解析解；煞車β=0.25、持續τ=0.5（剛好10步）
units: 無因次
status: confirmed
related: ours-model-offset-jam, ours-model-propagation, bando1995-ovm-equation
---

## 主張

第2頁的展示做法：讀者點擊之前，均勻車流用公式算，永遠保持等距等速；點擊那一刻才開始數值積分並讓那台車短暫減速。用最輕的煞車（β=0.25、τ=0.5），點擊後模型時間89.3出現塞車；不論在20還是500點擊，結果都一樣。切換時位置、速度、時間都連續。

## 原文依據

這是我們的模擬。M5b在9種煞車組合裡照事先寫好的規則選β·τ最小的。M5a v2的切換連續性、跟數值積分基準的一致性、很晚才點擊三項都通過（第3版）。

## 限制

- 解析解只是展示做法，不是說數值積分能永遠維持均勻：數值積分不點的話，在模型時間約436就會因為浮點誤差而亂掉（M5a第1版的結果，保留）。
- 「點一下就塞」是模型裡的事，真實實驗沒有說是誰踩了煞車。
