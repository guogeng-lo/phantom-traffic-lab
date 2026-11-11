# 研究差異與未解問題

每一條都要連回相關的證據卡。分類：1假設或方法不同、2條件不同、3結論真的衝突、4資料不足。

| 問題 | 分類 | 相關證據卡 | 目前判斷 | 會不會影響簡報核心主張 |
|---|---|---|---|---|
| 瓶頸只是觸發，還是塞車的成因之一？ | 4資料不足 | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 目前無法判斷。Sugiyama 2008第4～5頁支持特定環道條件下沒有瓶頸也會塞車，第7頁是作者對瓶頸的解釋。要判斷是不是真的衝突，需要另一篇在可比條件下的明確主張；它引用的Kerner立場我們還沒讀，待確認 | 不影響「沒有瓶頸也會塞」（有實驗支持），但簡報不能寫「塞車都跟瓶頸無關」 |
| 密度很高時還會不穩定嗎？ | 4資料不足 | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md)、[bando1995-stable-regions](cards/bando1995-stable-regions.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | Sugiyama 2008沒討論很擠的情況；Bando 1995的模型（圖10）很擠時是穩定的；Tadaki 2013在單一高密度場次（40台）觀察到均勻流，但只有一場、是第一天，作者自己說不確定是不是模型預測的那種。目前無法判斷真實車流是否如此 | 第3頁可以講「模型預測」和「單一場次觀察到均勻流」，不能講成「已經證實」 |
| 實驗的塞車波速度能不能跟我們的模擬比？ | 2條件不同 | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md) | 目前不能直接比：實驗是約20 km/h，有物理單位；選題階段的模擬是無因次單位。要先建立長度和時間的尺度（一組有出處的參數），才能比數值 | 影響簡報能不能說「模擬跟實驗一致」 |
| 22台車的分界是不是a/2？ | 2條件不同 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[orosz2010-ring-stability](cards/orosz2010-ring-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md) | 不衝突。Bando式(12)的a/2是長波極限（車距固定、車數很多）的條件；有限環道依式(9)(11)保留離散的波數。Orosz 2010附錄A的公式代入Bando模型（W=0、沒有延遲、不計車長），在式(24)的速度函數、車距b=2（V'(b)=1）、22台車時，敏感度a的分界是1.9595，跟我們從Bando式(11)推的一樣，代換那一步是我們做的。模擬量到的值是我們自己的程式結果，獨立審查無法從論文核對 | 只影響第3頁的進階展開區 |
| 要不要加入反應延遲？ | 1假設或方法不同 | [bando1995-no-delay](cards/bando1995-no-delay.md)、[orosz2010-delays](cards/orosz2010-delays.md) | Bando 1995刻意不加，認為二階方程式已經包含延遲效果；Orosz 2010說延遲夠大時，可能改成短的波先失去穩定。我們的模型沒有延遲，所以「最先不穩定的是最長的波」只在這個前提下成立。不判誰對 | 不影響核心主張；簡報不能把a講成反應時間 |
| 塞車的火種是隨機減速，還是車流本身不穩定？ | 1假設或方法不同 | [nagel1992-randomization](cards/nagel1992-randomization.md)、[bando1995-ovm-equation](cards/bando1995-ovm-equation.md) | 要分開「擾動從哪來」和「擾動怎麼長大」：NaSch用隨機減速不斷產生速度波動；Bando的例子是先給一個小的位置擾動，再看確定性模型怎麼把它放大。兩者假設不同，不判誰對；兩篇環道實驗提供的是車流演化的觀察，不足以在這兩個模型之間排除其中一個 | 簡報第3頁以Bando為主要模型時，要說明這只是其中一種解釋 |
| 塞車波往後的速度是15 km/h還是20 km/h？ | 2條件不同 | [nagel1992-real-units](cards/nagel1992-real-units.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md) | 不算衝突。NaSch第2228頁提到高速公路約15 km/h的量測值（未交代出處和量法），Sugiyama和Tadaki在各自的環道報告約20 km/h；都是近似值，並列各自的條件即可 | 簡報要分開寫各自的條件：高速公路約15 km/h（NaSch轉述，沒有交代出處和量法）；環道實驗約20 km/h（Sugiyama、Tadaki）。不合成一個通用的數字 |
| 真實實驗裡消掉波的方法，跟我們簡報的平滑車示範一樣嗎？ | 1假設或方法不同 | [stern2018-controllers](cards/stern2018-controllers.md)、[stern2018-results](cards/stern2018-results.md) | 不一樣。Stern 2018實驗A是FollowerStopper、B是受過訓練的駕駛執行同類策略、C是帶飽和的PI控制器，都在真實車上測；我們如果做平滑車示範，是在Bando模型裡用自己簡化的規則。只能說「參考同樣的想法」 | 平滑車是加分功能；要做的話頁面上必須寫清楚 |
