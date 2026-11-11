# 研究差異與未解問題

每一條都要連回相關的證據卡。分類：1假設或方法不同、2條件不同、3結論真的衝突、4資料不足。

| 問題 | 分類 | 相關證據卡 | 目前判斷 | 會不會影響簡報核心主張 |
|---|---|---|---|---|
| 瓶頸只是觸發，還是塞車的成因之一？ | 4資料不足（可能是3） | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 目前無法判斷。Sugiyama 2008依自己的模型說瓶頸只是觸發；它引用的Kerner理論看法不同，我們還沒讀Kerner | 不影響「沒有瓶頸也會塞」（有實驗支持），但簡報不能寫「塞車都跟瓶頸無關」 |
| 密度很高時還會不穩定嗎？ | 4資料不足 | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md)、[bando1995-stable-regions](cards/bando1995-stable-regions.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | Sugiyama 2008沒討論很擠的情況；Bando 1995的模型（圖10）很擠時是穩定的；Tadaki 2013的40台那一場車流均勻，但只有一場、是第一天，作者自己說不確定是不是模型預測的那種。目前無法判斷真實車流是否如此 | 第3頁可以講「模型預測」和「實驗有一個跡象」，不能講成「已經證實」 |
| 實驗的塞車波速度能不能跟我們的模擬比？ | 2條件不同 | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md) | 目前不能直接比：實驗是約20 km/h，選題階段的模擬是無因次單位。要先有一組有出處、對應真實單位的參數 | 影響簡報能不能說「模擬跟實驗一致」 |
| 22台車的分界是不是a/2？ | 2條件不同 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md) | 不衝突。Bando式(12)的a/2是把所有波都算進去的條件，作者也說車數夠大時邊界不重要；22台時實際分界是1.9595（我們推導＋模擬）。等Orosz 2010 ingest後再對照文獻 | 只影響第3頁的進階展開區 |
| 要不要加入反應延遲？ | 1假設或方法不同 | [bando1995-no-delay](cards/bando1995-no-delay.md) | Bando 1995刻意不加，認為二階方程式已經包含延遲效果；同一群作者1998年有加入延遲的版本（還沒讀）。不判誰對 | 不影響核心主張；但簡報不能把a講成反應時間 |
| 塞車的火種是隨機減速，還是車流本身不穩定？ | 1假設或方法不同 | [nagel1992-randomization](cards/nagel1992-randomization.md)、[bando1995-ovm-equation](cards/bando1995-ovm-equation.md) | NaSch模型靠隨機減速產生塞車，Bando模型沒有隨機性、靠不穩定放大一點小擾動。兩者假設不同，不判誰對；實驗（Sugiyama 2008、Tadaki 2013）兩種解釋都沒有排除 | 簡報第3頁以Bando為主要模型時，要說明這只是其中一種解釋 |
| 塞車波往後的速度是15 km/h還是20 km/h？ | 2條件不同 | [nagel1992-real-units](cards/nagel1992-real-units.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md) | 不算衝突。NaSch引用的高速公路量測約15 km/h（未標出處），Sugiyama和Tadaki的環道實驗約20 km/h；都是「約」，道路和量法不同 | 簡報講「大約每小時十幾到二十公里往後跑」比只講一個數字安全 |
