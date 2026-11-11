---
id: orosz2010
kind: paper
authors: Gábor Orosz, R. Eddie Wilson, Gábor Stépán
year: 2010
title: Traffic jams: dynamics and control
venue: Philosophical Transactions of the Royal Society A 368, 4455–4479
doi: 10.1098/rsta.2010.0205
url: https://doi.org/10.1098/rsta.2010.0205
read_status: 部分章節
read_scope: 第4455～4456頁（摘要和開頭）、第3(b)節跟車模型（第4461～4463頁）、第5節線性動力學（第4466～4467頁）、第6節開頭、附錄A（第4475～4476頁）；第2、4節和第6節大部分、第7節控制沒有細讀；用的是作者個人網站上的PDF
independent: 是
---

## 這篇在做什麼

一篇綜述，也是皇家學會一期交通主題特刊的導論。整理了交通流的各種模型、怎麼分析均勻車流穩不穩定、塞車怎麼形成，以及怎麼控制。我們主要用它的兩個部分：跟車模型的分類（確認Bando的模型在整個領域裡的位置），和附錄A裡環狀道路N台車的穩定分界公式。

頁碼用期刊頁碼（第4455～4479頁），PDF頁數等於期刊頁碼減4454。

## 研究條件

- 這是綜述，不是新的實驗或模擬；附錄A是一般跟車模型的線性分析。
- 附錄A只處理沒有反應延遲的情況（第4475頁）。
- 車距h是扣掉車長的車距（第4461頁式(3.7)），跟Bando 1995不考慮車長不同。

## 主要結果

- 跟車模型的一般形式和OV模型：[cards/orosz2010-ovm-family.md](../cards/orosz2010-ovm-family.md)
- 三種分析穩定性的方法結果相同：[cards/orosz2010-stability-approaches.md](../cards/orosz2010-stability-approaches.md)
- 環上N台車的穩定分界，最先不穩定的是最長的波：[cards/orosz2010-ring-stability.md](../cards/orosz2010-ring-stability.md)
- 有反應延遲時情況會改變：[cards/orosz2010-delays.md](../cards/orosz2010-delays.md)

跟Bando模型的對應（我們做的代換）：[derivations/finite-n-threshold.md](../derivations/finite-n-threshold.md)

## 限制

- 只讀了部分章節，讀的範圍見read_scope，沒讀的章節不拿來當證據。
- 附錄A的公式是一般模型的，對應到Bando模型要另外代換，那一步是我們做的。
- 這是綜述，對Bando模型的描述是作者的整理，原始出處還是Bando 1995。

## ingest紀錄

- [runs/2026-11-11-n1-orosz2010-r1.md](../../runs/2026-11-11-n1-orosz2010-r1.md)
