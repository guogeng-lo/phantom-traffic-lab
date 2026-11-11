# 研究差異與未解問題

每一條都要連回相關的證據卡。分類：1假設或方法不同、2條件不同、3結論真的衝突、4資料不足。

| 問題 | 分類 | 相關證據卡 | 目前判斷 | 會不會影響簡報核心主張 |
|---|---|---|---|---|
| 瓶頸只是觸發，還是塞車的成因之一？ | 4資料不足（可能是3） | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 目前無法判斷。Sugiyama 2008依自己的模型說瓶頸只是觸發；它引用的Kerner理論看法不同，我們還沒讀Kerner | 不影響「沒有瓶頸也會塞」（有實驗支持），但簡報不能寫「塞車都跟瓶頸無關」 |
| 密度很高時還會不穩定嗎？ | 2條件不同 | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md)、[bando1995-stable-regions](cards/bando1995-stable-regions.md) | Sugiyama 2008只說超過臨界密度會不穩定，沒討論很擠的情況；Bando 1995的模型（圖10）在很擠時是穩定的。兩者不衝突，是一個沒講、一個是模型結果。真實車流要等讀Tadaki 2013的不同車數實驗 | 會影響第3頁的講法，讀完Tadaki 2013前不能下結論 |
| 實驗的塞車波速度能不能跟我們的模擬比？ | 2條件不同 | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md) | 目前不能直接比：實驗是約20 km/h，選題階段的模擬是無因次單位。要先有一組有出處、對應真實單位的參數 | 影響簡報能不能說「模擬跟實驗一致」 |
| 22台車的分界是不是a/2？ | 2條件不同 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md) | 不衝突。Bando式(12)的a/2是把所有波都算進去的條件，作者也說車數夠大時邊界不重要；22台時實際分界是1.9595（我們推導＋模擬）。等Orosz 2010 ingest後再對照文獻 | 只影響第3頁的進階展開區 |
| 要不要加入反應延遲？ | 1假設或方法不同 | [bando1995-no-delay](cards/bando1995-no-delay.md) | Bando 1995刻意不加，認為二階方程式已經包含延遲效果；同一群作者1998年有加入延遲的版本（還沒讀）。不判誰對 | 不影響核心主張；但簡報不能把a講成反應時間 |
