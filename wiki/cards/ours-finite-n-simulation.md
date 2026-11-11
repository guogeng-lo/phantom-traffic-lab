---
id: ours-finite-n-simulation
type: our_simulation
source: audition/run2.log
locator: 測試A4、A4b（程式在audition/test_ovm.py）
conditions: V=tanh(Δx−2)+tanh2；N=22；車距2和2.5；RK4，時間步長0.05；只激發k=1的小擾動
units: 無因次
status: confirmed
related: ours-finite-n-threshold
---

## 主張

用模擬量出22台車的分界：車距2時量到1.95966（公式1.95949），車距2.5時量到1.54126（公式1.54104）。a=1.98時，照a/2條件應該不穩定，模擬裡擾動卻是衰減的。

## 原文依據

這是我們的模擬，不是論文。`audition/run2.log`的A4用兩個a值的成長率內插出分界，A4b在a=1.98量到成長率−3.88e-04。

## 限制

- 這是選題階段的程式，還不是正式的`model/`。
- 驗證的是我們的推導跟我們的模擬一致，不代表真實駕駛也這樣。
