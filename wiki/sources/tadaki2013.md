---
id: tadaki2013
kind: paper
authors: Shin-ichi Tadaki, Macoto Kikuchi, Minoru Fukui, Akihiro Nakayama, Katsuhiro Nishinari, Akihiro Shibata, Yuki Sugiyama, Taturu Yosida, Satoshi Yukawa
year: 2013
title: Phase transition in traffic jam experiment on a circuit
venue: New Journal of Physics 15, 103034 (20pp)
doi: 10.1088/1367-2630/15/10/103034
url: https://doi.org/10.1088/1367-2630/15/10/103034
read_status: 全文已讀
read_scope: 期刊第1～20頁：本文第1～12頁全文、表1、圖1～8；附錄A～E的文字和圖說（附錄裡每一場的時空圖沒有逐張細看）
independent: 是
---

## 這篇在做什麼

Sugiyama 2008那群人做的後續實驗。這次在名古屋巨蛋的室內環道，讓車數從10台到40台一場一場改變，看密度多高時會從順暢變成塞車，並估出臨界密度。作者刻意不用任何模型，只用實驗資料和高速公路常用的分析方法來估。

頁碼用期刊頁碼（第1～20頁）。典藏庫的PDF前面多兩頁，PDF頁數等於期刊頁碼加2。

## 研究條件

- 名古屋巨蛋室內平地，半徑50公尺、周長314公尺的環道（第3～4頁、圖2～3）。
- 用雷射掃描器量車的位置，大約每0.2秒一筆，空間解析度在50公尺處約0.16公尺（第5頁、附錄A）。上一次實驗是從影片人工讀，誤差約±0.5公尺。
- 兩天共19場，車數10～40台；車都是同一款（Toyota Vitz）；52位大學生輪流開（第5頁、表1）。
- 駕駛被要求用自己的方式安全駕駛，目標速度30 km/h（第5頁）。
- 第一天駕駛非常小心、沒有開到想要的速度，所以主要分析只用第一天的暖身場和第二天的資料（第6頁）。

## 主要結果

- 實驗設定：[cards/tadaki2013-setup.md](../cards/tadaki2013-setup.md)
- 車少時順、車多時塞，塞車團以約20 km/h往後傳：[cards/tadaki2013-density-dependence.md](../cards/tadaki2013-density-dependence.md)
- 臨界密度在每公尺0.08到0.09台之間：[cards/tadaki2013-critical-density.md](../cards/tadaki2013-critical-density.md)
- 中間密度時順暢和塞車兩種狀態都會出現（介穩態）：[cards/tadaki2013-metastable.md](../cards/tadaki2013-metastable.md)
- 作者說這個臨界密度跟高速公路的觀測一致：[cards/tadaki2013-expressway-consistency.md](../cards/tadaki2013-expressway-consistency.md)
- 40台車時車流反而均勻，但作者說還不確定代表什麼：[cards/tadaki2013-high-density.md](../cards/tadaki2013-high-density.md)

## 限制

- 第二天28、30、32、34台各做了2～3場，25台只有1場；場次不多，文中沒有對重複場次做統計檢定。
- 駕駛是大學生，第一天和第二天的開法明顯不同，作者為此排除了大部分第一天的資料。
- 40台那一場是第一天、沒有用在主要分析的場次，所以「很擠時變均勻」只是一個跡象。
- 跟高速公路比較的那一步是粗略的論證（車速快三倍，車距也要大三倍）。

## ingest紀錄

- [runs/2026-11-11-n1-tadaki2013-r1.md](../../runs/2026-11-11-n1-tadaki2013-r1.md)
