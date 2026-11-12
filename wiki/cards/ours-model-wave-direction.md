---
id: ours-model-wave-direction
type: our_simulation
source: runs/logs/2026-11-12-model-v3-v2-rerun.log
locator: 測試M6v2（model/run_v2.py）
conditions: model/ovm.py第3版；N=22、L=44、a=1；第2頁的煞車；取樣間隔0.5和0.05；追同一團塞車（至少3台相鄰的車速度低於0.1才開始）
units: 無因次
status: confirmed
related: sugiyama2008-backward-wave, bando1995-spontaneous-jam
---

## 主張

模型裡，車的平均速度是+0.9632（往前），塞車團的移動速度是−0.1505（往後）。兩種取樣間隔量到的一樣，畫時空圖時跨越起點的處理沒有錯誤。

## 原文依據

這是我們的模擬。M6第1版的追蹤方法有漏洞（沒通過），第2版改追蹤規則後通過，第3版求解器修正後回歸結果相同。紀錄在`runs/2026-11-12-model-core-r1.md`、`runs/2026-11-12-model-v2-r1.md`、`runs/2026-11-12-model-v3-r1.md`。

## 限制

- 波速是無因次的，**不能**說成20 km/h；20 km/h是真實環道實驗的數字。
- 只量了這一組條件。
