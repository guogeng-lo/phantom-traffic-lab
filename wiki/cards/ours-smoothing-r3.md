---
id: ours-smoothing-r3
type: our_simulation
source: runs/logs/2026-11-12-model-smoothing.log
locator: 測試M8的R3（model/explore_smoothing.py）
conditions: model/ovm.py；N=22、L=44、a=1；先讓塞車形成，t=300把第0台換成平滑車；比較區間[1000, 1500]；規則：a_s·(min(U, V(h))−v)，U=V(2)=0.9640，a_s=1；初始偏移ε=0.1（跟ours-model-offset-jam一樣）
units: 無因次
status: confirmed
related: ours-smoothing-r1, ours-smoothing-target-speed, stern2018-results
---

## 主張

在我們的模型裡，把一台車換成「固定目標速度、但車距不夠就照模型減速」的平滑車後，分三方面看：車速波動剩原本的42%，比較區間裡沒有車慢到0.1以下；平均車速從0.966變成0.887；安全方面，最小車距0.326，沒有撞車。

## 原文依據

這是我們的模擬。這是我們自己設計的平滑車規則，不是Stern 2018的控制器。比較項目和「有效」的標準事先寫在`model/CRITERIA.md`的M8，R3照標準判定為有效、有教學價值。

## 限制

- 這是我們自己設計的平滑車規則，不是Stern 2018的控制器。
- 只測了一組條件，不代表真實道路。
- 平均車速跟Stern實驗的通過量不是同一個指標，不能直接比數字。
- 這組模擬在第3版求解器修正（煞車改用整數步數）之前跑的；回歸測試R7證明沒有用煞車的模擬，修正前後逐位元相同（含R3平滑車的情境，`runs/logs/2026-11-12-model-v3-regression.log`）。
