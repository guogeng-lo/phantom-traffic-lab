---
id: stern2018
kind: paper
authors: Raphael E. Stern, Shumo Cui, Maria Laura Delle Monache, Rahul Bhadani, Matt Bunting, Miles Churchill, Nathaniel Hamilton, R'mani Haulcy, Hannah Pohlmann, Fangyu Wu, Benedetto Piccoli, Benjamin Seibold, Jonathan Sprinkle, Daniel B. Work
year: 2018
title: Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments
venue: Transportation Research Part C: Emerging Technologies（卷期和頁碼待查證）
doi: 10.1016/j.trc.2018.02.005
url: https://arxiv.org/abs/1705.01693
read_status: 全文已讀
read_scope: arXiv預印本1705.01693v1（2017-05-04）第1～14頁本文和表1～4；附錄只看了需要的部分。正式期刊版沒有讀，兩個版本可能有差異
independent: 是
---

## 這篇在做什麼

照Sugiyama的環道實驗再做一次，但車隊裡有一台可以自動控制速度的車（CAT Vehicle）。先讓所有人照常開、等走走停停波出現，再打開那台車的控制，看一台車能不能把波消掉。比較了車速的變動、急煞次數、油耗和通過量。

頁碼用arXiv預印本的頁碼（第1～18頁），不是期刊頁碼。

## 研究條件

- 單車道環道，半徑41.4公尺、周長260公尺，21～22台車（第3頁）。
- 只有一台車被控制；那台車的方向盤一直由受過訓練的人操作，只有速度是自動的（第4頁）。
- 其他駕駛是亞利桑那大學的職員，受過安全駕駛訓練，被要求像尖峰時段那樣開、盡量跟上前車，刻意不讓他們自己去消波（第4～5頁）。
- 三場實驗：A用FollowerStopper控制器（目標速度由外部觀察者給）、B由受過訓練的人照同樣策略開、C用自己算平均速度的PI控制器（第3、8～10頁）。
- 每場7～10分鐘，每種控制器只做一場。

## 主要結果

- 實驗設定：[cards/stern2018-setup.md](../cards/stern2018-setup.md)
- 三場都出現走走停停波：[cards/stern2018-waves-emerge.md](../cards/stern2018-waves-emerge.md)
- 控制的想法：照平均速度開：[cards/stern2018-controllers.md](../cards/stern2018-controllers.md)
- 打開控制後車速變動、急煞、油耗都降低：[cards/stern2018-results.md](../cards/stern2018-results.md)
- 目標速度設太高或關掉控制，波又回來：[cards/stern2018-wave-returns.md](../cards/stern2018-wave-returns.md)

## 限制

- 讀的是arXiv預印本，正式期刊版的內容和數字可能不同。
- 每種控制器只有一場，沒有重複和統計檢定。
- 本文的數字有小地方對不上：實驗B的油耗降幅，內文寫22.0%、表3寫22.1%；實驗C內文寫27.9%、表3寫28.1%。卡片以表3為準，並註明。
- 這是真實車輛實驗，但只在一條260公尺的環道上，作者說推廣到多車道高速公路還需要更多研究（第14頁）。
- 如果簡報要做「平滑車」示範，那會是我們自己的簡化版本，不是這篇的兩種控制器。

## ingest紀錄

- [runs/2026-11-11-n1-stern2018-r1.md](../../runs/2026-11-11-n1-stern2018-r1.md)
