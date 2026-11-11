# 審查包（第4輪，限定範圍）：第3輪問題的修正、自動產生的索引、檢查程式

## 你的角色

你是獨立審查者。這份Wiki的第3關（研究差異與忠實度審查）原本最多3輪，第3輪沒有通過；使用者另外授權這一輪限定範圍的複核，不是重新開始。第3輪的審查意見原文附在最後。請對照6篇論文PDF和這份審查包，只檢查下面四件事，不用重審其他沒改過的內容：

1. **第3輪的6條修正**有沒有修好：`stern2018-wave-returns`、`tadaki2013-critical-density`、`tadaki2013-density-dependence`、`orosz2010-ring-stability`、`glossary.md`的「相變」、`sources/sugiyama2008.md`的限制。特別看`stern2018-wave-returns`裡實驗A、B、C的控制方式和速度調整，是否分開而且跟原文一致。
2. **自動產生的`wiki/index.md`**：文獻表和39張證據卡的清單，現在由程式從文獻檔、證據卡產生（每張放類型、狀態、條件欄位原文和主張全文，不再另寫摘要）。請確認：
   - 39張都在，類型、狀態、條件、主張跟附錄裡的卡片一致，文獻的種類和閱讀狀態跟文獻檔一致。
   - 第3輪第三部分列的18條索引不一致，現在各自是否已解決。如果是卡片主張本身就缺條件，請標明是卡片的問題。
   - 開頭的介紹和導覽是人工寫的，也看一下有沒有跟自動產生的內容矛盾。
3. **這些修改有沒有引入新的錯誤**：讀錯原文、數字或頁碼錯、把模型講成實驗、語氣過度。
4. **相關程式的回歸測試**：審查包附了`scripts/check_wiki.py`、`scripts/build_index.py`、`tests/test_check_wiki.py`的原始碼和最近一次實際執行的輸出。請看：
   - 測試情境是否真的測到它名稱說的事（例如「改了卡片沒重建索引要擋」是不是真的會失敗）。
   - 學號、手機、金鑰等個資檢查有沒有因為SHA-256雜湊值的排除而變鬆。
   - 索引同步檢查有沒有漏洞。
   - 如果你的環境能連到GitHub，可以clone公開repo `guogeng-lo/phantom-traffic-lab`，checkout到commit `5ab826c`，跑 `python3 tests/test_check_wiki.py`、`python3 scripts/check_wiki.py --strict`、`python3 scripts/build_index.py --check`，貼上實際結果；論文PDF不在repo裡，`check_quotes.py`不用跑。不能跑就寫「沒有執行」，不要推測結果。

## 上傳的PDF和對應的文獻id

| 文獻id | 檔案 | 注意 |
|---|---|---|
| bando1995 | bando.pdf | 掃描檔，頁碼看頁首的1035～1042 |
| sugiyama2008 | NewJPhys_10_033001.pdf | 前面多兩頁（典藏庫封面和出版商的頁面），頁碼看頁首的1～7 |
| nagel1992 | ajp-jp1v2p2221.pdf | 掃描檔，頁碼2221～2229 |
| tadaki2013 | NewJPhys_15_103034.pdf | 前面多兩頁，頁碼看頁首 |
| stern2018 | 1705.01693v1.pdf | arXiv預印本，頁碼就是PDF頁碼 |
| orosz2010 | PTRSA2published.pdf | 頁碼4455～4479；Wiki只讀了部分章節，見文獻檔的read_scope |



## 請照這個格式回覆

第一部分，第3輪的問題逐條回覆（6條修正和18條索引不一致，一條一列）：

| 卡片id或檔案 | 第3輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |

第二部分，新發現的問題（沒有就寫「沒有」）：

| 卡片id或檔案 | 問題類型 | 嚴重程度（會誤導讀者／不精確／小問題） | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |

第三部分，自動產生的索引：不一致或產生方式有問題的地方（沒有就寫「沒有」）。

第四部分，回歸測試：有沒有執行、實際結果、測試有沒有漏洞。

第五部分，無法確認的地方。

最後兩行寫：
- 第3輪問題修好幾條、部分修好幾條、沒修好幾條；新問題幾條（其中會誤導讀者幾條）；索引問題幾條；測試問題幾條。
- 有沒有重大問題（會誤導讀者、科學錯誤、沒修好、索引不同步、測試沒通過或測不到它宣稱的事）：有／沒有。


## 這份審查包包含的檔案版本

| 檔案 | SHA-256 |
|---|---|
| `wiki/cards/orosz2010-ring-stability.md` | `ccb72521184c38f5f2d47b5265b58a1d619d0cdcf2a5ef3e18761839820c283b` |
| `wiki/cards/stern2018-wave-returns.md` | `e41fdc1895465840b568138a64adbd183682aca174ec78301388fd5a491ceb10` |
| `wiki/cards/tadaki2013-critical-density.md` | `28172191e36bbbae688b796f526494a6bd099e65bd88445c0920fcf3319650be` |
| `wiki/cards/tadaki2013-density-dependence.md` | `11fc2986bd7fcb0a32c53dab2df341c364bb14e381573f8aab6dcd6d2a20dee1` |
| `wiki/glossary.md` | `943b7b12302fc5a77cbc1d4d37ba766a57bf249141d0d39a3dda2d037b1bcd20` |
| `wiki/index.md` | `2f2bfd7bdf3b83117612c33f1f6c958105a211ca5fda8c9546072642d75973c0` |
| `wiki/sources/sugiyama2008.md` | `a7a7113d3e307ef9324026ef7e3505ace5c80beba5e0a618ef140fffe1ed74b5` |
| `wiki/cards/bando1995-capacity.md` | `9ec2145eab6e999bcce22d350cf8fd6baf3f8a5d5da6550d387910ecd6133c9e` |
| `wiki/cards/bando1995-cluster-values.md` | `507fff3823e47ea893003ed2ec887de1e9b8b2c107ffdd35a5a514570c20d5d7` |
| `wiki/cards/bando1995-large-n-note.md` | `114108267408dcbcce044c9780d8f695049a759281a889171ceb525c403ed1d0` |
| `wiki/cards/bando1995-linear-stability.md` | `9373d6bd06979be539f18d21cc510c49dc59387a220e6bc415070881ec8ca4b2` |
| `wiki/cards/bando1995-no-delay.md` | `527e89639f6d403e14ea511d978df1332796f8ef9ab50ac895878d1b8c5cba27` |
| `wiki/cards/bando1995-ovm-equation.md` | `66d6c10c8dc13e5f787a7dc3c6464d37fed6eec208dcbf2f5b5e5ce747120153` |
| `wiki/cards/bando1995-spontaneous-jam.md` | `adfbc601430f51f481bc4d3ec65fb4fd27322212f65e7771950d051fd0f94afd` |
| `wiki/cards/bando1995-stable-regions.md` | `4341b82ffec1ec800591c1b601e789a5bee7f79bf169c9e491e3fee48f4cb0c4` |
| `wiki/cards/bando1995-velocity-function.md` | `6694d775771202064a8b0df7349917a5ca3a0ce3de7436ba8e6060b9848d3b1a` |
| `wiki/cards/nagel1992-bottleneck.md` | `390d63652f68e79d0b2b8154ada5e02aab636f56badf982f4ca908c566e5b366` |
| `wiki/cards/nagel1992-circle-jams.md` | `11d952d1a97abd63a048bcf2f91ead24b526f8440024687239a3efda7e1012f1` |
| `wiki/cards/nagel1992-randomization.md` | `228d143002bd566baf9e7241935de8a8d775a9bcb87c2f49896f820851cb521b` |
| `wiki/cards/nagel1992-real-units.md` | `187abaef28bcd048211ace931ff6e0e764b60916da8a9e29e52b4b80837eb63a` |
| `wiki/cards/nagel1992-rules.md` | `68e4f0053e2fc64fcd2880a4c7e9d4f911175b9207aba42013f46b4d9db7d276` |
| `wiki/cards/nagel1992-transition.md` | `cff003b1c465855d10ecfce4ef4043524886c790892d017344f0d735392cf392` |
| `wiki/cards/orosz2010-delays.md` | `d9c562f5d7016899e6905612496f9f7d6564253edca9b78ec99c8d61445a6bab` |
| `wiki/cards/orosz2010-ovm-family.md` | `3ec4021e1c01e64462dab467a21e4d8e9edff5b7e8138bbab6a567a2c61ea5c2` |
| `wiki/cards/orosz2010-stability-approaches.md` | `b18ce4b79567da3b13973d8bded3db23905c8854625c42c03db056ab44a8f317` |
| `wiki/cards/ours-finite-n-simulation.md` | `e1d21332119095e1f4a59e155db96bb56dc901156c9abc1e9e0f4ed327a3cc7c` |
| `wiki/cards/ours-finite-n-threshold.md` | `90ca47668742e4fe565927b43cc37d1f98be1ed44d5d5b1699839330d0a3de9a` |
| `wiki/cards/stern2018-controllers.md` | `780ebe4917f2ece75e94a36aab12cc86fc07fd48e87e8c1dbfb0b645e54c253f` |
| `wiki/cards/stern2018-results.md` | `6c646aa9374adaa18cac7c3ba626e3aafa5e5f6a0b8cc631e6afb8aab08ee946` |
| `wiki/cards/stern2018-setup.md` | `285eb37718f26659de9a323a779108245859ccf0e8f10f2fd935377cecf06e39` |
| `wiki/cards/stern2018-waves-emerge.md` | `2ec922b1026dc7c4571f94c520ac1f6788bfd9c1dc5671fab60c6abb7d1a0161` |
| `wiki/cards/sugiyama2008-23-vehicles.md` | `59a1918f28237f05d49bf2d6f87fa272f2f3b52c7a50b613110f5e667ee088d7` |
| `wiki/cards/sugiyama2008-backward-wave.md` | `7c805e9157bead59c55e004ae342ca3c8bd68059641fcb69f3790497aba6893c` |
| `wiki/cards/sugiyama2008-fundamental-diagram.md` | `5b4e275cf71d7576e7aa5c4f3c9f2528bab4cee02dd90d6e73286b61d9145e6d` |
| `wiki/cards/sugiyama2008-highway-comparison.md` | `1821b3ebdfa55608111d23ca1c8428c0ca89c1e5c94b5b79d19e6daf92b818b7` |
| `wiki/cards/sugiyama2008-jam-emerges.md` | `52ada92ad185baee982284c6d9c8e9f2a1583845612e089d18681b04ce4974ca` |
| `wiki/cards/sugiyama2008-mechanism.md` | `edc56ceed98ead16bc7064cfddb41d9f8e09df920594445a7091ddbaebb79288` |
| `wiki/cards/sugiyama2008-setup.md` | `b49e2bf508faee3154534651e6c9748f8172b5f0c1c5e2bcb9eb0af629c01e13` |
| `wiki/cards/tadaki2013-expressway-consistency.md` | `866f64c147f861e072a1f3ab8ee1e51b52539c88bd7dd22a9f2c480a63b31bd4` |
| `wiki/cards/tadaki2013-high-density.md` | `21a9268b67acebb561d6d5efedb9a79295bac2e0a297759bb32485de932c315e` |
| `wiki/cards/tadaki2013-metastable.md` | `1825a7fad619e863ce2625f04adac717afdd73c9fbeca4843b4117efab7a26eb` |
| `wiki/cards/tadaki2013-setup.md` | `f0fbf5b2b1ca5762eb2f3779d37198f4623035eb789df7e79d7d1cdb5e89cb3a` |
| `wiki/sources/bando1995.md` | `fa31a7abc9f7265f818f479dc4e92b4f7f7eb8d7806316324c2a75b94a47ecc6` |
| `wiki/sources/nagel1992.md` | `3b2d4e6facadd89f4e5ebf57a14cb67e586512eed18fa59690e7202db04c8825` |
| `wiki/sources/orosz2010.md` | `0ccdc9adeabfc3ff3f8c29794dae350fca93faf088587526e291e965aade7676` |
| `wiki/sources/stern2018.md` | `dddbab143c9aec53262e7ea21843b7ba4d94611dba23c8e6ec9b87fc29889e09` |
| `wiki/sources/tadaki2013.md` | `820a2f2c9cf91befb7078f6411b119c6ab4fd4a0ecbdec11e35876a30e988f1a` |
| `scripts/check_wiki.py` | `061d72bf287cf34bdbdec6841c1a6afd0cddd9aa7fe0776e25bb3731fb7e0563` |
| `scripts/build_index.py` | `01b8cfe88a6c14052e0cce286c17627f44b63240b5a4c59f6001f62f6fc72995` |
| `tests/test_check_wiki.py` | `2ffc9400dbc8bd4b9b9a7ac2d76e9fcf5d49d210cd01312a8fb7b34ccebd38f1` |
| `runs/logs/2026-11-12-index-generation-tests.log` | `12a32d97def37b04c8968142bc82b91bd8f26468db056ab4a0e842c9ba9f39ce` |
| `runs/logs/2026-11-12-index-generation-build-check.log` | `a62378e52df5f9f13a4c915a11b44e8ca7608ec5e9be459742fad13dbea13343` |
| `runs/logs/2026-11-12-strict-before-r4.log` | `87d51918846ca9d151727b1eeabfe4b73a1c9aed8c63d3e421ae43cd5cfdd70f` |

# 以下是要審查的Wiki內容



========== 檔案：wiki/cards/orosz2010-ring-stability.md ==========

---
id: orosz2010-ring-stability
type: model_theory
source: orosz2010
locator: 第4467頁第3段、第4475～4476頁附錄A式(A1)～(A8)
conditions: 一般的跟車模型，沒有反應延遲；環上N台車；F、G、H大於0
units: 保留物理量綱（F、G、H是有單位的係數）
status: confirmed
related: orosz2010-stability-approaches, ours-finite-n-threshold
---

## 主張

（這是綜述附錄裡的數學推導，所以類型是model_theory。）在沒有反應延遲的跟車模型裡，環上N台車時，非零的波各有穩定分界，k和N−k是一對共軛、共用同一條分界；N是偶數時k=N/2沒有有限的分界。N≥3時，越過分界時最先失去穩定的是k=1（和它的共軛N−1，最長的波）。固定均勻車距、讓N趨近無限多時，最先失穩的k=1的波數2π/N趨近0（長波），整體的穩定條件變成(A8)。

## 原文依據

第4475頁附錄A把式(5.1)在沒有延遲時寫成(A1)，用環上N台車的解得到(A3)，開N次方後回到(A2)，波數只能是(A4)的2kπ/N。第4476頁(A6)是第k個波穩定性改變的條件，作者說從F小往大越過分界時系統「更不穩定」，因此最先失去穩定的是k=1；N趨近無限大時條件變成(A8)。第4467頁也說，沒有延遲時穩定性會先在低頻、長波（k=1）失去。

> Consequently, the stability loss occurs for the lowest wavenumber

## 限制

- 這是一般模型的公式，用F、G、H表示。代入Bando的模型（W=0、車長0）得到22台車分界的那一步是我們做的，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。
- 只適用沒有延遲的情況，見[orosz2010-delays](orosz2010-delays.md)。
- (A6)含tan²(kπ/N)，k=N/2時發散，所以那個波沒有有限的Hopf分界；作者也寫只有k≤N/2的分界出現在F、G、H>0的範圍。
- 原文沒有寫車數下限。N=2時唯一非零的波就是k=N/2=1，沒有有限的分界，所以「k=1最先失穩」要N≥3才有意義；這個條件是我們從(A6)看出來的。


========== 檔案：wiki/cards/stern2018-wave-returns.md ==========

---
id: stern2018-wave-returns
type: experiment
source: stern2018
locator: 第9～10頁第4.2節（三場的設定和實驗A結果）、第11頁表2、第12頁實驗B、第13頁實驗C、第14頁圖5
conditions: 實驗A的目標速度由外部設定、逐步調整；實驗B由受訓駕駛照外部給的目標速度開，中途調高一次；實驗C的目標速度由控制器自己算，沒有外部參數
units: m/s、mph
status: confirmed
related: stern2018-results
---

## 主張

控制不是開了就一勞永逸。三場的控制方式和速度調整不一樣，要分開看：

- 實驗A（FollowerStopper控制器，目標速度由外部設定）：目標速度依序調成6.50、7.00、7.50、8.00 m/s。調到8.00 m/s時，控制車平均比車流快，又引發了波；調回7.50 m/s後波再次減弱；改回人開之後波又出現。
- 實驗B（受訓駕駛不靠自動化，照同樣的策略開，目標速度由外部觀察者給）：先用14 mph（6.25 m/s），之後調高到16 mph（7.15 m/s），調高後的車速標準差是這一場最低的；改回一般開法後，波又出現。
- 實驗C（PI控制器，目標速度由控制器自己算，實驗中沒有改任何外部參數）：控制消除了一開始的波，但控制期間又產生了第二個波，這個波也被減弱。

## 原文依據

第9～10頁第4.2節寫了三場的設定：實驗A在第126秒啟動FollowerStopper，目標6.50 m/s，之後在第222、292、347秒改成7.00、7.50、8.00 m/s，第415秒降回7.50 m/s，第463秒改回人開；實驗B在第112秒開始以14 mph控制，第202秒改成16 mph，維持98秒後回到一般開法；實驗C在第218秒啟動PI控制器到第413秒結束，控制器自己決定目標速度。第11頁表2列出實驗B各時段的車速標準差（14 mph時1.58、16 mph時1.19、關掉控制後2.25，單位m/s）。第10頁說實驗A在目標7.50 m/s時，控制車的速度幾乎剛好等於車流平均、不需要減速；調到8.00 m/s時平均比車流快，又引發了波，調回7.50 m/s後波再次被減弱（原文dampened），控制器關掉後波又出現。第12頁說實驗B的目標速度調到16 mph時車速標準差最低，回到一般駕駛後波又出現。第13頁說實驗C的控制消除了一開始的波，但控制期間又產生了一個波，第二個波也被減弱（原文damped）。

> which inevitably induces a wave again

## 限制

- 只有這幾場的觀察，沒有說明「目標速度要設多少」的一般規則。

## 教學說法

實驗A：目標速度接近車流平均時效果最好，調得比車流快，波又回來。實驗B也調高過目標速度，但調高後車速變動是那一場最低的，波是改回一般開法後才回來。實驗C的目標速度是控制器自己算的。所以「目標速度設得比車流快會把波帶回來」只有實驗A支持。


========== 檔案：wiki/cards/tadaki2013-critical-density.md ==========

---
id: tadaki2013-critical-density
type: experiment
source: tadaki2013
locator: 第6頁第3段、第8頁圖5～6、第9頁圖7、第10頁圖8、第10～11頁
conditions: 用第一天暖身場和第二天的資料；臨界密度由車速波動和基本圖估計，沒有用任何模型
units: 台/m、台
status: confirmed
related: tadaki2013-density-dependence, tadaki2013-metastable, tadaki2013-expressway-consistency
---

## 主張

在作者選用的場次裡，25台以下時，車速的波動小、流量隨密度增加，是順暢的自由流；28台以上時，車速波動變大、出現塞車，大部分場次的基本圖點會散開。作者據此估臨界密度在每公尺0.08台（25台）到0.09台（28台）之間。例外是2030和2934兩場：塞車團裡有停止或幾乎停止的車，基本圖另列在圖8。因為只在定點記錄通過的車，依定點通過資料繪出的基本圖接近自由流。

## 原文依據

第6頁用每一場的平均車速和標準差（圖5）判斷：第二天28到34台的場次車速波動很大，代表有塞車。第9頁圖7分開畫自由流和塞車的基本圖。第10～11頁的結論是N≤25時是自由流、N≥28時出現塞車，臨界密度在0.08和0.09之間（單位每公尺）。

> the drivers were extremely cautious on the first day and did not appear to drive at the desired speed

（這句是第6頁說明為什麼大部分第一天的資料不用。）

## 限制

- 26、27台沒有做，所以只能說臨界值在25和28台之間。
- 第一天的資料大多被排除，理由是駕駛太小心。
- 基本圖是在環道上三個定點量的，停住的車不會被算進流量和平均速度。塞車團裡有停止或幾乎停止的車的場次，依定點通過資料繪出的基本圖接近自由流；但平均速度略低、波動比真正的自由流（圖7(a)）大，因為資料也包含追上和離開塞車團的車（第10頁）。


========== 檔案：wiki/cards/tadaki2013-density-dependence.md ==========

---
id: tadaki2013-density-dependence
type: experiment
source: tadaki2013
locator: 第6頁第1段、第7頁圖4、附錄B～C
conditions: 314公尺環道；圖4是第二天25、30、34台三場
units: 台、km/h
status: confirmed
related: tadaki2013-setup, tadaki2013-critical-density, sugiyama2008-backward-wave
---

## 主張

25台時所有車都順順地開，密度雖有波動但沒有變成塞車；30台時出現走走停停，停住或幾乎停住的車團以約20 km/h往後移動；34台時則是慢速的塞車團時而出現、時而消失。整體來看，車少時維持順暢、車多時出現塞車。

## 原文依據

第6頁描述圖4的三個時空圖：25台（場次2125）全部順暢；30台（場次2030）有停停走走、車團以約20 km/h往後移動，跟高速公路上的速度差不多；34台（場次2534）慢速的塞車團出現又消失。附錄B、C列出的場次可以查到時空圖（表1的1110沒有出現在附錄裡）。

> these show that jammed flow occurs in high density conditions while free flow is maintained at low density

## 限制

- 圖4只各挑一場當例子。第二天同車數的其他場次在附錄B；第一天的25台（1625）和30台（1730）有放進第6頁圖5的兩天比較，但沒有納入之後用來估計臨界密度的選定資料；時空圖在附錄C，附錄E也有第一天場次的基本圖。作者沒有對重複場次做統計比較。
- 約20 km/h跟Sugiyama 2008的數字相同，是同一群作者在不同場地量到的。


========== 檔案：wiki/glossary.md ==========

# 術語對照

全專案統一用這裡的譯名。簡報第一次出現時寫「中文（英文）」，之後用中文或縮寫。

| 中文 | 英文 | 其他常見譯名 | 出處或說明 |
|---|---|---|---|
| 幽靈塞車 | Phantom Traffic Jam | 待查 | 暫定，ingest時查可靠的繁體中文用法再確認 |
| 自由流 | free flow | — | sugiyama2008第2～3頁；所有車用差不多的速度、保持安全距離前進 |
| 塞車團 | jam cluster | 阻塞團、壅塞團 | sugiyama2008第5頁；暫定譯名，待查繁體中文學術用法 |
| 走走停停波 | stop-and-go wave | 停走波 | sugiyama2008第4頁；暫定譯名，待查 |
| 瓶頸 | bottleneck | — | sugiyama2008第2頁；例如匝道、隧道、上坡 |
| 臨界密度 | critical density | — | sugiyama2008第2～3頁 |
| 基本圖 | fundamental diagram | 流量密度圖 | sugiyama2008第2頁；密度和流量的關係圖；暫定，待查台灣交通工程用法 |
| 車頭間距 | headway distance | 車距、車頭距 | sugiyama2008第4頁；這裡指距離，不是時間；暫定，待查 |
| 最佳速度模型 | Optimal Velocity Model, OVM | — | bando1995提出，但原文把V叫legal velocity function；OVM這個名稱是後來文獻用的（例如Orosz 2010、Tadaki 2013） |
| 最佳速度函數 | optimal velocity function | 合法速度函數（直譯legal velocity function） | bando1995第1036頁；只看前車距離的「想開的速度」 |
| 敏感度 | sensitivity | — | bando1995第1036頁的a；不是反應時間 |
| 均勻車流 | steady state flow, uniform flow | 穩態流 | bando1995第1036頁；所有車等距等速 |
| 線性穩定性分析 | linear stability analysis | — | bando1995第1036～1037頁 |
| 週期邊界條件 | periodic boundary condition | — | bando1995第1036頁；第N+1台就是第1台，等於環狀道路 |
| 細胞自動機 | cellular automaton | 元胞自動機 | nagel1992第2221頁；把空間和時間切成格子、照規則更新的模型；暫定，待查繁體中文常用譯名 |
| 同時更新 | parallel update | 平行更新 | nagel1992第2227頁；每一步所有車一起照規則移動，一般NaSch模型用這種 |
| 隨機逐車更新 | random sequential update | 隨機序列更新 | nagel1992第2227頁；每次隨機挑一台車更新；暫定譯名 |
| NaSch模型 | Nagel–Schreckenberg model | — | 指nagel1992提出的模型；這個簡稱是後來文獻的叫法 |
| 隨機減速 | randomization | 隨機化 | nagel1992第2222頁第3步；暫定譯名 |
| 介穩態 | metastable state | 亞穩態 | tadaki2013第10頁；同一個密度下兩種狀態都可能出現；台灣物理學常用「介穩態」，待確認 |
| 相變 | phase transition | 相轉變 | sugiyama2008第3、7頁、tadaki2013第11頁；兩篇都用相變描述自由流變成塞車流：Sugiyama說是非平衡系統的相變，Tadaki說是動態相變，並說轉變似乎是一階 |
| 反應延遲 | reaction time, delay | 反應時間 | orosz2010第4462頁；Bando 1995沒有加 |
| 跟車模型 | car-following model | — | orosz2010第4461頁；每台車看前車決定怎麼開的模型 |
| 自動駕駛車 | autonomous vehicle, AV | 自駕車 | stern2018；這篇的車只有速度自動控制，方向盤由人操作 |
| 平滑車 | — | — | 我們簡報裡自己取的名字，指「照平均速度穩定開的那台車」，不是論文用語 |


========== 檔案：wiki/index.md ==========

# 幽靈塞車Wiki索引

這份Wiki整理「沒有事故為什麼也會塞車」的研究，是教學簡報的知識來源。

下面的文獻表和證據卡清單是`scripts/build_index.py`從文獻檔和證據卡產生的，不要手改；改了文獻檔或證據卡就重跑它，`scripts/check_wiki.py`會檢查有沒有同步。這段說明和導覽是人工寫的。

- 術語：[glossary.md](glossary.md)
- 研究差異與未解問題：[disputes.md](disputes.md)
- 簡報頁面和證據卡的對照：[slide-map.md](slide-map.md)
- 我們自己的推導：[derivations/finite-n-threshold.md](derivations/finite-n-threshold.md)

<!-- 以下由scripts/build_index.py從wiki/sources和wiki/cards產生，不要手改；改了文獻檔或證據卡就重跑 -->

## 文獻

| id | 種類 | 閱讀狀態 | 檔案 |
|---|---|---|---|
| bando1995 | paper | 全文已讀 | [sources/bando1995.md](sources/bando1995.md) |
| nagel1992 | paper | 全文已讀 | [sources/nagel1992.md](sources/nagel1992.md) |
| orosz2010 | paper | 部分章節 | [sources/orosz2010.md](sources/orosz2010.md) |
| stern2018 | paper | 全文已讀 | [sources/stern2018.md](sources/stern2018.md) |
| sugiyama2008 | paper | 全文已讀 | [sources/sugiyama2008.md](sources/sugiyama2008.md) |
| tadaki2013 | paper | 全文已讀 | [sources/tadaki2013.md](sources/tadaki2013.md) |

## 證據卡

共39張。每張的條件取自卡片的conditions欄位，主張直接取自卡片的「## 主張」，都沒有另外縮寫；原文依據和限制請點進卡片看。

### bando1995

#### [bando1995-capacity](cards/bando1995-capacity.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：N=100、L=200的模擬；運輸量用N/T估算（T是一台車跑完一圈的時間）

在這組條件下，用模擬估出的「有塞車時」通過量，和用均勻車流解直接算出的通過量，都約0.48；作者覺得奇怪，說會在之後的論文討論。兩個數字的取得方式不同：前者來自模擬裡一台車跑一圈的時間，後者是公式計算。

#### [bando1995-cluster-values](cards/bando1995-cluster-values.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：同bando1995-spontaneous-jam的模擬條件；數值是作者從最後100步的分布讀出來的

塞車形成之後，塞車團裡的車距約0.32、速度約0.03（幾乎停住）；團外的車距約3.68、速度約1.88。以車距小於2界定擁擠區時，100台車裡有50台在擁擠區。作者把模擬分成三個階段：前50步符合線性分析，50～400步看起來很亂，400步之後慢慢穩定下來。

#### [bando1995-large-n-note](cards/bando1995-large-n-note.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：作者對環狀道路邊界條件的說明

作者說，只要車數和環長夠大，環狀道路這個邊界條件對分析和模擬都不重要；邊界條件的詳細影響留到之後的論文。

#### [bando1995-linear-stability](cards/bando1995-linear-stability.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：跟bando1995-ovm-equation相同；只看均勻車流附近很小的擾動（線性化）

線性穩定性分析是判斷一點小變化會慢慢消失、還是越來越嚴重的方法。在均勻車流上加很小的擾動，把擾動拆成一個一個的波（第k個波的α_k=2πk/N）來看會不會變大。作者得到的總結（式(12)）是：速度函數在均勻車距的斜率V'(b)小於a/2時穩定，大於a/2時不穩定；在這個跟車方程式裡，換成別的速度函數V也適用。這個a/2是長波極限（車數很多）的分界；車數有限的環道，要依式(9)(11)逐一檢查那幾個非零的波，見[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)。

#### [bando1995-no-delay](cards/bando1995-no-delay.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：作者對模型設計的說明

這個模型刻意沒有加入駕駛的反應延遲。作者認為，因為模型寫的是加速度（二階方程式），本身就隱含了「速度跟不上變化」的效果，不需要另外加延遲時間。

#### [bando1995-ovm-equation](cards/bando1995-ovm-equation.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：單車道環狀道路，N台車、環長L，所有駕駛敏感度a相同，沒有反應延遲

每台車的加速度由「它想開的速度」和「現在的速度」的差決定：想開的速度V只看自己到前車的距離，差距乘上敏感度a就是加速度。所有車等距、等速的均勻車流（每台車的速度和間距都一樣；車距b=L/N、速度V(b)）一定是這個方程式的一個解。

#### [bando1995-spontaneous-jam](cards/bando1995-spontaneous-jam.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：模擬，不是實驗；N=100、L=200（車距2）、a=1、V=tanh(Δx−2)+tanh2；初始位置幾乎等距，第1台車往前偏0.1，所有車的初速都是0（式(19)）

在模擬裡，100台車的初始位置幾乎等距，只有第1台往前移0.1，所有車從靜止（初速0）開始，之後車流自己分成幾段幾乎停住的塞車和幾段快速前進的車，最後形成5團塞車；這些塞車團都以相同的速度慢慢往後移動。

#### [bando1995-stable-regions](cards/bando1995-stable-regions.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：V=tanh(Δx−2)+tanh2、a=1；圖10是示意圖

在這篇的模型和參數條件下，在速度函數的曲線上，車距很小和車距很大的地方都是穩定區，只有中間一段是不穩定區。均勻車距落在不穩定區時，車子會被推往兩邊的穩定區，一部分擠成塞車、一部分拉開跑快。

#### [bando1995-velocity-function](cards/bando1995-velocity-function.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：無因次；a=1

作者先試了最簡單的速度函數V=tanh(Δx)，結果在不穩定時會有車往後倒退，等於撞車。所以改用V(Δx)=tanh(Δx−2)+tanh2：車距是0時目標速度V(0)是0（實際速度還是由加速度方程式決定）。作者說在這個模型的模擬裡，駕駛會慢慢加減速、不會超過前車。

### nagel1992

#### [nagel1992-bottleneck](cards/nagel1992-bottleneck.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：開放道路：左端只要空著就放進一台速度0的車（代表兩線道併成一線道的瓶頸），右端最後6格把車刪掉；長度最多10000格、最多5×10^6步

在模擬的瓶頸情境（開放邊界）下，車流自己穩定在密度約每格0.069台、流量約每步0.304台的狀態。圖6把這個點畫在環道模擬的基本圖上，它低於環道基本圖的最大流量；作者也說在v_max=1、而且用隨機逐車更新（不是一般NaSch的同時更新）的特例裡，系統會自己走到最大流量，但v_max較大時看起來不是這樣。

#### [nagel1992-circle-jams](cards/nagel1992-circle-jams.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：環狀道路（週期邊界）、v_max=5；圖1密度0.03、圖2密度0.1（每格的車數）

模擬裡，密度低（每格0.03台）時車流順暢；密度較高（每格0.1台）時，車速的隨機變動會讓一小團一小團的塞車隨機出現，塞車團往後移動，車子開進去停一下、再從前端加速離開，像高速公路上的走走停停波。

#### [nagel1992-randomization](cards/nagel1992-randomization.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：同nagel1992-rules

作者說第3步的隨機減速是讓模擬像真實交通的關鍵，它代表人的行為或外在條件造成的速度變動；如果沒有這一步，模型完全確定，任何初始狀態都會很快變成一個固定、每步往後移一格的樣子。

#### [nagel1992-real-units](cards/nagel1992-real-units.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：作者用幾種粗略的方法把模型換算成真實單位；高速公路的數字是作者引用的量測值

作者把一格換算成7.5公尺（塞車時一台車佔的長度），並用幾種方法估算一個時間步大約是0.5到1秒的量級（其中一個數字原文印為0.7秒，但照它列的算式是0.54秒），結論是時間步的數量級是「秒」。其中一種方法用了高速公路上量到的塞車波往後速度約15 km/h。

#### [nagel1992-rules](cards/nagel1992-rules.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：單車道，道路切成格子，每格最多一台車；所有車同時更新

每一步，每台車依序做4件事：1. 還沒到最高速、前面空間夠，就加速1；2. 前車太近，就減到不會撞上的速度；3. 速度大於0的車，以機率p隨機減速1；4. 照速度往前走。

#### [nagel1992-transition](cards/nagel1992-transition.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：環狀道路、v_max=5；長時間平均；系統長度L=10^4格（圖4）

這個模型的基本圖上，大約在密度每格0.08台附近看得到從順暢到塞車的轉變；另外，基本圖流量最大值的位置和形狀會隨系統大小改變。作者說從這些圖看不出確切的轉變點在哪。

### orosz2010

#### [orosz2010-delays](cards/orosz2010-delays.md)

- 類型：review
- 狀態：confirmed
- 條件：有反應延遲的跟車模型

作者指出，如果駕駛的反應延遲夠大，均勻車流可能改在短的波（高頻）失去穩定，不再是最長的波；延遲再大，連駕駛想減小擾動的努力都可能失效。

#### [orosz2010-ovm-family](cards/orosz2010-ovm-family.md)

- 類型：review
- 狀態：confirmed
- 條件：單車道、車子一樣長、駕駛相同；綜述整理

在Orosz等人的整理裡，動態跟車模型把加速度寫成車距、車距變化和自己速度的函數，可以有反應延遲；OV模型是其中一類，加速度＝（想開的速度－現在速度）÷T，再加一項看相對速度的W。作者說，延遲全部設為0的做法就是Bando 1995用的。

#### [orosz2010-ring-stability](cards/orosz2010-ring-stability.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：一般的跟車模型，沒有反應延遲；環上N台車；F、G、H大於0

（這是綜述附錄裡的數學推導，所以類型是model_theory。）在沒有反應延遲的跟車模型裡，環上N台車時，非零的波各有穩定分界，k和N−k是一對共軛、共用同一條分界；N是偶數時k=N/2沒有有限的分界。N≥3時，越過分界時最先失去穩定的是k=1（和它的共軛N−1，最長的波）。固定均勻車距、讓N趨近無限多時，最先失穩的k=1的波數2π/N趨近0（長波），整體的穩定條件變成(A8)。

#### [orosz2010-stability-approaches](cards/orosz2010-stability-approaches.md)

- 類型：review
- 狀態：confirmed
- 條件：均勻車流附近的小擾動（線性化）

分析均勻車流穩不穩定，文獻裡有三種做法：假設無限長道路上的波、看環上N台車、或看一排車的訊號會不會一台傳一台放大。作者說三種做法得到相同的結果，並在附錄用沒有延遲的情況示範：環上N台車的條件保留N和離散的波數，車數趨近無限多（均勻車距固定）時，跟看一排車的條件取最小值時一致。均勻車流失去穩定時，會出現行進的波。

### stern2018

#### [stern2018-controllers](cards/stern2018-controllers.md)

- 類型：experiment
- 狀態：confirmed
- 條件：自動控制器用那台車自己量到的速度、跟前車的距離，以及從距離變化估出的前車速度；實驗A和B另外有外部給的目標速度

三種控制方式（實驗A的FollowerStopper、實驗B由受過訓練的人照同類策略開、實驗C的PI控制器）的共同想法是：那台車照著車流的平均速度開，而不是跟著前車忽快忽慢。前車加速時讓空隙變大、前車減速時把空隙吃掉，同樣的時間走同樣的距離，但加速和煞車少很多；距離太近時一定以安全為先。

#### [stern2018-results](cards/stern2018-results.md)

- 類型：experiment
- 狀態：confirmed
- 條件：比較「第一次出現波、沒有控制」和「控制開啟中表現最好」的時段（A、B有好幾段控制時段，取最好的一段；C只有一段）；每種控制器一場

三場實驗打開控制後，車隊整體的車速標準差（把所有車和那段時間合在一起算的一個數字）都下降（A降80.8%、B降49.5%、C降54.7%），油耗下降（42.5%、22.1%、28.1%），過度煞車事件（第4.1節定義）大幅減少；通過量A增加14.1%、B增加9.8%，但C減少2.5%。

#### [stern2018-setup](cards/stern2018-setup.md)

- 類型：experiment
- 狀態：confirmed
- 條件：單車道環道；21～22台車；只有一台車的速度可以自動控制

實驗在周長260公尺的單車道環道進行，21～22台車，其中一台是可以自動控制速度的車；其他駕駛被要求像尖峰時段那樣開：前方空隙拉大時要追上，同時保持安全、禁止貼車，目的是不讓他們自己把波消掉。那台控制車為了方便緊急閃避，行駛半徑往外偏半個車寬。

#### [stern2018-wave-returns](cards/stern2018-wave-returns.md)

- 類型：experiment
- 狀態：confirmed
- 條件：實驗A的目標速度由外部設定、逐步調整；實驗B由受訓駕駛照外部給的目標速度開，中途調高一次；實驗C的目標速度由控制器自己算，沒有外部參數

控制不是開了就一勞永逸。三場的控制方式和速度調整不一樣，要分開看：

- 實驗A（FollowerStopper控制器，目標速度由外部設定）：目標速度依序調成6.50、7.00、7.50、8.00 m/s。調到8.00 m/s時，控制車平均比車流快，又引發了波；調回7.50 m/s後波再次減弱；改回人開之後波又出現。
- 實驗B（受訓駕駛不靠自動化，照同樣的策略開，目標速度由外部觀察者給）：先用14 mph（6.25 m/s），之後調高到16 mph（7.15 m/s），調高後的車速標準差是這一場最低的；改回一般開法後，波又出現。
- 實驗C（PI控制器，目標速度由控制器自己算，實驗中沒有改任何外部參數）：控制消除了一開始的波，但控制期間又產生了第二個波，這個波也被減弱。

#### [stern2018-waves-emerge](cards/stern2018-waves-emerge.md)

- 類型：experiment
- 狀態：confirmed
- 條件：所有車都由人開的時段

三場實驗在全部由人開的時候都出現了走走停停波：實驗A在第79秒、實驗B在第55秒、實驗C在第161秒看到第一個波。

### sugiyama2008

#### [sugiyama2008-23-vehicles](cards/sugiyama2008-23-vehicles.md)

- 類型：experiment
- 狀態：confirmed
- 條件：同一個230公尺環道，車數23台

作者做過不同車數的實驗，文中只提到23台的結果：也形成了塞車團，速度跟22台時一樣。

#### [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)

- 類型：experiment
- 狀態：confirmed
- 條件：同sugiyama2008-setup的條件；速度是從360度攝影機的影片讀出的軌跡估算

塞車團往跟車子相反的方向移動，速度大約20 km/h，而且大小和速度維持不變。團裡的車完全停下，團外的車約40 km/h；前端的車加速離開，後面又有車加入，所以塞車團一直在，但裡面的車一直在換。

#### [sugiyama2008-fundamental-diagram](cards/sugiyama2008-fundamental-diagram.md)

- 類型：experiment
- 狀態：confirmed
- 條件：日本某條高速公路單一地點一個月的資料，由當時的日本道路公團量測

把高速公路上的車流密度和流量畫成圖（基本圖；圖1畫的是密度和流量的關係），資料點在臨界密度附近明顯分成兩群：自由流和擁擠車流。圖1這個地點的臨界密度約每公里25台。

#### [sugiyama2008-highway-comparison](cards/sugiyama2008-highway-comparison.md)

- 類型：experiment
- 狀態：confirmed
- 條件：作者拿其他研究的高速公路資料比較；圖5的軌跡是從Treiterer和Myers 1974的圖描下來的，原始空拍是1967年

作者表示，實驗裡塞車團往後退的速度（約20 km/h）跟真實高速公路上量到的塞車往後傳的速度差不多，並用1967年高速公路空拍描出的車輛軌跡（圖5）來比較。

#### [sugiyama2008-jam-emerges](cards/sugiyama2008-jam-emerges.md)

- 類型：experiment
- 狀態：confirmed
- 條件：同sugiyama2008-setup的條件（230公尺、22台車）

一開始均勻的車流維持了一段時間，之後車距出現小小的波動並逐漸變大，最後有幾台車被迫完全停下，形成走走停停。圖3的第二張照片是開始3分鐘後拍的，那時已經有一團5台車的塞車。

#### [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md)

- 類型：model_theory
- 狀態：confirmed
- 條件：作者依自己的交通流模型（引用參考文獻[2]～[4]）做的解釋，不是這個實驗直接量到的

這篇裡有三種不同層次的說法，要分開看：一是作者對模型的說明，模型在一開始是自由流、平均密度略高於某個臨界值時，能在沒有瓶頸的環道上產生塞車，機制是小波動在密度低時消失、超過臨界值時長大；二是環道實驗的觀察，在他們選的車數下，沒有瓶頸也出現了塞車；三是作者對瓶頸的解釋，瓶頸只是讓密度超過臨界值的觸發，不是塞車的根本原因。

#### [sugiyama2008-setup](cards/sugiyama2008-setup.md)

- 類型：experiment
- 狀態：confirmed
- 條件：平坦地面、單一車道的環形道路；車數事先用模型估過，刻意放在不穩定的範圍

實驗用周長230公尺的環形道路放22台車，開始前讓車子以約30 km/h、間距大致均勻地繞圈；之後駕駛只被要求安全跟前車、盡量維持巡航速度。

### tadaki2013

#### [tadaki2013-critical-density](cards/tadaki2013-critical-density.md)

- 類型：experiment
- 狀態：confirmed
- 條件：用第一天暖身場和第二天的資料；臨界密度由車速波動和基本圖估計，沒有用任何模型

在作者選用的場次裡，25台以下時，車速的波動小、流量隨密度增加，是順暢的自由流；28台以上時，車速波動變大、出現塞車，大部分場次的基本圖點會散開。作者據此估臨界密度在每公尺0.08台（25台）到0.09台（28台）之間。例外是2030和2934兩場：塞車團裡有停止或幾乎停止的車，基本圖另列在圖8。因為只在定點記錄通過的車，依定點通過資料繪出的基本圖接近自由流。

#### [tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md)

- 類型：experiment
- 狀態：confirmed
- 條件：314公尺環道；圖4是第二天25、30、34台三場

25台時所有車都順順地開，密度雖有波動但沒有變成塞車；30台時出現走走停停，停住或幾乎停住的車團以約20 km/h往後移動；34台時則是慢速的塞車團時而出現、時而消失。整體來看，車少時維持順暢、車多時出現塞車。

#### [tadaki2013-expressway-consistency](cards/tadaki2013-expressway-consistency.md)

- 類型：experiment
- 狀態：confirmed
- 條件：高速公路的數字是第11頁的敘述，引用參考文獻[9]（Sugiyama 2008）；約每公里25台可在第3頁圖1和Sugiyama 2008第3頁圖1（東名高速公路資料）核對，約120 km/h只出現在第11頁的敘述；比較方法是作者的粗略論證

作者說，高速公路自由流平均約120 km/h、臨界密度約每公里25台；實驗自由流約40 km/h（這是第10頁對圖7(a)自由流資料擬合二次曲線aρ − bρ²得到的係數a，不是直接量的平均車速）、臨界密度每公尺0.08～0.09台。作者用「車速快三倍，需要的車距也大約大三倍」的粗略比例，認為兩者一致。

#### [tadaki2013-high-density](cards/tadaki2013-high-density.md)

- 類型：experiment
- 狀態：confirmed
- 條件：40台那一場（場次1940），是第一天的場次；有列入兩天車速和波動的圖5和第12頁的討論，但沒有納入用來估計臨界密度的選定資料

40台那一場的車速波動非常小，時空圖上車流是均勻的。作者提到有些理論模型預測密度高到一定程度時均勻車流又會變穩定，但說目前還不清楚這場觀察到的是不是那種情況。

#### [tadaki2013-metastable](cards/tadaki2013-metastable.md)

- 類型：experiment
- 狀態：confirmed
- 條件：圖7(c)用的是第二天2228、2328（28台）和2830（30台）三場；另一場30台的2030另列在圖8

圖7(c)的三場（28台兩場、30台一場）裡，基本圖上同一個密度附近同時有自由流和塞車兩種點，作者據此判讀出現了介穩態。

#### [tadaki2013-setup](cards/tadaki2013-setup.md)

- 類型：experiment
- 狀態：confirmed
- 條件：室內平地環道；同款車；大學生駕駛；目標速度30 km/h

實驗在名古屋巨蛋周長314公尺的室內環道進行，兩天共19場，每場10到40台同款的車，由52位大學生輪流開，被要求用自己的方式安全地以約30 km/h行駛；車的位置用雷射掃描器大約每0.2秒量一次。

### 我們自己的推導和模擬

#### [ours-finite-n-simulation](cards/ours-finite-n-simulation.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：V=tanh(Δx−2)+tanh2；N=22；車距2和2.5；RK4，時間步長0.05；只激發k=1的小擾動

用模擬量出22台車的分界：車距2時量到1.95966（公式1.95949），車距2.5時量到1.54126（公式1.54104）。a=1.98時，照a/2條件應該不穩定，模擬裡擾動卻是衰減的。

#### [ours-finite-n-threshold](cards/ours-finite-n-threshold.md)

- 類型：our_derivation
- 狀態：confirmed
- 條件：bando1995的模型；環狀道路N台車，N≥3；只看很小的擾動

車數有限時，非零的第k個波只有在a < 2V'(b)cos²(πk/N)時才會變大（k=0是整體平移，不算；k和N−k是一對共軛，分界相同；N是偶數時k=N/2要直接用式(10)，它在a>0、V'(b)>0時不會失穩）。N≥3時，a往下調時最先變不穩定的是k=1這一對，所以N台車的實際分界是a = 2V'(b)cos²(π/N) = V'(b)(1+cos(2π/N))。22台車、車距2時是1.9595，不是a/2條件給的2；車距b固定、車數越多（環長跟著變長），越接近2V'(b)。

<!-- 自動產生結束 -->


========== 檔案：wiki/sources/sugiyama2008.md ==========

---
id: sugiyama2008
kind: paper
authors: Yuki Sugiyama, Minoru Fukui, Macoto Kikuchi, Katsuya Hasebe, Akihiro Nakayama, Katsuhiro Nishinari, Shin-ichi Tadaki, Satoshi Yukawa
year: 2008
title: Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam
venue: New Journal of Physics 10, 033001 (7pp)
doi: 10.1088/1367-2630/10/3/033001
url: https://doi.org/10.1088/1367-2630/10/3/033001
read_status: 全文已讀
read_scope: 期刊第1～7頁全文、圖1～5和圖說、腳註11～15、參考文獻；兩段補充影片沒有看
independent: 是
---

## 這篇在做什麼

在沒有紅綠燈、沒有障礙物的環形道路上放22台車，讓駕駛照平常的方式跟車。研究人員想確認：即使沒有路口、事故或道路瓶頸，車子彼此的跟車行為，是否仍可能讓塞車自己形成。實驗確實觀察到了這個現象。這是一篇很短的實驗報告（7頁），沒有寫出模型方程式，模型的部分引用他們自己1995年的論文（參考文獻[4]、[12]）。

頁碼用期刊本身印的頁碼（第1～7頁）。大阪大學典藏庫的PDF前面有兩張前置頁（典藏庫封面和出版商的頁面），PDF頁碼比期刊頁碼多2。

## 研究條件

- 平坦地面、單一車道的環形道路，周長230公尺，22台車，中間架一台360度攝影機量測（第4頁、圖2）。
- 車數是先用模型估過、刻意讓密度落在「均勻車流會不穩定」的範圍（第4頁）。
- 開始前讓車子以約30 km/h等速、間距大致均勻地繞；之後駕駛只被要求安全跟前車、盡量維持巡航速度（第4頁）。
- 作者自己說這個速度以平均車距來看偏快，是為了滿足不穩定條件才這樣設定（第4頁）。
- 也做過不同車數的實驗，但文中只提到23台的結果（第5頁）。
- 沒有寫駕駛是誰、做了幾次、每次的差異，也沒有統計分析。

## 主要結果

- 實驗設定：[cards/sugiyama2008-setup.md](../cards/sugiyama2008-setup.md)
- 均勻車流自己變成塞車：[cards/sugiyama2008-jam-emerges.md](../cards/sugiyama2008-jam-emerges.md)
- 塞車團往後傳、速度約20 km/h：[cards/sugiyama2008-backward-wave.md](../cards/sugiyama2008-backward-wave.md)
- 作者拿高速公路資料比較：[cards/sugiyama2008-highway-comparison.md](../cards/sugiyama2008-highway-comparison.md)
- 23台車也塞：[cards/sugiyama2008-23-vehicles.md](../cards/sugiyama2008-23-vehicles.md)
- 作者對機制的解釋：[cards/sugiyama2008-mechanism.md](../cards/sugiyama2008-mechanism.md)
- 高速公路的基本圖（用圖表示車流密度和通過車輛數之間的關係）：[cards/sugiyama2008-fundamental-diagram.md](../cards/sugiyama2008-fundamental-diagram.md)

## 限制

- 只有一個場地、一種車數設定的詳細結果，沒有重複次數和統計。作者在腳註15說更詳細的結果和不穩定的密度範圍會在之後的論文發表，但沒有指名是哪一篇。Tadaki 2013第3頁說自己是先前環道實驗的延伸，不過無法確認腳註當時指的就是它。
- 數字的性質要分開看：230公尺、22台是實驗設定（第4頁）；約30 km/h是開始前調好的巡航速度，也是要求駕駛的速度（第4頁）；團外車速約40 km/h、塞車團約20 km/h往後是觀察到的約略值（第5頁，原文roughly），第6頁圖4的車輛軌跡上也標了約20 km/h。
- 「瓶頸只是觸發、不是塞車的根本原因」是作者依自己的模型做的解釋，實驗本身支持的是「沒有瓶頸也可能塞車」。文中也引用了Kerner的研究（參考文獻[3]、[8]），我們只能確認有引用，Kerner的具體立場還沒讀，見[disputes.md](../disputes.md)。
- 文中沒有寫出模型方程式和穩定條件，要另外從模型的原始論文確認。

## ingest紀錄

- [runs/2026-11-11-n1-sugiyama2008-r1.md](../../runs/2026-11-11-n1-sugiyama2008-r1.md)


========== 附錄：沒改過的檔案，只放開頭欄位和主張（只用來核對index.md） ==========



---------- wiki/cards/bando1995-capacity.md ----------

---
id: bando1995-capacity
type: model_theory
source: bando1995
locator: 第1041頁式(25)(26)
conditions: N=100、L=200的模擬；運輸量用N/T估算（T是一台車跑完一圈的時間）
units: 無因次
status: confirmed
related: bando1995-spontaneous-jam
---

## 主張

在這組條件下，用模擬估出的「有塞車時」通過量，和用均勻車流解直接算出的通過量，都約0.48；作者覺得奇怪，說會在之後的論文討論。兩個數字的取得方式不同：前者來自模擬裡一台車跑一圈的時間，後者是公式計算。


---------- wiki/cards/bando1995-cluster-values.md ----------

---
id: bando1995-cluster-values
type: model_theory
source: bando1995
locator: 第1040頁圖7～8和右欄、第1041頁圖9
conditions: 同bando1995-spontaneous-jam的模擬條件；數值是作者從最後100步的分布讀出來的
units: 無因次
status: confirmed
related: bando1995-spontaneous-jam, bando1995-stable-regions
---

## 主張

塞車形成之後，塞車團裡的車距約0.32、速度約0.03（幾乎停住）；團外的車距約3.68、速度約1.88。以車距小於2界定擁擠區時，100台車裡有50台在擁擠區。作者把模擬分成三個階段：前50步符合線性分析，50～400步看起來很亂，400步之後慢慢穩定下來。


---------- wiki/cards/bando1995-large-n-note.md ----------

---
id: bando1995-large-n-note
type: model_theory
source: bando1995
locator: 第1036頁左欄第2段
conditions: 作者對環狀道路邊界條件的說明
units: 無數值
status: confirmed
related: ours-finite-n-threshold
---

## 主張

作者說，只要車數和環長夠大，環狀道路這個邊界條件對分析和模擬都不重要；邊界條件的詳細影響留到之後的論文。


---------- wiki/cards/bando1995-linear-stability.md ----------

---
id: bando1995-linear-stability
type: model_theory
source: bando1995
locator: 第1036～1037頁式(5)～(12)、圖1
conditions: 跟bando1995-ovm-equation相同；只看均勻車流附近很小的擾動（線性化）
units: 無因次
status: confirmed
related: bando1995-ovm-equation, ours-finite-n-threshold
---

## 主張

線性穩定性分析是判斷一點小變化會慢慢消失、還是越來越嚴重的方法。在均勻車流上加很小的擾動，把擾動拆成一個一個的波（第k個波的α_k=2πk/N）來看會不會變大。作者得到的總結（式(12)）是：速度函數在均勻車距的斜率V'(b)小於a/2時穩定，大於a/2時不穩定；在這個跟車方程式裡，換成別的速度函數V也適用。這個a/2是長波極限（車數很多）的分界；車數有限的環道，要依式(9)(11)逐一檢查那幾個非零的波，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。


---------- wiki/cards/bando1995-no-delay.md ----------

---
id: bando1995-no-delay
type: model_theory
source: bando1995
locator: 第1035頁右欄、第1042頁右欄
conditions: 作者對模型設計的說明
units: 無數值
status: confirmed
related: bando1995-ovm-equation
---

## 主張

這個模型刻意沒有加入駕駛的反應延遲。作者認為，因為模型寫的是加速度（二階方程式），本身就隱含了「速度跟不上變化」的效果，不需要另外加延遲時間。


---------- wiki/cards/bando1995-ovm-equation.md ----------

---
id: bando1995-ovm-equation
type: model_theory
source: bando1995
locator: 第1036頁式(1)～(4)
conditions: 單車道環狀道路，N台車、環長L，所有駕駛敏感度a相同，沒有反應延遲
units: 原文未指定物理單位（若用物理單位，a的單位是時間的倒數）
status: confirmed
related: bando1995-linear-stability, bando1995-velocity-function, bando1995-no-delay
---

## 主張

每台車的加速度由「它想開的速度」和「現在的速度」的差決定：想開的速度V只看自己到前車的距離，差距乘上敏感度a就是加速度。所有車等距、等速的均勻車流（每台車的速度和間距都一樣；車距b=L/N、速度V(b)）一定是這個方程式的一個解。


---------- wiki/cards/bando1995-spontaneous-jam.md ----------

---
id: bando1995-spontaneous-jam
type: model_theory
source: bando1995
locator: 第1037頁式(17)～(19)、第1038頁式(24)後段、第1039頁圖5、第1040頁圖6
conditions: 模擬，不是實驗；N=100、L=200（車距2）、a=1、V=tanh(Δx−2)+tanh2；初始位置幾乎等距，第1台車往前偏0.1，所有車的初速都是0（式(19)）
units: 無因次
status: confirmed
related: bando1995-velocity-function, bando1995-cluster-values, sugiyama2008-backward-wave
---

## 主張

在模擬裡，100台車的初始位置幾乎等距，只有第1台往前移0.1，所有車從靜止（初速0）開始，之後車流自己分成幾段幾乎停住的塞車和幾段快速前進的車，最後形成5團塞車；這些塞車團都以相同的速度慢慢往後移動。


---------- wiki/cards/bando1995-stable-regions.md ----------

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


---------- wiki/cards/bando1995-velocity-function.md ----------

---
id: bando1995-velocity-function
type: model_theory
source: bando1995
locator: 第1037頁式(16)、第1038頁式(24)和圖3～4、第1042頁圖11
conditions: 無因次；a=1
units: 無因次
status: confirmed
related: bando1995-ovm-equation, bando1995-spontaneous-jam
---

## 主張

作者先試了最簡單的速度函數V=tanh(Δx)，結果在不穩定時會有車往後倒退，等於撞車。所以改用V(Δx)=tanh(Δx−2)+tanh2：車距是0時目標速度V(0)是0（實際速度還是由加速度方程式決定）。作者說在這個模型的模擬裡，駕駛會慢慢加減速、不會超過前車。


---------- wiki/cards/nagel1992-bottleneck.md ----------

---
id: nagel1992-bottleneck
type: model_theory
source: nagel1992
locator: 第2227頁第4節、第2228頁圖6
conditions: 開放道路：左端只要空著就放進一台速度0的車（代表兩線道併成一線道的瓶頸），右端最後6格把車刪掉；長度最多10000格、最多5×10^6步
units: 車／格、車／時間步
status: confirmed
related: nagel1992-transition
---

## 主張

在模擬的瓶頸情境（開放邊界）下，車流自己穩定在密度約每格0.069台、流量約每步0.304台的狀態。圖6把這個點畫在環道模擬的基本圖上，它低於環道基本圖的最大流量；作者也說在v_max=1、而且用隨機逐車更新（不是一般NaSch的同時更新）的特例裡，系統會自己走到最大流量，但v_max較大時看起來不是這樣。


---------- wiki/cards/nagel1992-circle-jams.md ----------

---
id: nagel1992-circle-jams
type: model_theory
source: nagel1992
locator: 第2223頁圖1、第2224頁圖2和第1段
conditions: 環狀道路（週期邊界）、v_max=5；圖1密度0.03、圖2密度0.1（每格的車數）
units: 車／格
status: confirmed
related: nagel1992-randomization, nagel1992-transition
---

## 主張

模擬裡，密度低（每格0.03台）時車流順暢；密度較高（每格0.1台）時，車速的隨機變動會讓一小團一小團的塞車隨機出現，塞車團往後移動，車子開進去停一下、再從前端加速離開，像高速公路上的走走停停波。


---------- wiki/cards/nagel1992-randomization.md ----------

---
id: nagel1992-randomization
type: model_theory
source: nagel1992
locator: 第2222頁第2節最後兩段
conditions: 同nagel1992-rules
units: 格、時間步
status: confirmed
related: nagel1992-rules, nagel1992-circle-jams
---

## 主張

作者說第3步的隨機減速是讓模擬像真實交通的關鍵，它代表人的行為或外在條件造成的速度變動；如果沒有這一步，模型完全確定，任何初始狀態都會很快變成一個固定、每步往後移一格的樣子。


---------- wiki/cards/nagel1992-real-units.md ----------

---
id: nagel1992-real-units
type: model_theory
source: nagel1992
locator: 第2227頁第5節、第2228頁第1～2段
conditions: 作者用幾種粗略的方法把模型換算成真實單位；高速公路的數字是作者引用的量測值
units: m、s、km/h
status: confirmed
related: nagel1992-rules
---

## 主張

作者把一格換算成7.5公尺（塞車時一台車佔的長度），並用幾種方法估算一個時間步大約是0.5到1秒的量級（其中一個數字原文印為0.7秒，但照它列的算式是0.54秒），結論是時間步的數量級是「秒」。其中一種方法用了高速公路上量到的塞車波往後速度約15 km/h。


---------- wiki/cards/nagel1992-rules.md ----------

---
id: nagel1992-rules
type: model_theory
source: nagel1992
locator: 第2222頁第2節
conditions: 單車道，道路切成格子，每格最多一台車；所有車同時更新
units: 格、時間步
status: confirmed
related: nagel1992-randomization
---

## 主張

每一步，每台車依序做4件事：1. 還沒到最高速、前面空間夠，就加速1；2. 前車太近，就減到不會撞上的速度；3. 速度大於0的車，以機率p隨機減速1；4. 照速度往前走。


---------- wiki/cards/nagel1992-transition.md ----------

---
id: nagel1992-transition
type: model_theory
source: nagel1992
locator: 第2224頁第2段、第2225頁圖4
conditions: 環狀道路、v_max=5；長時間平均；系統長度L=10^4格（圖4）
units: 車／格
status: confirmed
related: nagel1992-circle-jams
---

## 主張

這個模型的基本圖上，大約在密度每格0.08台附近看得到從順暢到塞車的轉變；另外，基本圖流量最大值的位置和形狀會隨系統大小改變。作者說從這些圖看不出確切的轉變點在哪。


---------- wiki/cards/orosz2010-delays.md ----------

---
id: orosz2010-delays
type: review
source: orosz2010
locator: 第4467頁第3～4段
conditions: 有反應延遲的跟車模型
units: 無數值
status: confirmed
related: orosz2010-ring-stability, bando1995-no-delay
---

## 主張

作者指出，如果駕駛的反應延遲夠大，均勻車流可能改在短的波（高頻）失去穩定，不再是最長的波；延遲再大，連駕駛想減小擾動的努力都可能失效。


---------- wiki/cards/orosz2010-ovm-family.md ----------

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


---------- wiki/cards/orosz2010-stability-approaches.md ----------

---
id: orosz2010-stability-approaches
type: review
source: orosz2010
locator: 第4466～4467頁第5節、式(5.1)～(5.3)、第4475～4476頁附錄A式(A6)～(A10)
conditions: 均勻車流附近的小擾動（線性化）
units: 無數值
status: confirmed
related: bando1995-linear-stability, orosz2010-ring-stability
---

## 主張

分析均勻車流穩不穩定，文獻裡有三種做法：假設無限長道路上的波、看環上N台車、或看一排車的訊號會不會一台傳一台放大。作者說三種做法得到相同的結果，並在附錄用沒有延遲的情況示範：環上N台車的條件保留N和離散的波數，車數趨近無限多（均勻車距固定）時，跟看一排車的條件取最小值時一致。均勻車流失去穩定時，會出現行進的波。


---------- wiki/cards/ours-finite-n-simulation.md ----------

---
id: ours-finite-n-simulation
type: our_simulation
source: audition/run2.log
locator: 測試A4、A4b（程式在audition/test_ovm.py）
conditions: V=tanh(Δx−2)+tanh2；N=22；車距2和2.5；RK4，時間步長0.05；只激發k=1的小擾動
units: 無因次
status: confirmed
related: ours-finite-n-threshold
---

## 主張

用模擬量出22台車的分界：車距2時量到1.95966（公式1.95949），車距2.5時量到1.54126（公式1.54104）。a=1.98時，照a/2條件應該不穩定，模擬裡擾動卻是衰減的。


---------- wiki/cards/ours-finite-n-threshold.md ----------

---
id: ours-finite-n-threshold
type: our_derivation
source: wiki/derivations/finite-n-threshold.md
locator: 「從Bando 1995推」第1～6步、「跟Orosz 2010對照」
conditions: bando1995的模型；環狀道路N台車，N≥3；只看很小的擾動
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-large-n-note, ours-finite-n-simulation, orosz2010-ring-stability
---

## 主張

車數有限時，非零的第k個波只有在a < 2V'(b)cos²(πk/N)時才會變大（k=0是整體平移，不算；k和N−k是一對共軛，分界相同；N是偶數時k=N/2要直接用式(10)，它在a>0、V'(b)>0時不會失穩）。N≥3時，a往下調時最先變不穩定的是k=1這一對，所以N台車的實際分界是a = 2V'(b)cos²(π/N) = V'(b)(1+cos(2π/N))。22台車、車距2時是1.9595，不是a/2條件給的2；車距b固定、車數越多（環長跟著變長），越接近2V'(b)。


---------- wiki/cards/stern2018-controllers.md ----------

---
id: stern2018-controllers
type: experiment
source: stern2018
locator: 第3頁第1.2節、第5～7頁第3節和式(1)～(5)、第8頁第3.4節
conditions: 自動控制器用那台車自己量到的速度、跟前車的距離，以及從距離變化估出的前車速度；實驗A和B另外有外部給的目標速度
units: s
status: confirmed
related: stern2018-results
---

## 主張

三種控制方式（實驗A的FollowerStopper、實驗B由受過訓練的人照同類策略開、實驗C的PI控制器）的共同想法是：那台車照著車流的平均速度開，而不是跟著前車忽快忽慢。前車加速時讓空隙變大、前車減速時把空隙吃掉，同樣的時間走同樣的距離，但加速和煞車少很多；距離太近時一定以安全為先。


---------- wiki/cards/stern2018-results.md ----------

---
id: stern2018-results
type: experiment
source: stern2018
locator: 第8～9頁第4.1節（指標定義）、第9頁表1、第11頁表2、第12頁表3、第13頁表4、第13頁第4.2節末段
conditions: 比較「第一次出現波、沒有控制」和「控制開啟中表現最好」的時段（A、B有好幾段控制時段，取最好的一段；C只有一段）；每種控制器一場
units: %、次/車/km
status: confirmed
related: stern2018-controllers, stern2018-wave-returns
---

## 主張

三場實驗打開控制後，車隊整體的車速標準差（把所有車和那段時間合在一起算的一個數字）都下降（A降80.8%、B降49.5%、C降54.7%），油耗下降（42.5%、22.1%、28.1%），過度煞車事件（第4.1節定義）大幅減少；通過量A增加14.1%、B增加9.8%，但C減少2.5%。


---------- wiki/cards/stern2018-setup.md ----------

---
id: stern2018-setup
type: experiment
source: stern2018
locator: 第3頁第2.1節、第4～5頁
conditions: 單車道環道；21～22台車；只有一台車的速度可以自動控制
units: m、台
status: confirmed
related: sugiyama2008-setup, stern2018-waves-emerge
---

## 主張

實驗在周長260公尺的單車道環道進行，21～22台車，其中一台是可以自動控制速度的車；其他駕駛被要求像尖峰時段那樣開：前方空隙拉大時要追上，同時保持安全、禁止貼車，目的是不讓他們自己把波消掉。那台控制車為了方便緊急閃避，行駛半徑往外偏半個車寬。


---------- wiki/cards/stern2018-waves-emerge.md ----------

---
id: stern2018-waves-emerge
type: experiment
source: stern2018
locator: 第4頁第2.2節、第9～10頁第4.2節、表1、表2、表4
conditions: 所有車都由人開的時段
units: s
status: confirmed
related: stern2018-setup, sugiyama2008-jam-emerges
---

## 主張

三場實驗在全部由人開的時候都出現了走走停停波：實驗A在第79秒、實驗B在第55秒、實驗C在第161秒看到第一個波。


---------- wiki/cards/sugiyama2008-23-vehicles.md ----------

---
id: sugiyama2008-23-vehicles
type: experiment
source: sugiyama2008
locator: 第5頁第3段、腳註15
conditions: 同一個230公尺環道，車數23台
units: 台
status: confirmed
related: sugiyama2008-setup
---

## 主張

作者做過不同車數的實驗，文中只提到23台的結果：也形成了塞車團，速度跟22台時一樣。


---------- wiki/cards/sugiyama2008-backward-wave.md ----------

---
id: sugiyama2008-backward-wave
type: experiment
source: sugiyama2008
locator: 第5頁第1～2段、第6頁圖4
conditions: 同sugiyama2008-setup的條件；速度是從360度攝影機的影片讀出的軌跡估算
units: km/h、台
status: confirmed
related: sugiyama2008-jam-emerges, sugiyama2008-highway-comparison
---

## 主張

塞車團往跟車子相反的方向移動，速度大約20 km/h，而且大小和速度維持不變。團裡的車完全停下，團外的車約40 km/h；前端的車加速離開，後面又有車加入，所以塞車團一直在，但裡面的車一直在換。


---------- wiki/cards/sugiyama2008-fundamental-diagram.md ----------

---
id: sugiyama2008-fundamental-diagram
type: experiment
source: sugiyama2008
locator: 第2頁最後一段、第3頁圖1
conditions: 日本某條高速公路單一地點一個月的資料，由當時的日本道路公團量測
units: 台/km、台/5分鐘
status: confirmed
related: sugiyama2008-mechanism
---

## 主張

把高速公路上的車流密度和流量畫成圖（基本圖；圖1畫的是密度和流量的關係），資料點在臨界密度附近明顯分成兩群：自由流和擁擠車流。圖1這個地點的臨界密度約每公里25台。


---------- wiki/cards/sugiyama2008-highway-comparison.md ----------

---
id: sugiyama2008-highway-comparison
type: experiment
source: sugiyama2008
locator: 第5頁第2段、第6頁圖5
conditions: 作者拿其他研究的高速公路資料比較；圖5的軌跡是從Treiterer和Myers 1974的圖描下來的，原始空拍是1967年
units: km/h
status: confirmed
related: sugiyama2008-backward-wave
---

## 主張

作者表示，實驗裡塞車團往後退的速度（約20 km/h）跟真實高速公路上量到的塞車往後傳的速度差不多，並用1967年高速公路空拍描出的車輛軌跡（圖5）來比較。


---------- wiki/cards/sugiyama2008-jam-emerges.md ----------

---
id: sugiyama2008-jam-emerges
type: experiment
source: sugiyama2008
locator: 第4頁最後一段、第5頁圖3
conditions: 同sugiyama2008-setup的條件（230公尺、22台車）
units: 分鐘、台
status: confirmed
related: sugiyama2008-setup, sugiyama2008-backward-wave
---

## 主張

一開始均勻的車流維持了一段時間，之後車距出現小小的波動並逐漸變大，最後有幾台車被迫完全停下，形成走走停停。圖3的第二張照片是開始3分鐘後拍的，那時已經有一團5台車的塞車。


---------- wiki/cards/sugiyama2008-mechanism.md ----------

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

這篇裡有三種不同層次的說法，要分開看：一是作者對模型的說明，模型在一開始是自由流、平均密度略高於某個臨界值時，能在沒有瓶頸的環道上產生塞車，機制是小波動在密度低時消失、超過臨界值時長大；二是環道實驗的觀察，在他們選的車數下，沒有瓶頸也出現了塞車；三是作者對瓶頸的解釋，瓶頸只是讓密度超過臨界值的觸發，不是塞車的根本原因。


---------- wiki/cards/sugiyama2008-setup.md ----------

---
id: sugiyama2008-setup
type: experiment
source: sugiyama2008
locator: 第4頁第2～3段、圖2
conditions: 平坦地面、單一車道的環形道路；車數事先用模型估過，刻意放在不穩定的範圍
units: m、km/h、台
status: confirmed
related: sugiyama2008-jam-emerges
---

## 主張

實驗用周長230公尺的環形道路放22台車，開始前讓車子以約30 km/h、間距大致均勻地繞圈；之後駕駛只被要求安全跟前車、盡量維持巡航速度。


---------- wiki/cards/tadaki2013-expressway-consistency.md ----------

---
id: tadaki2013-expressway-consistency
type: experiment
source: tadaki2013
locator: 第11頁第2段、第3頁圖1、第9～10頁圖7(a)和擬合式
conditions: 高速公路的數字是第11頁的敘述，引用參考文獻[9]（Sugiyama 2008）；約每公里25台可在第3頁圖1和Sugiyama 2008第3頁圖1（東名高速公路資料）核對，約120 km/h只出現在第11頁的敘述；比較方法是作者的粗略論證
units: 台/km、台/m、km/h
status: confirmed
related: tadaki2013-critical-density, sugiyama2008-fundamental-diagram
---

## 主張

作者說，高速公路自由流平均約120 km/h、臨界密度約每公里25台；實驗自由流約40 km/h（這是第10頁對圖7(a)自由流資料擬合二次曲線aρ − bρ²得到的係數a，不是直接量的平均車速）、臨界密度每公尺0.08～0.09台。作者用「車速快三倍，需要的車距也大約大三倍」的粗略比例，認為兩者一致。


---------- wiki/cards/tadaki2013-high-density.md ----------

---
id: tadaki2013-high-density
type: experiment
source: tadaki2013
locator: 第12頁第2段、第8頁圖5、第18頁圖C.2
conditions: 40台那一場（場次1940），是第一天的場次；有列入兩天車速和波動的圖5和第12頁的討論，但沒有納入用來估計臨界密度的選定資料
units: 台
status: confirmed
related: bando1995-stable-regions
---

## 主張

40台那一場的車速波動非常小，時空圖上車流是均勻的。作者提到有些理論模型預測密度高到一定程度時均勻車流又會變穩定，但說目前還不清楚這場觀察到的是不是那種情況。


---------- wiki/cards/tadaki2013-metastable.md ----------

---
id: tadaki2013-metastable
type: experiment
source: tadaki2013
locator: 第5頁表1、第6頁定點量測說明、第9頁圖7(c)、第10頁圖8和內文
conditions: 圖7(c)用的是第二天2228、2328（28台）和2830（30台）三場；另一場30台的2030另列在圖8
units: 台、台/m
status: confirmed
related: tadaki2013-critical-density
---

## 主張

圖7(c)的三場（28台兩場、30台一場）裡，基本圖上同一個密度附近同時有自由流和塞車兩種點，作者據此判讀出現了介穩態。


---------- wiki/cards/tadaki2013-setup.md ----------

---
id: tadaki2013-setup
type: experiment
source: tadaki2013
locator: 第3～5頁、圖2～3、表1
conditions: 室內平地環道；同款車；大學生駕駛；目標速度30 km/h
units: m、km/h、台、s
status: confirmed
related: tadaki2013-density-dependence
---

## 主張

實驗在名古屋巨蛋周長314公尺的室內環道進行，兩天共19場，每場10到40台同款的車，由52位大學生輪流開，被要求用自己的方式安全地以約30 km/h行駛；車的位置用雷射掃描器大約每0.2秒量一次。


---------- wiki/sources/bando1995.md ----------

---
id: bando1995
kind: paper
authors: M. Bando, K. Hasebe, A. Nakayama, A. Shibata, Y. Sugiyama
year: 1995
title: Dynamical model of traffic congestion and numerical simulation
venue: Physical Review E 51(2), 1035–1042
doi: 10.1103/PhysRevE.51.1035
url: https://doi.org/10.1103/PhysRevE.51.1035
read_status: 全文已讀
read_scope: 第1035～1042頁全文，包含式(1)～(27)、圖1～11和參考文獻；PDF是掃描檔，對照頁面圖片讀，另外用OCR轉成文字做引用比對
independent: 是
---


---------- wiki/sources/nagel1992.md ----------

---
id: nagel1992
kind: paper
authors: Kai Nagel, Michael Schreckenberg
year: 1992
title: A cellular automaton model for freeway traffic
venue: Journal de Physique I 2(12), 2221–2229
doi: 10.1051/jp1:1992277
url: https://doi.org/10.1051/jp1:1992277
read_status: 全文已讀
read_scope: 第2221～2229頁全文和圖1～6；用的是HAL典藏的掃描版（jpa-00246697），文字層字序錯亂，對照頁面圖片讀
independent: 是
---


---------- wiki/sources/orosz2010.md ----------

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


---------- wiki/sources/stern2018.md ----------

---
id: stern2018
kind: paper
authors: Raphael E. Stern, Shumo Cui, Maria Laura Delle Monache, Rahul Bhadani, Matt Bunting, Miles Churchill, Nathaniel Hamilton, R'mani Haulcy, Hannah Pohlmann, Fangyu Wu, Benedetto Piccoli, Benjamin Seibold, Jonathan Sprinkle, Daniel B. Work
year: 2018
title: Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments
venue: Transportation Research Part C: Emerging Technologies（卷期和頁碼待查證）
doi: 10.1016/j.trc.2018.02.005
url: https://arxiv.org/abs/1705.01693
read_status: 全文已讀
read_scope: arXiv預印本1705.01693v1（2017-05-04）第1～14頁本文和表1～4；附錄只看了需要的部分。正式期刊版沒有讀，兩個版本可能有差異
independent: 是
---


---------- wiki/sources/tadaki2013.md ----------

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


========== 程式或執行輸出：scripts/check_wiki.py ==========

```
"""檢查Wiki的文獻檔、證據卡、索引，並掃描個資和金鑰。

用法：python3 scripts/check_wiki.py [--root 路徑] [--strict]
錯誤數 > 0 時結束代碼是1。只用標準函式庫。
--strict：push前用。Git歷史裡的PDF和疑似個資也算錯誤（平常只算警告，
因為歷史要改只能改寫歷史，必須先問使用者）。
"""
import argparse
import posixpath
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

KINDS = {"paper", "book", "data", "popular"}
READ = {"全文已讀", "部分章節", "只讀摘要", "尚未查證"}
TYPES = {"experiment", "model_theory", "review", "expression", "our_derivation", "our_simulation"}
OURS = {"our_derivation", "our_simulation"}
SOURCE_FIELDS = ["id", "kind", "authors", "year", "title", "venue", "doi", "url",
                 "read_status", "read_scope", "independent"]
SOURCE_SECTIONS = ["這篇在做什麼", "研究條件", "主要結果", "限制", "ingest紀錄"]
CARD_FIELDS = ["id", "type", "source", "locator", "conditions", "units", "status", "related"]
CARD_SECTIONS = ["主張", "原文依據", "限制"]
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_PAPERS = 5
MAX_QUOTE_WORDS = 50

# 個資和金鑰的樣式。這幾行本身會被掃到，所以行尾加了忽略標記。
PRIVACY = [
    (re.compile(r"(?<![\d.])4\d{8}(?![\d.])"), "像學號的9位數字"),  # privacy-scan: ignore
    (re.compile(r"(?<![\d.])09\d{2}[- ]?\d{3}[- ]?\d{3}(?![\d.])"), "手機號碼"),  # privacy-scan: ignore
    (re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)(?!example\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "電子郵件"),  # privacy-scan: ignore
    (re.compile(r"(/home/|/Users/|[A-Za-z]:\\Users|/tmp/claude|/mnt/user-data)"), "本機路徑"),  # privacy-scan: ignore
    (re.compile(r"\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,})"), "金鑰或Token"),  # privacy-scan: ignore
    (re.compile(r"\bI[1-4]A\d{2}\b"), "班級座號"),  # privacy-scan: ignore
]
IGNORE_MARK = "privacy-scan: ignore"
CJK = r"[一-鿿]"
SPACE_RE = re.compile(rf"{CJK} +[A-Za-z0-9]|[A-Za-z0-9] +{CJK}")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"[錯誤] {where}：{msg}")

    def warn(self, where, msg):
        self.warnings.append(f"[警告] {where}：{msg}")


def parse(path):
    """讀開頭的 --- 區塊（每行 key: value），回傳 (欄位, 內文)。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            meta.setdefault("__bad__", []).append(line)
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        if k in meta:
            meta.setdefault("__dup__", []).append(k)
        meta[k] = v.strip()
    return meta, text[end + 5:]


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def check_fields(rep, where, meta, fields):
    if meta is None:
        rep.err(where, "開頭沒有 --- 欄位區塊")
        return False
    for bad in meta.get("__bad__", []):
        rep.err(where, f"欄位格式錯誤：{bad}")
    for dup in meta.get("__dup__", []):
        rep.err(where, f"欄位 {dup} 出現不只一次")
    for f in fields:
        if f not in meta:
            rep.err(where, f"缺少欄位 {f}")
        elif f != "related" and not meta[f]:
            rep.err(where, f"欄位 {f} 是空的")
    for f in meta:
        if f not in ("__bad__", "__dup__") and f not in fields:
            rep.err(where, f"不認得的欄位 {f}")
    return True


def check_sources(root, rep):
    sources = {}
    for p in sorted((root / "wiki" / "sources").glob("*.md")):
        if p.name == "_template.md":
            continue
        where = p.relative_to(root).as_posix()
        meta, body = parse(p)
        if not check_fields(rep, where, meta, SOURCE_FIELDS):
            continue
        if meta.get("id") != p.stem:
            rep.err(where, f"id {meta.get('id')} 跟檔名不一樣")
        if not ID_RE.match(p.stem):
            rep.err(where, "檔名只能用小寫英數和-")
        if meta.get("kind") not in KINDS:
            rep.err(where, f"kind 要是 {'、'.join(sorted(KINDS))} 之一")
        if meta.get("read_status") not in READ:
            rep.err(where, f"read_status 要是 {'、'.join(sorted(READ))} 之一")
        if meta.get("independent") not in ("是", "否"):
            rep.err(where, "independent 要是「是」或「否」")
        if not re.fullmatch(r"\d{4}", meta.get("year", "")):
            rep.err(where, "year 要是4位數年份")
        url = meta.get("url", "")
        if url and not url.startswith("https://"):
            rep.err(where, "url 要用 https://")
        doi = meta.get("doi", "")
        if doi and doi != "無" and not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
            rep.err(where, "doi 格式不對（寫 10.xxxx/... 或「無」）")
        secs = sections(body)
        for s in SOURCE_SECTIONS:
            if s not in secs:
                rep.err(where, f"缺少段落「## {s}」")
        sources[p.stem] = meta
    return sources


def quote_words(text):
    lines = [l[1:] for l in text.splitlines() if l.startswith(">")]
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", " ".join(lines)))


def check_cards(root, rep, sources, tracked):
    cards = {}
    paths = [p for p in sorted((root / "wiki" / "cards").glob("*.md")) if p.name != "_template.md"]
    for p in paths:
        where = p.relative_to(root).as_posix()
        meta, body = parse(p)
        if not check_fields(rep, where, meta, CARD_FIELDS):
            continue
        cards[p.stem] = (meta, body, where)
    for cid, (meta, body, where) in cards.items():
        if meta.get("id") != cid:
            rep.err(where, f"id {meta.get('id')} 跟檔名不一樣")
        if not ID_RE.match(cid):
            rep.err(where, "檔名只能用小寫英數和-")
        t, src, loc = meta.get("type"), meta.get("source", ""), meta.get("locator", "")
        if t not in TYPES:
            rep.err(where, f"type 要是 {'、'.join(sorted(TYPES))} 之一")
        if meta.get("status") not in ("confirmed", "pending"):
            rep.err(where, "status 要是 confirmed 或 pending")
        if t in OURS:
            f = root / src
            if not src or src.startswith("/") or ".." in src or not f.is_file():
                rep.err(where, f"source 要是repo裡存在的檔案（找不到 {src}）")
            elif f.resolve() not in tracked:
                rep.err(where, f"source {src} 是不會上傳的檔案，別人沒辦法核對")
        elif t in TYPES:
            s = sources.get(src)
            if s is None:
                rep.err(where, f"source {src} 在 wiki/sources/ 裡找不到")
            else:
                rs = s.get("read_status")
                if rs == "尚未查證" and meta.get("status") == "confirmed":
                    rep.err(where, f"{src} 還是「尚未查證」，卡片不能是 confirmed")
                if rs == "只讀摘要" and "摘要" not in loc:
                    rep.err(where, f"{src} 只讀了摘要，locator 要寫「摘要」")
                if t == "expression" and s.get("kind") != "popular":
                    rep.err(where, "expression 只能引用 kind: popular 的文獻")
                if t != "expression" and s.get("kind") == "popular":
                    rep.err(where, "科普或新聞只能當 expression，不能當研究證據")
        secs = sections(body)
        for s_ in CARD_SECTIONS:
            if s_ not in secs or not secs[s_]:
                rep.err(where, f"缺少段落或段落是空的「## {s_}」")
        claim = re.sub(r"(?<!\d)(19|20)\d{2}(?!\d)", "", secs.get("主張", ""))
        if re.search(r"\d", claim):
            if meta.get("units") == "無數值":
                rep.err(where, "主張裡有數字，units 不能寫「無數值」（要寫單位或「無因次」）")
            if t not in OURS and not re.search(r"\d|摘要", loc):
                rep.err(where, "主張裡有數字，locator 要到頁碼、章節、公式或圖表編號（或寫「摘要」）")
        w = quote_words(body)
        if w > MAX_QUOTE_WORDS:
            rep.err(where, f"英文原文引用 {w} 個字，超過 {MAX_QUOTE_WORDS}")
        for r in [x.strip() for x in meta.get("related", "").split(",") if x.strip()]:
            if r not in cards:
                rep.err(where, f"related 的 {r} 不存在")
    return cards


def check_index(root, rep, sources, cards):
    idx = root / "wiki" / "index.md"
    if not idx.is_file():
        rep.err("wiki/index.md", "檔案不存在")
        return
    text = idx.read_text(encoding="utf-8")
    expected = index_with_generated(text, render_index(root))
    if expected is None:
        rep.err("wiki/index.md", "找不到自動產生區塊的標記，請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py")
    elif expected != text:
        rep.err("wiki/index.md", "跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），"
                                 "請跑 python3 scripts/build_index.py")
    for kind, name in re.findall(r"\b(sources|cards)/([a-z0-9-]+)\.md", text):
        if not (root / "wiki" / kind / f"{name}.md").is_file():
            rep.err("wiki/index.md", f"列出的 {kind}/{name}.md 不存在")
    for sid in sources:
        if f"sources/{sid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出文獻 {sid}")
    for cid in cards:
        if f"cards/{cid}.md" not in text:
            rep.err("wiki/index.md", f"沒有列出證據卡 {cid}")


# index.md的文獻表和證據卡清單由scripts/build_index.py從文獻檔、證據卡產生（單一事實來源）。
# 兩個標記中間是產生的內容，外面的主題介紹和導覽人工寫。check_index會重新產生一次，跟檔案不同就報錯。
# （2026-11-12加的：第2、3輪審查發現手寫的索引摘要沒跟著卡片更新，見runs/2026-11-12-index-generation.md。）
INDEX_BEGIN = "<!-- 以下由scripts/build_index.py從wiki/sources和wiki/cards產生，不要手改；改了文獻檔或證據卡就重跑 -->"
INDEX_END = "<!-- 自動產生結束 -->"
OURS_GROUP = "我們自己的推導和模擬"


def fix_links(text):
    """主張裡的相對連結是從cards/出發寫的，放進index.md要改成從wiki/出發。"""
    def repl(m):
        target = m.group(1)
        if re.match(r"^(https?:|#|/)", target):
            return m.group(0)
        return f"]({posixpath.normpath(posixpath.join('cards', target))})"
    return re.sub(r"\]\(([^)\s]+)\)", repl, text)


def render_index(root):
    wiki = root / "wiki"
    srcs, groups = [], {}
    for p in sorted((wiki / "sources").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, _ = parse(p)
        meta = meta or {}
        srcs.append(f"| {p.stem} | {meta.get('kind', '')} | {meta.get('read_status', '')} | "
                    f"[sources/{p.name}](sources/{p.name}) |")
    n_cards = 0
    for p in sorted((wiki / "cards").glob("*.md")):
        if p.name == "_template.md":
            continue
        meta, body = parse(p)
        meta = meta or {}
        n_cards += 1
        group = OURS_GROUP if meta.get("type", "").startswith("our_") else meta.get("source", "")
        claim = fix_links(sections(body).get("主張", ""))
        groups.setdefault(group, []).append(
            f"#### [{p.stem}](cards/{p.name})\n\n- 類型：{meta.get('type', '')}\n- 狀態：{meta.get('status', '')}\n"
            f"- 條件：{meta.get('conditions', '')}\n\n{claim}")
    out = [INDEX_BEGIN, "", "## 文獻", "", "| id | 種類 | 閱讀狀態 | 檔案 |", "|---|---|---|---|", *srcs, "",
           "## 證據卡", "", f"共{n_cards}張。每張的條件取自卡片的conditions欄位，主張直接取自卡片的「## 主張」，都沒有另外縮寫；原文依據和限制請點進卡片看。"]
    for g in sorted(k for k in groups if k != OURS_GROUP) + ([OURS_GROUP] if OURS_GROUP in groups else []):
        out += ["", f"### {g}"]
        for item in groups[g]:
            out += ["", item]
    out += ["", INDEX_END]
    return "\n".join(out)


def index_with_generated(text, generated):
    """把index.md裡兩個標記之間換成新產生的內容；沒有標記就回傳None。"""
    a, b = text.find(INDEX_BEGIN), text.find(INDEX_END)
    if a < 0 or b < a:
        return None
    return text[:a] + generated + text[b + len(INDEX_END):]


def tracked_files(root):
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=root,
                             capture_output=True, text=True, check=True).stdout
        return [root / l for l in out.splitlines() if l]
    except (OSError, subprocess.CalledProcessError):
        return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


# SHA-256雜湊值是64位十六進位，裡面常會剛好有一段像學號或手機的數字。只在有明確標記時排除：
# 1. 同一行寫了「SHA-256」，後面緊接著用反引號包起來的64位小寫十六進位；或
# 2. 表格的表頭有一欄以「SHA-256」開頭，而且這一格以反引號包起來的64位小寫十六進位開頭。
# 排除只套用在學號和手機兩條規則，信箱、路徑、金鑰、座號照原本那一行檢查。
# （2026-11-11看到pipeline/review/n3-package-r2.md的雜湊被誤判成學號之後才加的，紀錄在
#  runs/2026-11-11-check-wiki-hash-exclusion.md。掃Git歷史時用那個commit的完整檔案判斷表頭，
#  見runs/2026-11-11-check-wiki-history-fullfile.md。）
HASH_TOKEN = "`[0-9a-f]{64}`"
HASH_RE = re.compile(HASH_TOKEN)
LABELED_HASH = re.compile(r"(SHA-256[:：]?\s*)" + HASH_TOKEN)
HASH_CELL = re.compile(r"^(\s*)" + HASH_TOKEN)
HASH_MASKED = {"像學號的9位數字", "手機號碼"}


def sha_column(line):
    """表格表頭裡以SHA-256開頭的那一欄，回傳它用「|」切開後的位置；不是這種表頭就回傳None。"""
    if not line.lstrip().startswith("|"):
        return None
    for i, cell in enumerate(line.split("|")):
        if cell.strip().startswith("SHA-256"):
            return i
    return None


class ShaTable:
    """一行一行讀，記住現在是不是在有SHA-256欄的表格裡。表格一結束（下一行不是「|」開頭）就失效。"""
    def __init__(self):
        self.col = None

    def feed(self, line):
        col = sha_column(line)
        if col is not None:
            self.col = col
        elif not line.lstrip().startswith("|"):
            self.col = None
        return self.col


def mask_hashes(line, sha_col=None):
    line = LABELED_HASH.sub(r"\1`<sha256>`", line)
    if sha_col is not None and line.lstrip().startswith("|"):
        cells = line.split("|")
        if sha_col < len(cells):
            cells[sha_col] = HASH_CELL.sub(r"\1`<sha256>`", cells[sha_col])
        line = "|".join(cells)
    return line


def scan_line(line, sha_col=None):
    if IGNORE_MARK in line:
        return []
    masked = mask_hashes(line, sha_col)
    return [name for pat, name in PRIVACY if pat.search(masked if name in HASH_MASKED else line)]


def check_history(root, rep, strict):
    """掃Git歷史裡加進去過的每一行，以及出現過的PDF。"""
    def git(*args):
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=True).stdout
    try:
        git("rev-parse", "--verify", "HEAD")
    except (OSError, subprocess.CalledProcessError):
        return
    report = rep.err if strict else rep.warn
    for name in sorted(set(git("log", "--all", "--name-only", "--format=").splitlines())):
        if name.lower().endswith(".pdf"):
            report("Git歷史", f"出現過PDF：{name}")
    def sha_cols(commit, path):
        """讀這個commit裡這個檔案的完整內容，算出每一行是不是在SHA-256表格裡（行號從1開始）。
        讀不到（例如檔名有特殊字元）就全部當成不在表格裡，也就是不排除。"""
        try:
            text = git("show", f"{commit}:{path}")
        except subprocess.CalledProcessError:
            return {}
        table = ShaTable()
        return {n: table.feed(line) for n, line in enumerate(text.splitlines(), 1)}

    def flush(commit, path, added):
        # 只有新增的行裡有反引號包起來的64位十六進位，排除才可能有作用，這時才去讀完整檔案
        cols = sha_cols(commit, path) if any(HASH_RE.search(text) for _, text in added) else {}
        for n, text in added:
            for name in scan_line(text, cols.get(n)):
                report(f"Git歷史 {commit} {path}", f"疑似{name}")

    # 只掃每個commit新增的行，但表頭用那個commit的完整檔案判斷，不靠diff前後幾行的上下文。
    # 用@@標頭的行數判斷哪些行是內容，內容剛好以「+++」開頭也不會被當成檔名。
    commit, path, added, n, old_left, new_left = "", "", [], 0, 0, 0
    for line in git("log", "--all", "-p", "--no-color", "--format=commit %h").splitlines():
        if old_left > 0 or new_left > 0:
            if line.startswith("+"):
                added.append((n, line[1:]))
                n, new_left = n + 1, new_left - 1
            elif line.startswith("-"):
                old_left -= 1
            elif line.startswith(" ") or line == "":
                n, old_left, new_left = n + 1, old_left - 1, new_left - 1
            continue
        if line.startswith("commit "):
            flush(commit, path, added)
            commit, path, added = line[7:], "", []
        elif line.startswith("diff --git "):
            flush(commit, path, added)
            path, added = "", []
        elif line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if m:
                old_left = int(m.group(1)) if m.group(1) is not None else 1
                n = int(m.group(2))
                new_left = int(m.group(3)) if m.group(3) is not None else 1
    flush(commit, path, added)


def check_privacy(root, rep, tracked):
    for p in sorted(tracked):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if p.suffix.lower() == ".pdf":
            rep.err(rel, "PDF不能放進repo")
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        table = ShaTable()
        for n, line in enumerate(text.splitlines(), 1):
            for name in scan_line(line, table.feed(line)):
                rep.err(f"{rel}:{n}", f"疑似{name}")


def check_spacing(root, rep):
    for p in sorted((root / "wiki").rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        lines = p.read_text(encoding="utf-8").splitlines()
        start = 0
        if lines and lines[0] == "---" and "---" in lines[1:]:
            start = lines.index("---", 1) + 1
        in_code = False
        for n, line in enumerate(lines[start:], start + 1):
            if line.startswith("```"):
                in_code = not in_code
            if in_code or line.startswith(">"):
                continue
            if SPACE_RE.search(re.sub(r"`[^`]*`", "", line)):
                rep.warn(f"{rel}:{n}", "中文和英文或數字之間有空格")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    rep = Report()
    tracked = {p.resolve() for p in tracked_files(root) if p.is_file()}
    sources = check_sources(root, rep)
    cards = check_cards(root, rep, sources, tracked)
    check_index(root, rep, sources, cards)
    check_privacy(root, rep, tracked)
    check_history(root, rep, args.strict)
    check_spacing(root, rep)
    used = {m.get("source") for m, _, _ in cards.values() if m.get("status") == "confirmed"}
    papers = [s for s, m in sources.items() if m.get("kind") == "paper" and m.get("independent") == "是"
              and m.get("read_status") in ("全文已讀", "部分章節") and s in used]
    if len(papers) < MIN_PAPERS:
        rep.warn("wiki/sources", f"實際讀過、而且有confirmed證據卡的獨立論文 {len(papers)} 篇，"
                                 f"還不到 {MIN_PAPERS} 篇")
    for line in rep.errors + rep.warnings:
        print(line)
    pending = sum(1 for m, _, _ in cards.values() if m.get("status") == "pending")
    print(f"\n文獻 {len(sources)} 篇（算進5篇的獨立論文 {len(papers)} 篇），"
          f"證據卡 {len(cards)} 張（pending {pending} 張）。")
    print(f"錯誤 {len(rep.errors)} 個，警告 {len(rep.warnings)} 個。")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
```


========== 程式或執行輸出：scripts/build_index.py ==========

```
"""從文獻檔和證據卡產生wiki/index.md的文獻表和證據卡清單。

用法：
  python3 scripts/build_index.py           # 重寫index.md裡兩個標記之間的內容，標記外面的人工內容不動
  python3 scripts/build_index.py --check   # 只比對，不同步就印出來、結束代碼1（check_wiki.py也會做同樣的比對）
產生的內容：文獻的id、種類、閱讀狀態、連結；證據卡依文獻分組，每張的id、類型、狀態、主張全文、連結。
主張直接用卡片的「## 主張」，不另外縮寫。產生規則寫在check_wiki.py的render_index，兩邊用同一份。
"""
import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wiki import index_with_generated, render_index  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    idx = root / "wiki" / "index.md"
    text = idx.read_text(encoding="utf-8")
    new = index_with_generated(text, render_index(root))
    if new is None:
        print("[錯誤] wiki/index.md找不到自動產生區塊的兩行標記")
        return 1
    if args.check:
        same = new == text
        print("index.md跟文獻檔、證據卡同步" if same else "[錯誤] index.md跟文獻檔、證據卡不同步")
        return 0 if same else 1
    if new != text:
        idx.write_text(new, encoding="utf-8", newline="\n")
        print("已重建 wiki/index.md 的自動產生區塊")
    else:
        print("wiki/index.md 已經是最新的，沒有改")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


========== 程式或執行輸出：tests/test_check_wiki.py ==========

```
"""故意弄壞Wiki，確認check_wiki.py擋得住。

用法：python3 tests/test_check_wiki.py
每個情境印出 預期／實際。只用標準函式庫，在暫存資料夾裡跑，不會動到repo。
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_wiki.py"

SOURCE = """---
id: demo2000
kind: paper
authors: A. Author, B. Author
year: 2000
title: A demo paper
venue: Demo Journal 1(1)
doi: 10.1234/demo.2000
url: https://example.com/demo
read_status: 全文已讀
read_scope: 全文
independent: 是
---

## 這篇在做什麼
示範用。

## 研究條件
示範用。

## 主要結果
見cards/demo2000-claim.md。

## 限制
示範用。

## ingest紀錄
示範用。
"""

CARD = """---
id: demo2000-claim
type: experiment
source: demo2000
locator: p.3 圖2
conditions: 環狀道路
units: m
status: confirmed
related:
---

## 主張
2000年的實驗裡，22台車繞230m的環。

## 原文依據
> a short quote

## 限制
只有一次實驗。
"""

INDEX_HEAD = "# 索引\n\n人工寫的導覽。\n\n"


def make_site(tmp):
    (tmp / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp / "scripts" / "check_wiki.py")
    shutil.copy(SCRIPT.parent / "build_index.py", tmp / "scripts" / "build_index.py")
    (tmp / "wiki" / "sources").mkdir(parents=True)
    (tmp / "wiki" / "cards").mkdir()
    (tmp / "wiki" / "sources" / "demo2000.md").write_text(SOURCE, encoding="utf-8")
    (tmp / "wiki" / "cards" / "demo2000-claim.md").write_text(CARD, encoding="utf-8")
    sys.path.insert(0, str(SCRIPT.parent))
    from check_wiki import INDEX_BEGIN, INDEX_END
    (tmp / "wiki" / "index.md").write_text(INDEX_HEAD + INDEX_BEGIN + "\n" + INDEX_END + "\n", encoding="utf-8")
    rebuild(tmp)


def rebuild(tmp):
    """照規定的做法：改了文獻檔或證據卡之後重建索引。"""
    subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "build_index.py"), "--root", str(tmp)],
                   check=True, capture_output=True)


def run(tmp, *args):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-B", str(tmp / "scripts" / "check_wiki.py"), "--root", str(tmp), *args],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, r.stdout


def git(tmp, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    subprocess.run(["git", *args], cwd=tmp, env=env, check=True, capture_output=True)


def commit_all(tmp, msg):
    git(tmp, "add", "-A")
    git(tmp, "commit", "-q", "-m", msg)


def leak_then_remove(tmp):
    """先commit一個有金鑰的檔案，再刪掉commit：現在的檔案乾淨，但歷史裡還有。"""
    git(tmp, "init", "-q")
    (tmp / "note.md").write_text("key=sk-" + "b" * 30 + "\n", encoding="utf-8")
    commit_all(tmp, "leak")
    (tmp / "note.md").unlink()
    commit_all(tmp, "remove")


def our_card_to_ignored(tmp):
    git(tmp, "init", "-q")
    (tmp / ".gitignore").write_text("local/\n", encoding="utf-8")
    (tmp / "local").mkdir()
    (tmp / "local" / "sim.py").write_text("print(1)\n", encoding="utf-8")
    edit(C(tmp), "type: experiment", "type: our_simulation")
    edit(C(tmp), "source: demo2000", "source: local/sim.py")


# 雜湊值排除的測試用：假學號、假手機只在這兩行出現，其他地方用變數組字串。
SID = "412345678"  # privacy-scan: ignore
PHONE = "0912345678"  # privacy-scan: ignore
SHA_TABLE = "| 檔案 | SHA-256 |\n|---|---|\n"


def fake_hash(inner="", n=64):
    """長得像SHA-256的十六進位字串，可以在中間夾一段數字。"""
    return ("ab" * 10 + inner).ljust(n, "c")[:n]


def note(text):
    return lambda t: (t / "note.md").write_text(text, encoding="utf-8")


def history_note(text):
    """先commit一個檔案，再刪掉：現在的檔案乾淨，只剩歷史裡有。"""
    def f(tmp):
        git(tmp, "init", "-q")
        (tmp / "note.md").write_text(text, encoding="utf-8")
        commit_all(tmp, "add")
        (tmp / "note.md").unlink()
        commit_all(tmp, "remove")
    return f


def history_versions(*texts):
    """同一個檔案依序commit好幾個版本，最後刪掉。後面版本的diff只看得到改動附近幾行。"""
    def f(tmp):
        git(tmp, "init", "-q")
        for i, text in enumerate(texts):
            (tmp / "note.md").write_text(text, encoding="utf-8")
            commit_all(tmp, f"v{i}")
        (tmp / "note.md").unlink()
        commit_all(tmp, "remove")
    return f


def rows(n, cell=None):
    return "".join(f"| `f{i}.md` | `{cell or fake_hash()}` |\n" for i in range(n))


def edit(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert old in t, f"測試寫錯了：{path.name} 裡找不到 {old!r}"
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


def S(tmp):
    return tmp / "wiki" / "sources" / "demo2000.md"


def C(tmp):
    return tmp / "wiki" / "cards" / "demo2000-claim.md"


def add_popular(tmp):
    t = SOURCE.replace("demo2000", "news2001").replace("kind: paper", "kind: popular")
    (tmp / "wiki" / "sources" / "news2001.md").write_text(t, encoding="utf-8")
    rebuild(tmp)


# 第4個欄位是選項：args＝額外參數；warn＝預期只有警告（結束代碼0）且警告裡有這段字；
# out＝預期結束代碼0且輸出裡有這段字。沒有選項時：None代表預期沒有錯誤，字串代表錯誤裡要有這段字。
CASES = [
    ("正常資料", lambda t: None, None),
    ("主張裡只有年份，units寫無數值", lambda t: (edit(C(t), "units: m", "units: 無數值"),
                                       edit(C(t), "22台車繞230m的環", "做了實驗"), rebuild(t)), None),
    ("文獻少一個欄位", lambda t: edit(S(t), "venue: Demo Journal 1(1)\n", ""), "缺少欄位 venue"),
    ("閱讀狀態亂寫", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 大概讀過"), "read_status 要是"),
    ("DOI格式錯", lambda t: edit(S(t), "doi: 10.1234/demo.2000", "doi: demo"), "doi 格式不對"),
    ("網址不是https", lambda t: edit(S(t), "https://example.com", "http://example.com"), "url 要用 https://"),
    ("文獻少段落", lambda t: edit(S(t), "## 限制\n示範用。\n", ""), "缺少段落「## 限制」"),
    ("證據卡的文獻不存在", lambda t: edit(C(t), "source: demo2000", "source: ghost1999"), "找不到"),
    ("文獻尚未查證，卡片卻是confirmed", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 尚未查證"),
     "不能是 confirmed"),
    ("只讀摘要，locator沒寫摘要", lambda t: edit(S(t), "read_status: 全文已讀", "read_status: 只讀摘要"),
     "locator 要寫「摘要」"),
    ("科普當成實驗證據", lambda t: (add_popular(t), edit(C(t), "source: demo2000", "source: news2001")),
     "科普或新聞只能當 expression"),
    ("expression引用論文", lambda t: edit(C(t), "type: experiment", "type: expression"),
     "expression 只能引用"),
    ("證據類型亂寫", lambda t: edit(C(t), "type: experiment", "type: guess"), "type 要是"),
    ("有數字但units寫無數值", lambda t: edit(C(t), "units: m", "units: 無數值"), "units 不能寫「無數值」"),
    ("英文原文引用太長", lambda t: edit(C(t), "> a short quote", "> " + "word " * 60), "超過 50"),
    ("證據卡少原文依據", lambda t: edit(C(t), "## 原文依據\n> a short quote\n", ""), "「## 原文依據」"),
    ("自己的模擬指向不存在的檔案", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                     edit(C(t), "source: demo2000", "source: audition/nope.py")),
     "source 要是repo裡存在的檔案"),
    ("自己的模擬用..跳出repo", lambda t: (edit(C(t), "type: experiment", "type: our_simulation"),
                                    edit(C(t), "source: demo2000", "source: ../etc/passwd")),
     "source 要是repo裡存在的檔案"),
    ("related指到不存在的卡", lambda t: edit(C(t), "related:", "related: nope-card"), "related 的 nope-card 不存在"),
    ("卡片id跟檔名不同", lambda t: edit(C(t), "id: demo2000-claim", "id: other"), "跟檔名不一樣"),
    ("索引沒列卡片", lambda t: edit(t / "wiki" / "index.md", "(cards/demo2000-claim.md)", ""), "沒有列出證據卡"),
    ("放了PDF", lambda t: (t / "raw.pdf").write_bytes(b"%PDF-1.4"), "PDF不能放進repo"),
    ("檔案裡有像學號的數字", lambda t: (t / "note.md").write_text("學號 412345678\n", encoding="utf-8"),  # privacy-scan: ignore
     "像學號"),
    ("檔案裡有個人信箱", lambda t: (t / "note.md").write_text("someone@gmail.com\n", encoding="utf-8"),  # privacy-scan: ignore
     "電子郵件"),
    ("檔案裡有本機路徑", lambda t: (t / "note.md").write_text("C:\\Users\\me\\a.pdf\n", encoding="utf-8"),  # privacy-scan: ignore
     "本機路徑"),
    ("檔案裡有金鑰", lambda t: (t / "note.md").write_text("key=sk-" + "a" * 30 + "\n", encoding="utf-8"),
     "金鑰或Token"),
    ("檔案裡有手機號碼", lambda t: (t / "note.md").write_text("電話 0912-345-678\n", encoding="utf-8"),  # privacy-scan: ignore
     "手機號碼"),
    ("log裡的小數不能誤判成學號或電話", lambda t: (t / "run.log").write_text(
        "rate 1.412345678 / 0.0912345678\n", encoding="utf-8"), None),
    ("欄位重複", lambda t: edit(C(t), "status: confirmed", "status: confirmed\nstatus: pending"),
     "欄位 status 出現不只一次"),
    ("索引列了不存在的卡", lambda t: edit(t / "wiki" / "index.md", "人工寫的導覽。",
                                    "人工寫的導覽。見[舊卡](cards/deleted-card.md)。"),
     "cards/deleted-card.md 不存在"),
    ("有數字的主張，locator只寫全文", lambda t: edit(C(t), "locator: p.3 圖2", "locator: 全文"),
     "locator 要到頁碼"),
    ("自己的模擬指向不會上傳的檔案", our_card_to_ignored, "不會上傳的檔案"),
    ("歷史裡有金鑰：平常是警告", leak_then_remove, "金鑰或Token", {"warn": True}),
    ("歷史裡有金鑰：--strict是錯誤", leak_then_remove, "金鑰或Token", {"args": ["--strict"]}),
    ("歷史裡有PDF：--strict是錯誤", lambda t: (git(t, "init", "-q"), (t / "a.pdf").write_bytes(b"%PDF"),
                                         commit_all(t, "pdf"), (t / "a.pdf").unlink(), commit_all(t, "rm")),
     "出現過PDF：a.pdf", {"args": ["--strict"]}),
    ("有confirmed卡的論文才算進5篇", lambda t: None, "算進5篇的獨立論文 1 篇", {"out": True}),
    ("沒有confirmed卡的論文不算", lambda t: (edit(C(t), "status: confirmed", "status: pending"), rebuild(t)),
     "算進5篇的獨立論文 0 篇", {"out": True}),
    # 以下是雜湊值排除（2026-11-11，看到n3-package-r2.md的SHA-256被誤判成學號之後才加的）
    ("SHA-256表格裡的雜湊值不算學號", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None),
    ("SHA-256表格裡的雜湊值不算手機", note(SHA_TABLE + f"| `a.md` | `{fake_hash(PHONE)}` |\n"), None),
    ("SHA-256欄的雜湊後面接說明也排除",
     note("| 檔案 | SHA-256（第2輪後） |\n|---|---|\n" + f"| `a.md` | `{fake_hash(SID)}`（第2輪修改後） |\n"), None),
    ("同一行有SHA-256標記的雜湊值不算學號", note(f"PDF的SHA-256 `{fake_hash(SID)}`\n"), None),
    ("學號緊接中文照樣偵測", note(f"學號{SID}\n"), "像學號的9位數字"),
    ("學號夾在英文字母中照樣偵測", note(f"id{SID}x\n"), "像學號的9位數字"),
    ("沒有分隔的手機號碼照樣偵測", note(f"電話{PHONE}\n"), "手機號碼"),
    ("一般句子裡的學號照樣偵測", note(f"請{SID}同學到辦公室\n"), "像學號的9位數字"),
    ("沒有SHA-256標記的64位十六進位不放行", note(f"commit `{fake_hash(SID)}`\n"), "像學號的9位數字"),
    ("SHA-256欄裡只有63位不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID, 63)}` |\n"), "像學號的9位數字"),
    ("SHA-256欄裡沒有反引號不放行", note(SHA_TABLE + f"| `a.md` | {fake_hash(SID)} |\n"), "像學號的9位數字"),
    ("雜湊放在SHA-256以外的欄不放行",
     note("| 檔案 | SHA-256 | 備註 |\n|---|---|---|\n" + f"| `a.md` | `{fake_hash()}` | `{fake_hash(SID)}` |\n"),
     "像學號的9位數字"),
    ("表格結束後的雜湊不放行", note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` |\n\n`{fake_hash(SID)}`\n"),
     "像學號的9位數字"),
    ("SHA-256表格同一列的學號照樣偵測",
     note(SHA_TABLE + f"| `a.md` | `{fake_hash()}` | 學號{SID} |\n"), "像學號的9位數字"),
    ("SHA-256表格同一列的金鑰照樣偵測",
     note(SHA_TABLE + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"), "金鑰或Token"),
    ("歷史裡SHA-256表格的雜湊不算學號（--strict）",
     history_note(SHA_TABLE + f"| `a.md` | `{fake_hash(SID)}` |\n"), None, {"args": ["--strict"]}),
    ("歷史裡沒有標記的雜湊照樣抓（--strict）",
     history_note(f"commit `{fake_hash(SID)}`\n"), "像學號的9位數字", {"args": ["--strict"]}),
    # 以下是歷史掃描改讀完整檔案（2026-11-11，看到4462639的diff看不到表頭、雜湊被誤判之後才加的）
    ("歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     None, {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `sk-{'a' * 30}` | `{fake_hash(SID)}` |\n"),
     "金鑰或Token", {"args": ["--strict"]}),
    ("歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10), SHA_TABLE + rows(10) + f"| `學號{SID}` | `{fake_hash()}` |\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：表格結束很久之後加的雜湊照樣抓（--strict）",
     history_versions(SHA_TABLE + rows(10) + "\n說明\n" * 5,
                      SHA_TABLE + rows(10) + "\n說明\n" * 5 + f"`{fake_hash(SID)}`\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    ("歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）",
     history_versions("| 檔案 | 備註 |\n|---|---|\n" + rows(10),
                      "| 檔案 | 備註 |\n|---|---|\n" + rows(10) + f"| `x.md` | `{fake_hash(SID)}` |\n"),
     "像學號的9位數字", {"args": ["--strict"]}),
    # 以下是索引自動產生和同步檢查（2026-11-12，第2、3輪審查發現手寫的索引摘要沒跟著卡片更新之後才加的）
    ("改了卡片的主張沒重建索引要擋", lambda t: edit(C(t), "22台車繞230m的環", "22台車繞260m的環"), "不同步"),
    ("改了卡片的狀態沒重建索引要擋", lambda t: edit(C(t), "status: confirmed", "status: pending"), "不同步"),
    ("改了卡片的條件沒重建索引要擋", lambda t: edit(C(t), "conditions: 環狀道路", "conditions: 直線道路"), "不同步"),
    ("改了文獻的閱讀狀態沒重建索引要擋",
     lambda t: (edit(S(t), "read_status: 全文已讀", "read_status: 部分章節"), edit(S(t), "read_scope: 全文", "read_scope: 第1節")),
     "不同步"),
    ("新增卡片沒重建索引要擋",
     lambda t: (t / "wiki" / "cards" / "demo2000-second.md").write_text(CARD.replace("demo2000-claim", "demo2000-second"),
                                                                       encoding="utf-8"), "不同步"),
    ("手改自動產生的摘要要擋", lambda t: edit(t / "wiki" / "index.md", "22台車繞230m的環", "22台車繞環"), "不同步"),
    ("自動產生的標記被刪掉要擋",
     lambda t: edit(t / "wiki" / "index.md", "<!-- 自動產生結束 -->", ""), "找不到自動產生區塊的標記"),
    ("改了卡片也重建索引就通過", lambda t: (edit(C(t), "22台車繞230m的環", "22台車繞260m的環"), rebuild(t)), None),
    ("改人工寫的導覽不用重建", lambda t: edit(t / "wiki" / "index.md", "人工寫的導覽。", "人工寫的導覽，改過。"), None),
    ("主張裡的相對連結在索引裡改成從wiki出發",
     lambda t: (edit(C(t), "22台車繞230m的環。", "22台車繞230m的環，見[本卡](demo2000-claim.md)。"), rebuild(t),
                edit(t / "wiki" / "index.md", "見[本卡](cards/demo2000-claim.md)", "見[本卡](cards/demo2000-claim.md)")),
     None),
]


def main():
    fails = 0
    for case in CASES:
        name, breaker, expect = case[:3]
        opt = case[3] if len(case) > 3 else {}
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            make_site(tmp)
            breaker(tmp)
            code, out = run(tmp, *opt.get("args", []))
            if opt.get("warn"):
                warns = [l for l in out.splitlines() if l.startswith("[警告]") and expect in l]
                ok = code == 0 and bool(warns)
                want, got = f"沒有錯誤，警告裡有「{expect}」", out.strip().replace("\n", "；")
            elif opt.get("out"):
                ok = code == 0 and expect in out
                want, got = f"沒有錯誤，輸出裡有「{expect}」", out.strip().splitlines()[-2:]
            elif expect is None:
                ok = code == 0
                want, got = "沒有錯誤", ("沒有錯誤" if code == 0 else out.strip())
            else:
                ok = code == 1 and expect in out
                errs = [l for l in out.splitlines() if l.startswith("[錯誤]")]
                want, got = f"錯誤裡有「{expect}」", "；".join(errs) or "沒有錯誤"
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {name}\n    預期：{want}\n    實際：{got}")
    print(f"\n共{len(CASES)}個情境，失敗{fails}個。")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
```


========== 程式或執行輸出：runs/logs/2026-11-12-index-generation-tests.log ==========

```
[PASS] 正常資料
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡只有年份，units寫無數值
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 文獻少一個欄位
    預期：錯誤裡有「缺少欄位 venue」
    實際：[錯誤] wiki/sources/demo2000.md：缺少欄位 venue
[PASS] 閱讀狀態亂寫
    預期：錯誤裡有「read_status 要是」
    實際：[錯誤] wiki/sources/demo2000.md：read_status 要是 全文已讀、只讀摘要、尚未查證、部分章節 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] DOI格式錯
    預期：錯誤裡有「doi 格式不對」
    實際：[錯誤] wiki/sources/demo2000.md：doi 格式不對（寫 10.xxxx/... 或「無」）
[PASS] 網址不是https
    預期：錯誤裡有「url 要用 https://」
    實際：[錯誤] wiki/sources/demo2000.md：url 要用 https://
[PASS] 文獻少段落
    預期：錯誤裡有「缺少段落「## 限制」」
    實際：[錯誤] wiki/sources/demo2000.md：缺少段落「## 限制」
[PASS] 證據卡的文獻不存在
    預期：錯誤裡有「找不到」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source ghost1999 在 wiki/sources/ 裡找不到；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 文獻尚未查證，卡片卻是confirmed
    預期：錯誤裡有「不能是 confirmed」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 還是「尚未查證」，卡片不能是 confirmed；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 只讀摘要，locator沒寫摘要
    預期：錯誤裡有「locator 要寫「摘要」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：demo2000 只讀了摘要，locator 要寫「摘要」；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 科普當成實驗證據
    預期：錯誤裡有「科普或新聞只能當 expression」
    實際：[錯誤] wiki/cards/demo2000-claim.md：科普或新聞只能當 expression，不能當研究證據；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] expression引用論文
    預期：錯誤裡有「expression 只能引用」
    實際：[錯誤] wiki/cards/demo2000-claim.md：expression 只能引用 kind: popular 的文獻；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 證據類型亂寫
    預期：錯誤裡有「type 要是」
    實際：[錯誤] wiki/cards/demo2000-claim.md：type 要是 experiment、expression、model_theory、our_derivation、our_simulation、review 之一；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 有數字但units寫無數值
    預期：錯誤裡有「units 不能寫「無數值」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，units 不能寫「無數值」（要寫單位或「無因次」）
[PASS] 英文原文引用太長
    預期：錯誤裡有「超過 50」
    實際：[錯誤] wiki/cards/demo2000-claim.md：英文原文引用 60 個字，超過 50
[PASS] 證據卡少原文依據
    預期：錯誤裡有「「## 原文依據」」
    實際：[錯誤] wiki/cards/demo2000-claim.md：缺少段落或段落是空的「## 原文依據」
[PASS] 自己的模擬指向不存在的檔案
    預期：錯誤裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 audition/nope.py）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自己的模擬用..跳出repo
    預期：錯誤裡有「source 要是repo裡存在的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source 要是repo裡存在的檔案（找不到 ../etc/passwd）；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] related指到不存在的卡
    預期：錯誤裡有「related 的 nope-card 不存在」
    實際：[錯誤] wiki/cards/demo2000-claim.md：related 的 nope-card 不存在
[PASS] 卡片id跟檔名不同
    預期：錯誤裡有「跟檔名不一樣」
    實際：[錯誤] wiki/cards/demo2000-claim.md：id other 跟檔名不一樣
[PASS] 索引沒列卡片
    預期：錯誤裡有「沒有列出證據卡」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-claim
[PASS] 放了PDF
    預期：錯誤裡有「PDF不能放進repo」
    實際：[錯誤] raw.pdf：PDF不能放進repo
[PASS] 檔案裡有像學號的數字
    預期：錯誤裡有「像學號」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 檔案裡有個人信箱
    預期：錯誤裡有「電子郵件」
    實際：[錯誤] note.md:1：疑似電子郵件
[PASS] 檔案裡有本機路徑
    預期：錯誤裡有「本機路徑」
    實際：[錯誤] note.md:1：疑似本機路徑
[PASS] 檔案裡有金鑰
    預期：錯誤裡有「金鑰或Token」
    實際：[錯誤] note.md:1：疑似金鑰或Token
[PASS] 檔案裡有手機號碼
    預期：錯誤裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] log裡的小數不能誤判成學號或電話
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 欄位重複
    預期：錯誤裡有「欄位 status 出現不只一次」
    實際：[錯誤] wiki/cards/demo2000-claim.md：欄位 status 出現不只一次；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 索引列了不存在的卡
    預期：錯誤裡有「cards/deleted-card.md 不存在」
    實際：[錯誤] wiki/index.md：列出的 cards/deleted-card.md 不存在
[PASS] 有數字的主張，locator只寫全文
    預期：錯誤裡有「locator 要到頁碼」
    實際：[錯誤] wiki/cards/demo2000-claim.md：主張裡有數字，locator 要到頁碼、章節、公式或圖表編號（或寫「摘要」）
[PASS] 自己的模擬指向不會上傳的檔案
    預期：錯誤裡有「不會上傳的檔案」
    實際：[錯誤] wiki/cards/demo2000-claim.md：source local/sim.py 是不會上傳的檔案，別人沒辦法核對；[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 歷史裡有金鑰：平常是警告
    預期：沒有錯誤，警告裡有「金鑰或Token」
    實際：[警告] Git歷史 a19553d note.md：疑似金鑰或Token；[警告] wiki/sources：實際讀過、而且有confirmed證據卡的獨立論文 1 篇，還不到 5 篇；；文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。；錯誤 0 個，警告 2 個。
[PASS] 歷史裡有金鑰：--strict是錯誤
    預期：錯誤裡有「金鑰或Token」
    實際：[錯誤] Git歷史 a19553d note.md：疑似金鑰或Token
[PASS] 歷史裡有PDF：--strict是錯誤
    預期：錯誤裡有「出現過PDF：a.pdf」
    實際：[錯誤] Git歷史：出現過PDF：a.pdf
[PASS] 有confirmed卡的論文才算進5篇
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 1 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 1 篇），證據卡 1 張（pending 0 張）。', '錯誤 0 個，警告 1 個。']
[PASS] 沒有confirmed卡的論文不算
    預期：沒有錯誤，輸出裡有「算進5篇的獨立論文 0 篇」
    實際：['文獻 1 篇（算進5篇的獨立論文 0 篇），證據卡 1 張（pending 1 張）。', '錯誤 0 個，警告 1 個。']
[PASS] SHA-256表格裡的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256表格裡的雜湊值不算手機
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] SHA-256欄的雜湊後面接說明也排除
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 同一行有SHA-256標記的雜湊值不算學號
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 學號緊接中文照樣偵測
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 學號夾在英文字母中照樣偵測
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有分隔的手機號碼照樣偵測
    預期：錯誤裡有「手機號碼」
    實際：[錯誤] note.md:1：疑似手機號碼
[PASS] 一般句子裡的學號照樣偵測
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] 沒有SHA-256標記的64位十六進位不放行
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:1：疑似像學號的9位數字
[PASS] SHA-256欄裡只有63位不放行
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256欄裡沒有反引號不放行
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 雜湊放在SHA-256以外的欄不放行
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] 表格結束後的雜湊不放行
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:5：疑似像學號的9位數字
[PASS] SHA-256表格同一列的學號照樣偵測
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] note.md:3：疑似像學號的9位數字
[PASS] SHA-256表格同一列的金鑰照樣偵測
    預期：錯誤裡有「金鑰或Token」
    實際：[錯誤] note.md:3：疑似金鑰或Token
[PASS] 歷史裡SHA-256表格的雜湊不算學號（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史裡沒有標記的雜湊照樣抓（--strict）
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 864b843 note.md：疑似像學號的9位數字
[PASS] 歷史：SHA-256表格中間加一列，diff看不到表頭也排除（--strict）
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 歷史：SHA-256表格中間加的那列有金鑰照樣抓（--strict）
    預期：錯誤裡有「金鑰或Token」
    實際：[錯誤] Git歷史 79e993a note.md：疑似金鑰或Token
[PASS] 歷史：SHA-256表格中間加的那列有學號照樣抓（--strict）
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 25c343e note.md：疑似像學號的9位數字
[PASS] 歷史：表格結束很久之後加的雜湊照樣抓（--strict）
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 fe8248c note.md：疑似像學號的9位數字
[PASS] 歷史：沒有SHA-256欄的表格加雜湊照樣抓（--strict）
    預期：錯誤裡有「像學號的9位數字」
    實際：[錯誤] Git歷史 43f8e11 note.md：疑似像學號的9位數字
[PASS] 改了卡片的主張沒重建索引要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的狀態沒重建索引要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了卡片的條件沒重建索引要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 改了文獻的閱讀狀態沒重建索引要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 新增卡片沒重建索引要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py；[錯誤] wiki/index.md：沒有列出證據卡 demo2000-second
[PASS] 手改自動產生的摘要要擋
    預期：錯誤裡有「不同步」
    實際：[錯誤] wiki/index.md：跟文獻檔、證據卡不同步（自動產生的部分被手改，或卡片改了沒重建），請跑 python3 scripts/build_index.py
[PASS] 自動產生的標記被刪掉要擋
    預期：錯誤裡有「找不到自動產生區塊的標記」
    實際：[錯誤] wiki/index.md：找不到自動產生區塊的標記，請照原本的格式放回兩行標記，再跑 python3 scripts/build_index.py
[PASS] 改了卡片也重建索引就通過
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 改人工寫的導覽不用重建
    預期：沒有錯誤
    實際：沒有錯誤
[PASS] 主張裡的相對連結在索引裡改成從wiki出發
    預期：沒有錯誤
    實際：沒有錯誤

共69個情境，失敗0個。
```


========== 程式或執行輸出：runs/logs/2026-11-12-index-generation-build-check.log ==========

```
index.md跟文獻檔、證據卡同步
exit=0
```


========== 程式或執行輸出：runs/logs/2026-11-12-strict-before-r4.log ==========

```
文獻 6 篇（算進5篇的獨立論文 6 篇），證據卡 39 張（pending 0 張）。
錯誤 0 個，警告 0 個。
exit=0
```


========== 上一輪的審查意見原文 ==========

## 第一部分｜上一輪的問題逐條複核

本輪複核上一輪留下的 4 條「部分修好」和 11 條新問題，共 15 條。其中一條車數下限問題涉及兩張卡和一份推導，表中分三列，最後統計合計一條。

| 卡片id或檔案 | 上一輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |
|---|---|---|---|
| `nagel1992-bottleneck` | 開放邊界的比較基準，以及 \(v_{\max}=1\) 特例的更新方式 | 修好 | 主張已說明圖6是把開放邊界結果疊在環道基本圖上，並明列達到最大流量的特例同時要求 \(v_{\max}=1\) 和隨機逐車更新。符合第2227頁第4節、第2228頁圖6。ajp-jp1v2p2221 |
| `stern2018-wave-returns` | 把減弱寫成消除、B 場頁碼、教學說法適用範圍 | 修好 | A 調回 7.50 m/s 後的波與 C 的第二個波都寫成「減弱」。B 回復一般駕駛後波再現定位到第12頁。教學說法已把調快後復波的結果限定在 A 場。新增的 B 場敘述見第二部分。1705.01693v1 |
| `disputes.md`／22台分界 | 1.9595 缺少參數名稱和速度函數條件 | 修好 | 已寫明是敏感度 \(a\) 的分界，採 Bando 式（24）的速度函數、\(b=2\)、\(V'(b)=1\)。依 Bando 第1036–1038頁式（9）–（11）、（24）重算得 1.959493，與 Orosz 第4475–4476頁附錄 A 的代換結果一致。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) PTRSA2published |
| `disputes.md`／15 或 20 km/h | 簡報欄仍把兩種情境合成一個速度範圍 | 修好 | 簡報欄已並列 Nagel 第2228頁轉述的高速公路約 15 km/h、Sugiyama 第5–6頁和 Tadaki 第6–7頁報告的環道約 20 km/h，並交代 Nagel 未提供原始量測出處與方法。ajp-jp1v2p2221 NewJPhys_10_033001 NewJPhys_15_103034 |
| `ours-finite-n-threshold` | 首個失穩模態與有限環道通式缺少 \(N\ge3\) | 修好 | 主張及條件已列出 \(N\ge3\)。限制也交代 \(N=2\) 唯一的非零模態無有限失穩分界，可由 Bando 第1036頁式（10）核對。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) |
| `orosz2010-ring-stability` | 首個失穩模態缺少 \(N\ge3\) | 修好 | 主張已在 \(k=1\) 及其共軛模態先失穩之前加上 \(N\ge3\)。限制說明這個下限是 Wiki 從第4475–4476頁式（A2）、（A4）、（A6）推出的。PTRSA2published |
| `finite-n-threshold.md` | 推導第4–5步缺少 \(N\ge3\) | 修好 | 第4步、第5步及適用範圍均列出下限，並交代 \(N=2\) 的例外。將 \(\alpha=\pi\) 代入 Bando 第1036頁式（10），在 \(a>0\)、\(V'(b)>0\) 時兩根實部皆為負。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) |
| `stern2018-results` | A、B 的最佳控制時段與 C 的完整控制時段未區分 | 修好 | 條件及限制都已分開寫。第9頁表1、第11頁表2和第12頁表3可對出 A、B 各自的最佳區間，第13頁表4確認 C 使用第218–413秒的完整 PI 控制時段。1705.01693v1 |
| `tadaki2013-critical-density` | 圖8例外場次的停車條件與定點量測解讀 | 部分修好 | 主張已寫「停止或幾乎停止」和「基本圖接近自由流」。限制末尾仍寫「看不出塞車」。第10頁指出圖8雖近似自由流，平均速度仍略低、波動仍較大。建議限制也保留這兩項差異。NewJPhys_15_103034 |
| `tadaki2013-density-dependence` | 「同車數的其他場次」漏掉第一天的附錄 C | 修好 | 已分開列出第二天的附錄 B 和第一天的 1625、1730，後兩場可由第5頁表1、第17頁圖 C.1(b) 與第18頁圖 C.2(a) 核對。新增的資料使用範圍敘述見第二部分。NewJPhys_15_103034 |
| `tadaki2013-expressway-consistency` | 高速公路約 25 台/km 和約 120 km/h 的出處混在一起 | 修好 | 兩篇論文各自的第3頁圖1都標出約 25 台/km。約 120 km/h 已定位到 Tadaki 第11頁的比較敘述，並標出更早的數值來源待查。NewJPhys_15_103034 NewJPhys_10_033001 |
| `wiki/sources/sugiyama2008.md` | PDF 前置頁少算一頁 | 修好 | 典藏庫封面與出版商前置頁各一張，其後才是印刷第1頁。文獻檔的頁碼偏移量已改為 2。NewJPhys_10_033001 |
| `wiki/index.md`／`bando1995-capacity` | 把兩個 0.48 都寫成模擬結果 | 修好 | 摘要已區分塞車流的模擬估計和均勻流解的公式計算，符合第1041頁式（25）、（26）。摘要適用條件見第三部分。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) |
| `wiki/index.md`／`bando1995-linear-stability` | 速度函數的適用範圍與有限環道分界 | 修好 | 摘要已限定同一跟車方程式，區分長波極限 \(V'(b)=a/2\) 與有限環道的離散模態判定。可由第1036–1037頁式（9）–（12）核對。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) |
| `wiki/index.md`／`orosz2010-stability-approaches` | 把三種方法的結果無條件視為相同 | 修好 | 摘要已明列零延遲、有限環道保留 \(N\)、固定車距的大 \(N\) 極限與車隊條件一致。符合第4467頁及第4476頁式（A6）–（A10）。PTRSA2published |
| `wiki/index.md`／`orosz2010-delays` | 把短波先失穩寫成必然 | 修好 | 摘要已恢復「可能」，符合第4467頁。PTRSA2published |
| `wiki/index.md`／`ours-finite-n-threshold` | 直接把以 \(a\) 表示的有限分界與 \(a/2\) 比較 | 修好 | 兩個分界已統一用 \(a\) 表示。有限環道為 \(a=V'(b)[1+\cos(2\pi/N)]\)，長波極限為 \(a=2V'(b)\)。取極限的條件見第三部分。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com) |

## 第二部分｜新發現的問題

| 卡片id | 問題類型 | 嚴重程度 | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |
|---|---|---|---|---|---|
| `stern2018-wave-returns` | 忠實度 | 會誤導讀者 | Stern 第10頁、第11頁表2、第12頁 | 教學說法寫「實驗B、C沒有做這種速度調整」。B 確實把目標速度從 14 mph 提到 16 mph，而且調高後車速標準差降到該場最低。B 的波是在恢復一般跟車後再出現。1705.01693v1 | 寫明 A 場在調高目標速度、控制車平均速度超過車流後復波。B 場也調過目標速度，復波發生在停止執行控制策略後。C 場由控制器自行決定目標速度。 |
| `tadaki2013-density-dependence` | 忠實度 | 不精確 | Tadaki 第6頁第3段、第8頁圖5、第17–18頁附錄 C、第17–20頁附錄 E | 「1625 和 1730 沒有用在分析」範圍過廣。作者先比較兩天場次的平均車速及標準差，之後才把第一天非暖身場次排除在後續主要分析之外。附錄 E 也有第一天場次的基本圖。NewJPhys_15_103034 | 寫成「兩場未納入用來估計臨界密度的選定資料，時空圖仍列於附錄 C」。 |
| `orosz2010-ring-stability` | 推導 | 不精確 | Orosz 第4467頁、第4476頁式（A6）–（A8） | 「分界變成一個不分 \(k\) 的條件」容易被讀成所有波共用同一條分界。（A8）是取最先失穩的長波後得到的整體穩定條件。若在取極限時保留非零波數 \(q=2\pi k/N\)，（A6）仍含 \(\tan^2(q/2)\)。PTRSA2published | 寫成「固定均勻車距、令 \(N\to\infty\) 時，最先失穩的模態趨向長波極限，整體穩定條件化為（A8）」。 |
| `wiki/glossary.md`／相變 | 忠實度 | 不精確 | Sugiyama 第3、7頁，Tadaki 第11頁第4節 | 「比喻成動態的相變」弱化了作者實際提出的判斷。Sugiyama 把臨界密度處的穩定性改變解釋為非平衡相變。Tadaki 以實驗判定自由流與塞車流之間有動態相變，並保留相變階數的判斷。NewJPhys_10_033001 NewJPhys_15_103034 | 寫成「兩篇都以動態相變描述自由流到塞車流的轉變。Tadaki 認為轉變似乎是一階」。 |
| `wiki/sources/sugiyama2008.md` | 忠實度 | 小問題 | Sugiyama 第4頁圖2及實驗設定、第5–6頁圖4 | 限制把數字的來源概括為影片與圖上的估計。第4頁的 230 公尺、22 台是實驗設定，約 30 km/h 是給駕駛的巡航要求。第5–6頁約 20 km/h 才是依車輛軌跡得到的波速。NewJPhys_10_033001 | 分別標明場地與車數、駕駛的目標巡航速度、從軌跡估出的波速。 |

## 第三部分｜`index.md` 和證據卡、文獻檔不一致的地方

已逐列比對 39 張證據卡及 6 筆文獻。39 張卡的 `type`、`status` 和 6 筆文獻的 `kind` 均相符。下表列出摘要中會影響解讀的差異，以及一筆 `read_status` 欄位文字差異。

| 卡片id或文獻id | 索引寫的 | 卡片或文獻檔寫的 | 問題是什麼 |
|---|---|---|---|
| `orosz2010-ring-stability` | 環上 \(N\) 台車，零延遲時最長波先失穩 | \(N\ge3\) 才有這個首失穩模態。\(N=2\) 無有限分界 | 漏掉 \(N\ge3\)，讓結論涵蓋了卡片明列的例外。 |
| `stern2018-controllers` | 控制的想法是照車流平均速度開 | 以平均速度為目標，距離太近時以安全為先 | 缺少安全減速的優先條件，容易讀成控制車只要維持平均速度即可。 |
| `stern2018-results` | 比較表現最好的控制時段，車速變動、急煞、油耗都降低 | 基準為首個已出波且未控制的時段。A、B 取各自最佳區間，C 取完整 PI 控制時段。煞車使用第4.1節定義的事件指標 | 摘要欠缺比較基準和 C 的時段範圍。「急煞」也容易被當成一般急煞分類。 |
| `nagel1992-real-units` | 一格 7.5 公尺、一步約 0.5–1 秒 | 用塞車時每車占用長度及數種粗略換算估計，時間步的結論為秒量級 | 摘要省略估算性質，容易把這組換算當成模型固定的物理單位。 |
| `tadaki2013-density-dependence` | 車少順、車多塞，塞車團約 20 km/h 往後 | 圖4舉三場。約 20 km/h 是 30 台的 2030 場，34 台的 2534 場記錄的是慢速塞車團出現又消失 | 省略場次後，約 20 km/h 容易被讀成所有高密度場次的結果。 |
| `tadaki2013-metastable` | 中間密度時順暢和塞車都會出現 | 圖7(c)的三場中，基本圖在同一個密度附近有自由流和塞車兩種點 | 摘要漏掉「同一個密度附近」，也省略判讀依據是三場的基本圖。 |
| `tadaki2013-expressway-consistency` | 作者說跟高速公路的臨界密度一致 | 作者用速度相差三倍、所需車距約差三倍的比例作粗略比較 | 省略換算條件，容易被讀成兩邊的臨界密度數值直接相等。 |
| `tadaki2013-high-density` | 40 台時反而均勻，但作者說還不確定 | 第一天的單一 40 台場次觀察到均勻流。作者不確定的是這是否對應模型預測 | 摘要把單場結果寫成一般的 40 台情況，也模糊了作者不確定的對象。 |
| `bando1995-large-n-note` | 作者說車數和環長夠大時邊界條件不重要 | 作者討論的是採用環道的週期邊界條件 | 摘要把特定的邊界條件擴大成泛指各種邊界條件。 |
| `bando1995-velocity-function` | 簡單函數會倒車撞車，改用平移後的 `tanh` | 簡單函數在作者討論的失穩模擬中出現倒車，作者在單車道模型裡將它解讀為碰撞 | 漏掉失穩模擬的前提，讓倒車碰撞看起來是使用該函數就會發生的結果。 |
| `bando1995-spontaneous-jam` | 模擬中一台車偏 0.1，就長出 5 團塞車 | 指定參數的 100 台模擬，初始位置近乎等距、所有車由靜止出發，首車前移 0.1 | 「就長出 5 團」把特定初始條件和參數下的結果寫成普遍結果。 |
| `bando1995-capacity` | 模擬估計和均勻流解的通過量都約 0.48 | 兩值是在 \(N=100\)、\(L=200\) 的指定模型條件下比較 | 取得方式已同步，摘要仍缺少限定兩個數值的模擬條件。 |
| `ours-finite-n-threshold` | 有限環道分界及長波極限的公式 | Bando 跟車模型的小擾動分界，固定車距 \(b\)、增長環長時取大 \(N\) 極限 | 漏掉固定 \(b\) 的條件，容易把固定環長、增加車數的情況也讀成同一個極限。 |
| `ours-finite-n-simulation` | 模擬量到的 22 台分界跟推導相符 | 卡片分別報告 \(b=2\) 和 \(b=2.5\) 的兩個分界 | 摘要只留下車數，容易讓人以為 22 台有唯一的分界。 |
| `sugiyama2008-setup` | 約 30 km/h 起步 | 正式開始前，車已在環道以約 30 km/h、間距大致均勻地巡航 | 「起步」容易讀成由靜止加速，卡片描述的是開始記錄前已建立的巡航狀態。 |
| `sugiyama2008-23-vehicles` | 23 台也塞，速度一樣 | 23 台形成的**塞車團移動速度**和 22 台那場相同 | 摘要漏掉速度所指的對象，容易被讀成車輛行駛速度相同。 |
| `sugiyama2008-fundamental-diagram` | 高速公路基本圖，臨界密度約 25 台/km | 約 25 台/km 是圖1所用的單一地點、一個月資料的結果 | 摘要漏掉量測範圍，容易把該地點的數值當成高速公路通用值。 |
| `stern2018` | `全文已讀（arXiv預印本）` | `read_status` 為 `全文已讀`。`read_scope` 說明讀的是 arXiv v1 本文、表1–4 和部分附錄 | 欄位文字不完全相同。版本註記有文獻檔支持，可將版本與閱讀範圍放在獨立註記。 |

## 第四部分｜無法確認的地方

- `bando.pdf` 附件的掃描頁無法直接讀取。Bando 的核對採用同 DOI、同印刷頁碼的公開刊本 PDF。兩份檔案是否逐位元相同，無法確認。[courses.physics.ucsd.edu](https://courses.physics.ucsd.edu/2014/Spring/physics221a/REFERENCES/bando.pdf?utm_source=chatgpt.com)
- Bando 與 Orosz 的公式可重算 22 台、\(b=2\) 和 \(b=2.5\) 的解析分界。Wiki 自有程式的 RK4 執行、成長率、內插值、\(a=1.98\) 的衰減結果，以及手動比對至小數第10位的紀錄，需要 `audition/` 的程式與執行紀錄才能核實。n3-package-r3
- Tadaki 第5頁表1將 1110 標為 N/A，正文報告 19 場，附錄 C 報告第一天有 9 場。1110 標為 N/A 的原因，以及是否計入 19 場，原文未交代。NewJPhys_15_103034
- Tadaki 第11頁確實提到高速公路自由流約 120 km/h，但附上的 Sugiyama 第3頁圖1只有密度和流量，無法確認該速度的原始量測來源。Nagel 第2228頁轉述的高速公路約 15 km/h，同樣無法從這批 PDF 確認原始量測來源或方法。NewJPhys_15_103034 NewJPhys_10_033001 ajp-jp1v2p2221
- Sugiyama 第5頁腳註15未指名後續論文，無法確認當時特指 Tadaki 2013。這批 PDF 也不足以核實 Kerner 對瓶頸的具體立場，或把環道中的流態轉換歸因於某一次個別煞車。NewJPhys_10_033001 NewJPhys_15_103034

上一輪問題修好 14 條、部分修好 1 條、沒修好 0 條；新問題 5 條；索引不一致 18 條。
