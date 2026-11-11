---
id: bando1995-stable-regions
type: model_theory
source: bando1995
locator: 第1041頁右欄最後一段、圖10
conditions: V=tanh(Δx−2)+tanh2、a=1；圖10是示意圖
units: 無數值
status: confirmed
related: bando1995-linear-stability, bando1995-cluster-values, sugiyama2008-mechanism
---

## 主張

在這篇的模型和參數條件下，在速度函數的曲線上，車距很小和車距很大的地方都是穩定區，只有中間一段是不穩定區。均勻車距落在不穩定區時，車子會被推往兩邊的穩定區，一部分擠成塞車、一部分拉開跑快。

## 原文依據

第1041頁說初始車距b落在穩定區時，小擾動不會改變車流；落在不穩定區時，每台車會被推向左右兩邊的穩定區。圖10在tanh(Δx−2)+tanh2的曲線上畫出stable、unstable、stable三區，並標出擁擠時的車距Δx_min和順暢時的車距Δx_max。

## 限制

- 圖10是示意圖，沒有標出區域邊界的數值。我們用V'(Δx)=a/2自己算，a=1時邊界約在車距1.12和2.88，跟圖上虛線的位置相符；這是我們算的，不是論文寫的。
- 這是模型的結論。真實車流在很擠的時候是不是穩定，要看密度實驗（例如Tadaki 2013），見[disputes.md](../disputes.md)。

## 教學說法

在這個模型裡，車子很少時很順，車子多到一個程度會開始走走停停，但如果擠到幾乎貼在一起，大家只能一起慢慢開，反而不會出現走走停停的波。這是模型的結果，不代表所有真實道路都這樣。
