---
id: ours-model-n-sweep
type: our_simulation
source: runs/2026-11-12-model-v3-r1.md
locator: 測試M2、M2v2、M2補測（model/run_core.py、model/run_v2.py、model/run_v3_m2.py）
conditions: model/ovm.py；L=44、a=1；N=3～60；k=1的小擾動；RK4，dt=0.05；量法照model/CRITERIA.md第2、3版
units: 無因次
status: confirmed
related: ours-finite-n-threshold, bando1995-stable-regions, ours-model-uniform-dense
---

## 主張

環長44、a=1時，解析推導預測16～39台會放大。正式模型的數值驗證：58個N裡57個量測資料足夠，全部跟理論相符；其中會放大的是16～20、22～39台。21台因為成長太快、量測區間不到事先規定的200，標為數值無法判定，不能說已經通過數值驗證。

## 原文依據

這是我們的模擬。第1版量法有漏洞（沒通過），第2版改量法後N=20、21資料不足，第3版補測後N=20相符、N=21仍不足。三次結果都保留，見`runs/2026-11-12-model-core-r1.md`、`runs/2026-11-12-model-v2-r1.md`、`runs/2026-11-12-model-v3-r1.md`。M2整體的判定是「數值無法判定」。

## 限制

- 21台量到的成長率跟理論差不到1e−8，但量測區間只有190左右，照事先規定不算驗證。
- 量法是看過第1、2次結果之後才改的，使用者批准，紀錄在`runs/2026-11-12-model-criteria-v2.md`、`runs/2026-11-12-model-criteria-v3.md`。
- 模擬的車數和真實實驗的密度不能直接對數字，模擬是無因次的。
