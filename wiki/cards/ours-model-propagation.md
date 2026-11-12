---
id: ours-model-propagation
type: our_simulation
source: runs/logs/2026-11-12-model-v3-core-rerun.log
locator: 測試M7（model/run_core.py）
conditions: model/ovm.py第3版；N=22、L=44；第2頁的煞車；a=1和a=2.5對照
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-no-delay, ours-model-fast-adjust
---

## 主張

同樣點一下，a=1時擾動在200模型時間內放大28倍，a=2.5時縮到0.03倍。a=1時，被點那台後面21台的最低速度，有19台比前一台低，但不是每一台都更低。

## 原文依據

這是我們的模擬。M7用整體的擾動大小判定，事先寫明不要求每一台都比前一台低；逐台的最低速度只記錄。

## 限制

- 不能說「每一台都比前一台煞得更深」，第13台就比第12台高。
- 只測了這一組條件。
