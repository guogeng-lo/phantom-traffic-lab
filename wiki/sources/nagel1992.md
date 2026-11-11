---
id: nagel1992
kind: paper
authors: Kai Nagel, Michael Schreckenberg
year: 1992
title: A cellular automaton model for freeway traffic
venue: Journal de Physique I 2(12), 2221–2229
doi: 10.1051/jp1:1992277
url: https://doi.org/10.1051/jp1:1992277
read_status: 全文已讀
read_scope: 第2221～2229頁全文和圖1～6；用的是HAL典藏的掃描版（jpa-00246697），文字層字序錯亂，對照頁面圖片讀
independent: 是
---

## 這篇在做什麼

用一個很簡單的電腦規則模擬高速公路車流：把道路切成一格一格，每台車每一步照4條規則加速、減速、隨機慢一下、往前走。這種方法叫細胞自動機（cellular automaton），後來常被叫做NaSch模型。作者發現車變多時，車流會從順暢變成走走停停，而且塞車是隨機出現的。

頁碼用期刊頁碼（第2221～2229頁）。

## 研究條件

- 單一車道，路切成L格，每格最多一台車；車速是0到v_max的整數（第2222頁）。
- 大部分模擬用v_max=5（第2222頁）。
- 第3節是環狀道路（週期邊界），第4節是一端有瓶頸的開放道路（第2222、2227頁）。
- 第5節才把格子和時間步換算成真實單位：一格約7.5公尺、一步約1秒（第2227頁）。
- 隨機減速的機率p，文中沒有寫主要模擬用的數值（圖6的標籤看起來是p=0.5，但內文沒寫，所以不採用）。

## 主要結果

- 4條規則：[cards/nagel1992-rules.md](../cards/nagel1992-rules.md)
- 隨機減速這一步是關鍵：[cards/nagel1992-randomization.md](../cards/nagel1992-randomization.md)
- 環狀道路上，密度高時塞車隨機出現、往後移動：[cards/nagel1992-circle-jams.md](../cards/nagel1992-circle-jams.md)
- 從順暢到塞車的轉變在密度約0.08附近，但確切位置不清楚：[cards/nagel1992-transition.md](../cards/nagel1992-transition.md)
- 換算真實單位：[cards/nagel1992-real-units.md](../cards/nagel1992-real-units.md)
- 瓶頸路段：[cards/nagel1992-bottleneck.md](../cards/nagel1992-bottleneck.md)

## 限制

- 這是模型和模擬，不是實驗。
- 它對塞車成因的解釋跟Bando 1995不同：這裡的塞車靠隨機減速觸發，Bando的模型沒有隨機性，是車流本身不穩定。這是假設不同，不判誰對，見[disputes.md](../disputes.md)。
- 換算真實單位的幾種方法只「數量級一致」，作者自己說是粗略的論證（第2227頁）。

## ingest紀錄

- [runs/2026-11-11-n1-nagel1992-r1.md](../../runs/2026-11-11-n1-nagel1992-r1.md)
