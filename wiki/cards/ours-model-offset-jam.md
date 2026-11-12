---
id: ours-model-offset-jam
type: our_simulation
source: runs/logs/2026-11-12-model-core.log
locator: 測試M4（model/run_core.py）
conditions: model/ovm.py；N=22、L=44、a=1；一開始均勻，只把第0台車往前移ε；RK4，dt=0.05；平均車距2（L/N）
units: 無因次
status: confirmed
related: bando1995-spontaneous-jam, ours-model-click-brake
---

## 主張

模型裡，只把一台車往前偏一點點，也會長成塞車（有車的速度低於0.1）。偏0.1時在模型時間92出現，偏0.01時在120.5，偏0.2時在87。

## 原文依據

這是我們的模擬。`model/CRITERIA.md`的M4事先寫好選擇規則：Bando用的0.1落在[60, 300]就用0.1，所以第1頁用0.1。

## 限制

- 偏移是我們故意設定的，模型不會自己產生擾動。
- 時間是無因次的模型時間，不是秒。畫面播放多快是另外決定的顯示設定，要寫明動畫已加速。
