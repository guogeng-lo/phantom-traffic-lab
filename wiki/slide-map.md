# 簡報頁面和證據卡對照

依`pipeline/outline.md`第2版填寫（2026-11-12）；模型測試完成後，原本還沒建的模擬卡換成正式的【我們的模擬】證據卡（2026-11-12）；寫逐頁稿時，補上逐頁稿實際用到的卡（2026-11-12，見`runs/2026-11-12-d-pages-draft1.md`）。每頁的核心主張都要對到至少一張證據卡。

【我們的模擬】的卡都來自`model/`的正式測試，測試標準和結果見`model/CRITERIA.md`和`runs/2026-11-12-model-*.md`。

| 頁 | 核心主張 | 證據卡 | 層次 |
|---|---|---|---|
| 1 | 真實環道實驗裡，沒有瓶頸也出現了塞車 | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-jam-emerges](cards/sugiyama2008-jam-emerges.md) | 主線 |
| 1 | 模型裡，一個很小的初始偏移會長成塞車 | [bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)、[ours-model-offset-jam](cards/ours-model-offset-jam.md) | 主線 |
| 1 | 實驗支持的是「沒有瓶頸也可能塞」，不是「塞車都跟瓶頸無關」 | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 知識 |
| 2 | 模型裡，一台車短暫減速，會在後面的車裡放大成塞車 | [bando1995-ovm-equation](cards/bando1995-ovm-equation.md)、[bando1995-velocity-function](cards/bando1995-velocity-function.md)、[bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)、[ours-model-click-brake](cards/ours-model-click-brake.md) | 主線 |
| 3 | 車往前開，塞車團往後移；真實環道約20 km/h | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)、[ours-model-wave-direction](cards/ours-model-wave-direction.md) | 主線 |
| 4 | 在指定條件下，擾動往後傳、越傳越大；調整夠快時越傳越小 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[bando1995-no-delay](cards/bando1995-no-delay.md)、[ours-model-propagation](cards/ours-model-propagation.md) | 主線、進階 |
| 5 | 22台、車距2時，調整強度a有一條分界，約1.96 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md)、[orosz2010-ring-stability](cards/orosz2010-ring-stability.md)、[ours-model-threshold](cards/ours-model-threshold.md)、[ours-model-near-threshold](cards/ours-model-near-threshold.md)、[ours-model-fast-adjust](cards/ours-model-fast-adjust.md)、[ours-model-click-brake](cards/ours-model-click-brake.md) | 主線、進階 |
| 6 | 環長固定時，車太少、太多都不會放大，中間最容易；太擠時是大家一起慢。分開寫：解析推導預測16～39台會放大；模擬驗證了16～20、22～39台；21台模擬無法判定 | [bando1995-stable-regions](cards/bando1995-stable-regions.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-model-n-sweep](cards/ours-model-n-sweep.md)、[ours-model-uniform-dense](cards/ours-model-uniform-dense.md) | 主線 |
| 6 | 真實環道：車少順、車多塞；臨界密度約每公尺0.08～0.09台 | [tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[tadaki2013-critical-density](cards/tadaki2013-critical-density.md) | 主線 |
| 6 | 同一個密度有時順、有時塞；40台那一場是均勻的（作者不確定） | [tadaki2013-metastable](cards/tadaki2013-metastable.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | 知識、進階 |
| 7 | 三個真實環道實驗都看到沒有障礙物也會出現走走停停，塞車往後移 | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-setup](cards/tadaki2013-setup.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)、[stern2018-setup](cards/stern2018-setup.md)、[stern2018-waves-emerge](cards/stern2018-waves-emerge.md) | 主線 |
| 7 | 實驗的塞車波速度跟高速公路上量到的差不多（作者引用別人的資料） | [sugiyama2008-highway-comparison](cards/sugiyama2008-highway-comparison.md) | 知識 |
| 7 | 基本圖：高速公路一個地點的資料在臨界密度附近分成兩群；環道和高速公路的臨界密度，作者用粗略比例認為一致 | [sugiyama2008-fundamental-diagram](cards/sugiyama2008-fundamental-diagram.md)、[tadaki2013-expressway-consistency](cards/tadaki2013-expressway-consistency.md) | 知識、進階 |
| 8 | 在Stern的環道實驗裡，一台車照平均速度開，波明顯變弱 | [stern2018-setup](cards/stern2018-setup.md)、[stern2018-controllers](cards/stern2018-controllers.md)、[stern2018-results](cards/stern2018-results.md) | 主線 |
| 8 | 實驗A把目標速度調得比車流快，波又回來 | [stern2018-wave-returns](cards/stern2018-wave-returns.md) | 主線 |
| 8 | 我們設計的平滑車規則在我們的模型裡的效果：車速波動、平均車速、安全性分開呈現；R3是主要互動，R1是比較方案（波動消失但平均車速少約21%），R2撞車是失敗案例 | [ours-smoothing-r3](cards/ours-smoothing-r3.md)、[ours-smoothing-r1](cards/ours-smoothing-r1.md)、[ours-smoothing-r2-collision](cards/ours-smoothing-r2-collision.md) | 主線、知識 |
| 8 | 第三題：平滑車開得比大家快，減弱波的效果一定比較好嗎？（目標速度越快，剩下的波動越大，但沒有重新形成塞車；不能說重現了Stern實驗A） | [ours-smoothing-target-speed](cards/ours-smoothing-target-speed.md)、[stern2018-wave-returns](cards/stern2018-wave-returns.md) | 主線 |
| 9 | 模型的假設和其他觀點：隨機減速、反應延遲 | [nagel1992-rules](cards/nagel1992-rules.md)、[nagel1992-randomization](cards/nagel1992-randomization.md)、[nagel1992-circle-jams](cards/nagel1992-circle-jams.md)、[orosz2010-delays](cards/orosz2010-delays.md)、[orosz2010-ovm-family](cards/orosz2010-ovm-family.md) | 知識、進階 |
| 9 | 模型的其他簡化：所有駕駛都一樣、單車道、只看前一台車 | [bando1995-ovm-equation](cards/bando1995-ovm-equation.md) | 知識 |
| 9 | 模擬沒有單位，模擬的塞車團速度不能說成20 km/h；20 km/h是真實實驗的數字 | [ours-model-wave-direction](cards/ours-model-wave-direction.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md) | 知識 |
| 9 | 實驗的場次很少 | [sugiyama2008-jam-emerges](cards/sugiyama2008-jam-emerges.md)、[stern2018-results](cards/stern2018-results.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | 知識 |
| 9 | 實驗支持「沒有瓶頸也可能塞」；「瓶頸只是觸發」是作者用模型做的解釋 | [sugiyama2008-setup](cards/sugiyama2008-setup.md)、[sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 知識 |
| 10 | 三題測驗對應前面的頁，不新增主張：沒有事故也會塞（真實實驗）、塞車波往後傳（實驗和模型）、什麼條件下小擾動會放大（模型） | [sugiyama2008-jam-emerges](cards/sugiyama2008-jam-emerges.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[ours-model-wave-direction](cards/ours-model-wave-direction.md)、[bando1995-linear-stability](cards/bando1995-linear-stability.md)、[ours-model-threshold](cards/ours-model-threshold.md) | 主線 |
