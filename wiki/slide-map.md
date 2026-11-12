# 簡報頁面和證據卡對照

依`pipeline/outline.md`第2版填寫（2026-11-12）。每頁的核心主張都要對到至少一張證據卡。

「待建」的卡要等`model/`的正式測試支持才建（見`pipeline/production-plan.md`的A）。建好之前，那一頁的那個主張不能放進HTML。

| 頁 | 核心主張 | 證據卡 | 層次 |
|---|---|---|---|
| 1 | 真實環道實驗裡，沒有瓶頸也出現了塞車 | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-jam-emerges](cards/sugiyama2008-jam-emerges.md) | 主線 |
| 1 | 模型裡，一個很小的初始偏移會長成塞車 | [bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)；待建：第1頁的模擬參數（M4） | 主線 |
| 2 | 模型裡，一台車短暫減速，會在後面的車裡放大成塞車 | [bando1995-ovm-equation](cards/bando1995-ovm-equation.md)、[bando1995-velocity-function](cards/bando1995-velocity-function.md)、[bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)；待建：第2頁的模擬參數（M5） | 主線 |
| 3 | 車往前開，塞車團往後移；真實環道約20 km/h | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)；待建：時空圖的波速方向（M6） | 主線 |
| 4 | 在指定條件下，擾動往後傳、越傳越大；調整夠快時越傳越小 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[bando1995-no-delay](cards/bando1995-no-delay.md)；待建：擾動傳遞（M7） | 主線、進階 |
| 5 | 22台、車距2時，調整強度a有一條分界，約1.96 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md)、[orosz2010-ring-stability](cards/orosz2010-ring-stability.md)；待建：分界的正式測試（M1） | 主線、進階 |
| 6 | 環長固定時，車太少、太多都不會放大，中間最容易；太擠時是大家一起慢 | [bando1995-stable-regions](cards/bando1995-stable-regions.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)；待建：車數掃描和均勻速度（M2、M3） | 主線 |
| 6 | 真實環道：車少順、車多塞；臨界密度約每公尺0.08～0.09台 | [tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[tadaki2013-critical-density](cards/tadaki2013-critical-density.md) | 主線 |
| 6 | 同一個密度有時順、有時塞；40台那一場是均勻的（作者不確定） | [tadaki2013-metastable](cards/tadaki2013-metastable.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | 知識、進階 |
| 7 | 三個真實環道實驗都看到沒有障礙物也會出現走走停停，塞車往後移 | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-setup](cards/tadaki2013-setup.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[stern2018-setup](cards/stern2018-setup.md)、[stern2018-waves-emerge](cards/stern2018-waves-emerge.md) | 主線 |
| 7 | 實驗的塞車波速度跟高速公路上量到的差不多（作者引用別人的資料） | [sugiyama2008-highway-comparison](cards/sugiyama2008-highway-comparison.md) | 知識 |
| 8 | 在Stern的環道實驗裡，一台車照平均速度開，波明顯變弱 | [stern2018-setup](cards/stern2018-setup.md)、[stern2018-controllers](cards/stern2018-controllers.md)、[stern2018-results](cards/stern2018-results.md) | 主線 |
| 8 | 實驗A把目標速度調得比車流快，波又回來 | [stern2018-wave-returns](cards/stern2018-wave-returns.md) | 主線 |
| 8 | 我們設計的平滑車規則在我們的模型裡的效果（探索中） | 待建：平滑車探索（M8、M9），結果不支持就不放 | 主線（有結果才放） |
| 9 | 模型的假設和其他觀點：隨機減速、反應延遲 | [nagel1992-randomization](cards/nagel1992-randomization.md)、[nagel1992-circle-jams](cards/nagel1992-circle-jams.md)、[orosz2010-delays](cards/orosz2010-delays.md)、[orosz2010-ovm-family](cards/orosz2010-ovm-family.md) | 知識、進階 |
| 10 | 三題測驗對應前面的頁，不新增主張 | 沿用第1～6頁的卡 | 主線 |
