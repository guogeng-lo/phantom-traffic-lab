---
id: ours-model-fast-adjust
type: our_simulation
source: runs/logs/2026-11-12-model-v3-core-rerun.log
locator: 測試M5c（model/run_core.py）
conditions: model/ovm.py第3版；N=22、L=44；a=2.2、2.5、3.0；跟第2頁一樣的煞車
units: 無因次
status: confirmed
related: ours-model-threshold, ours-model-propagation
---

## 主張

每台車調整速度夠快（a=2.2、2.5、3.0）時，同樣點一下，不會形成塞車，擾動在300模型時間內衰減到0.01以下（4e−4、1e−4、2e−5）。

## 原文依據

這是我們的模擬。`model/CRITERIA.md`的M5c，求解器修正後重跑，數字跟修正前相同。

## 限制

- 只測了這三個a和這一種煞車大小。
- a不是反應時間。
