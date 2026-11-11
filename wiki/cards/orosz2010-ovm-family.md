---
id: orosz2010-ovm-family
type: review
source: orosz2010
locator: 第4461頁式(3.7)前的h_n定義和式(3.7)、第4462頁式(3.10)和三種延遲設定、第4462～4463頁式(3.12)
conditions: 單車道、車子一樣長、駕駛相同；綜述整理
units: 保留物理量綱（距離、速度、鬆弛時間T）
status: confirmed
related: bando1995-ovm-equation, bando1995-no-delay
---

## 主張

在Orosz等人的整理裡，動態跟車模型把加速度寫成車距、車距變化和自己速度的函數，可以有反應延遲；OV模型是其中一類，加速度＝（想開的速度－現在速度）÷T，再加一項看相對速度的W。作者說，延遲全部設為0的做法就是Bando 1995用的。

## 原文依據

第4461頁在式(3.7)前定義車距h_n = x_{n+1} − x_n − ℓ，是兩車保險桿之間的距離（扣掉車長ℓ），式(3.7)是它對時間的微分。第4462頁式(3.10)是一般的動態模型，列出三種常見的延遲設定，第一種「零反應時間」引用Bando 1995。第4462頁式(3.12)是OV模型，第一項是以鬆弛時間T趨向最佳速度V(h)，W是看相對速度的項；第4462～4463頁說W=0、沒有延遲的情況已被大量研究，引用Bando 1995。

> This is usually justified by saying that dynamic models (3.10) may reproduce uniform flow as well as stop-and-go waves for zero reaction time

## 限制

- Bando 1995沒有W項、也不考慮車長，所以要對應時W=0、車長0，Bando的a對應這裡的1/T。這個對應寫在`wiki/derivations/finite-n-threshold.md`。
