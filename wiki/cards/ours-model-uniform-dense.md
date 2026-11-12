---
id: ours-model-uniform-dense
type: our_simulation
source: runs/logs/2026-11-12-model-core.log
locator: 測試M3（model/run_core.py）
conditions: model/ovm.py；N=44、L=44（車距1）、a=1；RK4，dt=0.05
units: 無因次
status: confirmed
related: ours-model-n-sweep, bando1995-stable-regions
---

## 主張

44台擠在環長44的環上時，均勻車流的速度是0.2024（V(1)），模擬跑到1000一直維持這個速度，誤差2e−11；加上小擾動也會衰減，衰減率跟理論一樣。也就是大家一起很慢地走，但小擾動不會放大。

## 原文依據

這是我們的模擬。`model/CRITERIA.md`的M3，容許誤差事先寫好（速度差1e−9以內）。

## 限制

- 「不會放大」只指很小的擾動，不等於「不塞」或「開得快」。
- 無因次，不能換成km/h。
