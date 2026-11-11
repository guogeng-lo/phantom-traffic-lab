---
id: sugiyama2008-mechanism
type: model_theory
source: sugiyama2008
locator: 第1～2頁摘要、第3頁第2段、第7頁第1～2段
conditions: 作者依自己的交通流模型（引用參考文獻[2]～[4]）做的解釋，不是這個實驗直接量到的
units: 無數值
status: confirmed
related: sugiyama2008-jam-emerges, sugiyama2008-23-vehicles
---

## 主張

作者的解釋是：車流裡一直都有小波動。車子少的時候波動會消失；平均密度超過某個臨界值時，均勻車流變得不穩定，波動會長大，最後變成塞車。瓶頸只是讓密度超過臨界值的觸發，不是塞車的根本原因。

## 原文依據

第3頁第2段整理了機制：密度低時小波動會消失，超過臨界值時波動會持續成長並破壞自由流，數學上是自由流解變不穩定、塞車解變穩定，作者把它理解成非平衡系統的相變。第7頁說瓶頸看起來像塞車的原因，是因為瓶頸讓密度超過了臨界值。

> a bottleneck is only a trigger and not the essential origin of a traffic jam

## 限制

- 這是作者用自己的模型做的解釋。實驗支持的是「沒有瓶頸、密度夠高時也可能塞車」，不是「所有塞車都跟瓶頸無關」。
- 作者只講到「超過臨界密度就不穩定」，沒有討論密度非常高時的情況。我們選題階段的模擬（`audition/page3_check.log`）在密度很高時又變回穩定，這是範圍不同，不算矛盾，見[disputes.md](../disputes.md)。
- 文中引用的Kerner理論對塞車成因有不同看法，還沒讀，見[disputes.md](../disputes.md)。
