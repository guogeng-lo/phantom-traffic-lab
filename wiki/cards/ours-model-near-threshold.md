---
id: ours-model-near-threshold
type: our_simulation
source: runs/logs/2026-11-12-model-v3-core-rerun.log
locator: 測試M5d（model/run_core.py）
conditions: model/ovm.py第3版；N=22、L=44；a=1.90～2.10；第2頁的煞車和三倍煞車；跑到點擊後1500
units: 無因次
status: confirmed
related: ours-model-threshold, ours-model-fast-adjust
---

## 主張

分界（約1.96）附近變化很慢。a=1.90、1.94理論上會放大，但點擊後1500模型時間內都還沒形成塞車，擾動只是慢慢變大；a=1.98～2.10的擾動慢慢變小。這次測的煞車大小，沒有看到理論說穩定、卻出現塞車的情況。

## 原文依據

這是我們的模擬。M5d事先寫明只記錄、不判通過，用來決定第5頁怎麼說明分界附近的情況。

## 限制

- 只測了兩種煞車大小，更大的擾動沒有測。
- 頁面上不能只靠動畫說明分界，要寫「越靠近分界，變化越慢」。
