# 審查包（第3輪）：確認上一輪的問題有沒有修好

## 你的角色

你是獨立審查者。上一輪你（或另一個審查者）對這份Wiki提出了意見，原文附在最後。整理的人逐條回到論文核對後修改了下面這些檔案。請對照同樣的6篇論文PDF，確認：

1. 上一輪列出的每一個問題，有沒有修好。
2. 修改有沒有引入新的錯誤（讀錯原文、數字或頁碼錯、把模型講成實驗、語氣過度）。整理的人有時也會改上一輪沒指出的地方，這些一樣要檢查。
3. `wiki/index.md`跟證據卡是否一致：索引裡每一列的類型、狀態和摘要，跟那張卡的`type`、`status`和「主張」有沒有不一樣，摘要有沒有比主張講得更強、或漏掉會改變意思的條件；文獻那張表的種類和閱讀狀態，跟文獻檔的`kind`、`read_status`是否相同。全部列都要看，不只這輪改過的。

這份審查包只完整放改過的檔案。沒改過的檔案上一輪已經看過，忠實度不用重看；最後的附錄只放它們的開頭欄位和「主張」，用來做第3項的核對。

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

第一部分，上一輪的問題逐條回覆，一張卡一列：

| 卡片id或檔案 | 上一輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |

第二部分，新發現的問題（沒有就寫「沒有」），格式跟上一輪的第一部分一樣：

| 卡片id | 問題類型 | 嚴重程度 | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |

第三部分，`index.md`和證據卡不一致的地方（沒有就寫「沒有」）：

| 卡片id或文獻id | 索引寫的 | 卡片或文獻檔寫的 | 問題是什麼 |

第四部分，無法確認的地方。

最後一行寫：上一輪問題修好幾條、部分修好幾條、沒修好幾條；新問題幾條；索引不一致幾條。


## 這份審查包包含的檔案版本

| 檔案 | SHA-256 |
|---|---|
| `wiki/cards/nagel1992-bottleneck.md` | `390d63652f68e79d0b2b8154ada5e02aab636f56badf982f4ca908c566e5b366` |
| `wiki/cards/orosz2010-ring-stability.md` | `af882f8e485b18893e07c476fd15c912dfa1d405a212effceaa129dd62fd7172` |
| `wiki/cards/ours-finite-n-threshold.md` | `90ca47668742e4fe565927b43cc37d1f98be1ed44d5d5b1699839330d0a3de9a` |
| `wiki/cards/stern2018-results.md` | `6c646aa9374adaa18cac7c3ba626e3aafa5e5f6a0b8cc631e6afb8aab08ee946` |
| `wiki/cards/stern2018-wave-returns.md` | `c083385769248305d2fc1d29ca63be81abe5cf5b2cd35439008c2651bf9be67b` |
| `wiki/cards/tadaki2013-critical-density.md` | `cc7a7d5b6c5665b7b8d6c28c2cf7856c6994fb5c8ca708d7bd1ab1af80191462` |
| `wiki/cards/tadaki2013-density-dependence.md` | `93f55762952a6a4adc9743d643950b382e317273d5bb70750598f542607c5730` |
| `wiki/cards/tadaki2013-expressway-consistency.md` | `866f64c147f861e072a1f3ab8ee1e51b52539c88bd7dd22a9f2c480a63b31bd4` |
| `wiki/derivations/finite-n-threshold.md` | `e9c973144d38ba4ffe3989e314597616d86ce37c7f92e61870ac22f918aeae66` |
| `wiki/disputes.md` | `b1ef0fd08a35c4c39f219e5979cf04999a24942c009b11180c89353960a7f022` |
| `wiki/glossary.md` | `daca7aedbd49a4e1bdd6ed86f43097769e6722841f4207dbef8e8572d7419b02` |
| `wiki/index.md` | `64d5d5632b1f9e6af6e16f97ee0078ed6a479c9a3c9f1d41f48706d9202f95f1` |
| `wiki/sources/sugiyama2008.md` | `0bb6874178c625d61444a44d38922eb0e71ec77063c8a09ac61073552a554220` |
| `wiki/cards/bando1995-capacity.md` | `9ec2145eab6e999bcce22d350cf8fd6baf3f8a5d5da6550d387910ecd6133c9e` |
| `wiki/cards/bando1995-cluster-values.md` | `507fff3823e47ea893003ed2ec887de1e9b8b2c107ffdd35a5a514570c20d5d7` |
| `wiki/cards/bando1995-large-n-note.md` | `114108267408dcbcce044c9780d8f695049a759281a889171ceb525c403ed1d0` |
| `wiki/cards/bando1995-linear-stability.md` | `9373d6bd06979be539f18d21cc510c49dc59387a220e6bc415070881ec8ca4b2` |
| `wiki/cards/bando1995-no-delay.md` | `527e89639f6d403e14ea511d978df1332796f8ef9ab50ac895878d1b8c5cba27` |
| `wiki/cards/bando1995-ovm-equation.md` | `66d6c10c8dc13e5f787a7dc3c6464d37fed6eec208dcbf2f5b5e5ce747120153` |
| `wiki/cards/bando1995-spontaneous-jam.md` | `adfbc601430f51f481bc4d3ec65fb4fd27322212f65e7771950d051fd0f94afd` |
| `wiki/cards/bando1995-stable-regions.md` | `4341b82ffec1ec800591c1b601e789a5bee7f79bf169c9e491e3fee48f4cb0c4` |
| `wiki/cards/bando1995-velocity-function.md` | `6694d775771202064a8b0df7349917a5ca3a0ce3de7436ba8e6060b9848d3b1a` |
| `wiki/cards/nagel1992-circle-jams.md` | `11d952d1a97abd63a048bcf2f91ead24b526f8440024687239a3efda7e1012f1` |
| `wiki/cards/nagel1992-randomization.md` | `228d143002bd566baf9e7241935de8a8d775a9bcb87c2f49896f820851cb521b` |
| `wiki/cards/nagel1992-real-units.md` | `187abaef28bcd048211ace931ff6e0e764b60916da8a9e29e52b4b80837eb63a` |
| `wiki/cards/nagel1992-rules.md` | `68e4f0053e2fc64fcd2880a4c7e9d4f911175b9207aba42013f46b4d9db7d276` |
| `wiki/cards/nagel1992-transition.md` | `cff003b1c465855d10ecfce4ef4043524886c790892d017344f0d735392cf392` |
| `wiki/cards/orosz2010-delays.md` | `d9c562f5d7016899e6905612496f9f7d6564253edca9b78ec99c8d61445a6bab` |
| `wiki/cards/orosz2010-ovm-family.md` | `3ec4021e1c01e64462dab467a21e4d8e9edff5b7e8138bbab6a567a2c61ea5c2` |
| `wiki/cards/orosz2010-stability-approaches.md` | `b18ce4b79567da3b13973d8bded3db23905c8854625c42c03db056ab44a8f317` |
| `wiki/cards/ours-finite-n-simulation.md` | `e1d21332119095e1f4a59e155db96bb56dc901156c9abc1e9e0f4ed327a3cc7c` |
| `wiki/cards/stern2018-controllers.md` | `780ebe4917f2ece75e94a36aab12cc86fc07fd48e87e8c1dbfb0b645e54c253f` |
| `wiki/cards/stern2018-setup.md` | `285eb37718f26659de9a323a779108245859ccf0e8f10f2fd935377cecf06e39` |
| `wiki/cards/stern2018-waves-emerge.md` | `2ec922b1026dc7c4571f94c520ac1f6788bfd9c1dc5671fab60c6abb7d1a0161` |
| `wiki/cards/sugiyama2008-23-vehicles.md` | `59a1918f28237f05d49bf2d6f87fa272f2f3b52c7a50b613110f5e667ee088d7` |
| `wiki/cards/sugiyama2008-backward-wave.md` | `7c805e9157bead59c55e004ae342ca3c8bd68059641fcb69f3790497aba6893c` |
| `wiki/cards/sugiyama2008-fundamental-diagram.md` | `5b4e275cf71d7576e7aa5c4f3c9f2528bab4cee02dd90d6e73286b61d9145e6d` |
| `wiki/cards/sugiyama2008-highway-comparison.md` | `1821b3ebdfa55608111d23ca1c8428c0ca89c1e5c94b5b79d19e6daf92b818b7` |
| `wiki/cards/sugiyama2008-jam-emerges.md` | `52ada92ad185baee982284c6d9c8e9f2a1583845612e089d18681b04ce4974ca` |
| `wiki/cards/sugiyama2008-mechanism.md` | `edc56ceed98ead16bc7064cfddb41d9f8e09df920594445a7091ddbaebb79288` |
| `wiki/cards/sugiyama2008-setup.md` | `b49e2bf508faee3154534651e6c9748f8172b5f0c1c5e2bcb9eb0af629c01e13` |
| `wiki/cards/tadaki2013-high-density.md` | `21a9268b67acebb561d6d5efedb9a79295bac2e0a297759bb32485de932c315e` |
| `wiki/cards/tadaki2013-metastable.md` | `1825a7fad619e863ce2625f04adac717afdd73c9fbeca4843b4117efab7a26eb` |
| `wiki/cards/tadaki2013-setup.md` | `f0fbf5b2b1ca5762eb2f3779d37198f4623035eb789df7e79d7d1cdb5e89cb3a` |
| `wiki/sources/bando1995.md` | `fa31a7abc9f7265f818f479dc4e92b4f7f7eb8d7806316324c2a75b94a47ecc6` |
| `wiki/sources/nagel1992.md` | `3b2d4e6facadd89f4e5ebf57a14cb67e586512eed18fa59690e7202db04c8825` |
| `wiki/sources/orosz2010.md` | `0ccdc9adeabfc3ff3f8c29794dae350fca93faf088587526e291e965aade7676` |
| `wiki/sources/stern2018.md` | `dddbab143c9aec53262e7ea21843b7ba4d94611dba23c8e6ec9b87fc29889e09` |
| `wiki/sources/tadaki2013.md` | `820a2f2c9cf91befb7078f6411b119c6ab4fd4a0ecbdec11e35876a30e988f1a` |

# 以下是要審查的Wiki內容



========== 檔案：wiki/cards/nagel1992-bottleneck.md ==========

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

## 原文依據

第2227頁第4節說明開放邊界的設定，模擬放鬆之後密度<ρ_c>=0.069±0.002、流量<q_c>=0.304±0.001。第2227頁同一節說v_max=1、隨機逐車更新時，系統會自己走到最大流量ρ=1/2，但這似乎不適用於v_max>1。第2228頁圖6的十字是開放邊界的結果，曲線是環道的長時間平均；圖說寫這個自我組織的瓶頸狀態並不在流量的最大值，跟v_max=1時不同。

## 限制

- 模型裡的瓶頸是邊界條件，跟真實道路的匝道或隧道不同。
- 這張卡跟「瓶頸是不是塞車成因」的討論有關，但這篇沒有直接回答那個問題。


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

（這是綜述附錄裡的數學推導，所以類型是model_theory。）在沒有反應延遲的跟車模型裡，環上N台車時，非零的波各有穩定分界，k和N−k是一對共軛、共用同一條分界；N是偶數時k=N/2沒有有限的分界。N≥3時，越過分界時最先失去穩定的是k=1（和它的共軛N−1，最長的波）。車數趨近無限多（均勻車距固定）時，分界變成一個不分k的條件(A8)。

## 原文依據

第4475頁附錄A把式(5.1)在沒有延遲時寫成(A1)，用環上N台車的解得到(A3)，開N次方後回到(A2)，波數只能是(A4)的2kπ/N。第4476頁(A6)是第k個波穩定性改變的條件，作者說從F小往大越過分界時系統「更不穩定」，因此最先失去穩定的是k=1；N趨近無限大時條件變成(A8)。第4467頁也說，沒有延遲時穩定性會先在低頻、長波（k=1）失去。

> Consequently, the stability loss occurs for the lowest wavenumber

## 限制

- 這是一般模型的公式，用F、G、H表示。代入Bando的模型（W=0、車長0）得到22台車分界的那一步是我們做的，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。
- 只適用沒有延遲的情況，見[orosz2010-delays](orosz2010-delays.md)。
- (A6)含tan²(kπ/N)，k=N/2時發散，所以那個波沒有有限的Hopf分界；作者也寫只有k≤N/2的分界出現在F、G、H>0的範圍。
- 原文沒有寫車數下限。N=2時唯一非零的波就是k=N/2=1，沒有有限的分界，所以「k=1最先失穩」要N≥3才有意義；這個條件是我們從(A6)看出來的。


========== 檔案：wiki/cards/ours-finite-n-threshold.md ==========

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

## 原文依據

這是我們推的，不是論文寫的，完整推導在`wiki/derivations/finite-n-threshold.md`。推法：bando1995式(11)的臨界曲線是f=a/(2cos²(α/2))，式(9)的α_k=2πk/N只能取這幾個值，把α_k代進去，第k個波不穩定的條件是f>a/(2cos²(πk/N))；k=1時右邊最小。f=V'(b)。

另外拿Orosz 2010附錄A對照：取W=0、沒有延遲、不計車長，代入F=aV'、G=0、H=a。直接代進式(A2)得到的特徵方程式跟Bando式(10)相同；代進(A6)得到同一個分界。Orosz也寫明沒有延遲時最先不穩定的是k=1。G=0是Orosz附錄所討論參數範圍（F、G、H>0）的邊界。

## 限制

- 我們自己推的。Orosz 2010的公式是一般跟車模型的，把它對應到Bando模型（W=0、沒有延遲、不計車長）的那一步是我們做的，Orosz沒有直接算Bando模型22台的分界。
- 只適用沒有延遲的模型；Orosz第4467頁說延遲夠大時，可能改成短的波先失去穩定。
- 只對很小的擾動成立。
- 要N≥3。N=2時唯一非零的波是k=N/2=1，不會失穩，沒有這個分界。
- 差別只有約2%，對一般讀者不重要，放在進階展開區。


========== 檔案：wiki/cards/stern2018-results.md ==========

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

## 原文依據

第12頁表3列出三場實驗「波剛出現時」和「控制開啟時表現最好的時段」的車速標準差、油耗、急煞次數和通過量，以及變化百分比。第13頁第4.2節末段整理成四點：車速標準差在三場都下降、油耗都下降、急煞大幅減少（從每車每公里8.58～9.66次降到最差2.47次、最好0.12次）、通過量A和B增加、C略降。

> The velocity standard deviation is reduced in all experiments

## 限制

- 表3的控制時段：A、B有好幾段控制時段（表1、表2），取各自表現最好的一段，不是整段控制期間的平均；C只有一段控制時段，就是第218～413秒的整段PI控制（表4）。
- 每種控制器只有一場，沒有統計檢定。
- 油耗降幅內文和表3有小差異（B：22.0%和22.1%；C：27.9%和28.1%），這裡用表3。
- 實驗C的控制器只用自己的資訊，平均速度略降，所以通過量反而少一點。


========== 檔案：wiki/cards/stern2018-wave-returns.md ==========

---
id: stern2018-wave-returns
type: experiment
source: stern2018
locator: 第10頁實驗A、第12頁實驗B、第13頁實驗C、第14頁圖5
conditions: 實驗A調整目標速度；實驗A、B關閉控制之後；實驗C控制期間
units: m/s
status: confirmed
related: stern2018-results
---

## 主張

控制不是開了就一勞永逸：實驗A把目標速度從7.50調到8.00 m/s、比車流平均還快時，波又出現了；實驗A、B關掉控制後波也回來了；實驗C在控制期間又產生了第二個波，這個波也被減弱。

## 原文依據

第10頁說實驗A在目標7.50 m/s時，控制車的速度幾乎剛好等於車流平均、不需要減速；調到8.00 m/s時平均比車流快，又引發了波，調回7.50 m/s後波再次被減弱（原文dampened），控制器關掉後波又出現。第12頁說實驗B回到一般駕駛後波又出現。第13頁說實驗C的控制消除了一開始的波，但控制期間又產生了一個波，第二個波也被減弱（原文damped）。

> which inevitably induces a wave again

## 限制

- 只有這幾場的觀察，沒有說明「目標速度要設多少」的一般規則。

## 教學說法

在實驗A裡，那台車的目標速度剛好接近大家的平均時，減弱波的效果最好；把目標速度調得比大家快，波又回來了。實驗B、C沒有做這種速度調整，不能拿來支持這個說法。


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
- 基本圖是在環道上三個定點量的，停住的車不會被算進流量和平均速度。塞車團裡有停止或幾乎停止的車的場次，依定點通過資料繪出的基本圖接近自由流，看不出塞車（第10頁）。


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

- 圖4只各挑一場當例子。第二天同車數的其他場次在附錄B；第一天的25台（1625）和30台（1730）沒有用在分析，時空圖在附錄C。作者沒有對重複場次做統計比較。
- 約20 km/h跟Sugiyama 2008的數字相同，是同一群作者在不同場地量到的。


========== 檔案：wiki/cards/tadaki2013-expressway-consistency.md ==========

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

## 原文依據

第11頁拿高速公路的臨界密度（自由流約120 km/h時約每公里25台）跟實驗比較（自由流約40 km/h，臨界密度0.08～0.09每公尺），用車距跟車速成正比的說法認為兩者一致。

> As a car will require a headway that is three times larger when driving three times faster, our measured experimental critical density is consistent with values observed on the expressway.

## 限制

- 自由流約120 km/h：Tadaki第11頁引用Sugiyama 2008，但Sugiyama 2008的圖1只有密度和流量，我們在那篇裡找不到120 km/h這個數字，出處待查證。約每公里25台則兩篇的圖1都寫了。
- 「車速三倍、車距三倍」是作者採用的粗略比例，不是嚴格的推導。照這個比例，環道的臨界密度換算成高速公路約每公里26.7～30台（我們自己算的：0.08～0.09台／公尺除以3），跟25台是近似的比較。
- 這段解決了Sugiyama 2008那張基本圖卡片裡「高速公路25台/km跟環道密度不能直接比」的問題的一部分，但只是作者的論證。


========== 檔案：wiki/derivations/finite-n-threshold.md ==========

# 有限車數時的穩定分界（我們的推導）

這份是我們自己的推導，不是任何一篇論文直接寫的。證據卡`ours-finite-n-threshold`指向這份。

## 從Bando 1995推

1. Bando 1995第1036頁式(9)：環上N台車，擾動只能拆成α_k = 2πk/N（k = 0, 1, ..., N−1）這幾種波。
2. 第1037頁式(11)：分開穩定和不穩定的臨界曲線是f = a / (2cos²(α/2))，其中f = V'(b)（式(7)）。f比這條曲線大，那個波就會變大。
3. 把α_k代進去：第k個波在V'(b) > a / (2cos²(πk/N)) 時變大。
   - k = 0：式(10)的解是z = 0和z = −a，分別是整體平移和會衰減的共同速度擾動，不算失穩。
   - k和N − k是一對共軛，分界相同（N ≥ 3時，k = 1和k = N − 1是第一對）。
   - N是偶數時，k = N/2的cos(πk/N) = 0，上面的式子會除以0，要直接用式(10)：z² + az + 2aV'(b) = 0。a > 0、V'(b) > 0時兩個根的實部都小於0，這個波不會失穩。
4. 以下要N ≥ 3。（N = 2時唯一非零的波就是k = 1 = N/2，依第3步的二次式不會失穩，沒有有限的分界。）在1 ≤ k < N/2的範圍裡，k = 1時cos²(π/N)最大，右邊最小，所以a從大往小調時，最先變不穩定的是k = 1和k = N − 1這一對。
5. 分界（N ≥ 3）：V'(b) = a / (2cos²(π/N))，也就是a = 2V'(b)cos²(π/N) = V'(b)(1 + cos(2π/N))（用2cos²x = 1 + cos2x）。
6. N = 22、b = 2（V'(2) = 1）：a = 1 + cos(2π/22) ≈ 1.9595。如果固定車距b = 2、讓環長跟著車數一起變長，N越大越接近2，也就是Bando式(12)的V'(b) < a/2；一般來說，固定b時分界趨近2V'(b)。如果是固定環長、增加車數，b = L/N和V'(b)都會跟著變，就不是這個極限。

## 跟Orosz 2010對照

Orosz 2010附錄A（第4475～4476頁）處理的是一般的跟車模型。

**它的設定：**
- 線性化後的式(5.1)、(A1)用三個係數F、G、H。
- 依式(5.2)：F = ∂f/∂h，G = ∂f/∂ḣ，H = −∂f/∂v，都在均勻車流的位置取值。

**它的結果：**
- 環上N台車時，式(A6)給出第k個波穩定性改變的條件：F = ½(2G+H)[(2G+H)tan²(kπ/N) + H]。
- 作者寫明，沒有延遲時，穩定性最先在k = 1失去；N趨近無限大時，條件變成式(A8)：F < ½(2G+H)H。

**怎麼對應到Bando的模型（這一步是我們做的）：**
- Orosz第4462頁式(3.12)的OV模型是f = (V(h) − v)/T + W(ḣ)。取W = 0，延遲全部為0（Orosz第4462頁說這種設定就是Bando 1995用的），就是Bando的式(1)，其中a = 1/T。
- 代入得到F = V'(h*)/T = aV'，G = 0，H = 1/T = a。
- Orosz的h是扣掉車長ℓ的車距，環長是L + Nℓ；Bando不考慮車長，相當於ℓ = 0，兩邊的均勻車距都是L/N。

**最直接的核對：**把F = aV'、G = 0、H = a代進Orosz的式(A2)，得到z² + az − aV'(e^{iq} − 1) = 0，跟Bando式(10)完全相同（q對應α）。特徵方程式一樣，後面的分界自然一樣。另外，G = 0落在Orosz附錄討論的參數範圍（F、G、H > 0）的邊界上。

**代入(A6)的結果：**
- G = 0代進(A6)：F = ½H²(1 + tan²(kπ/N)) = H² / (2cos²(kπ/N))。
- 再代入F = aV'、H = a：aV' = a² / (2cos²(kπ/N))，也就是V' = a / (2cos²(kπ/N))，跟上面第3步一樣。
- k = 1時跟第5步一樣；N趨近無限大時，(A8)變成aV' < a²/2，也就是V' < a/2，跟Bando式(12)一樣。

數值上，用`audition/ovm.py`的`critical_a`和上面從Orosz代入的公式，各算N = 22、30、100、10⁶，V' = 1和0.7864兩組，結果到小數第10位都相同（2026-11-11手動跑過，這個比對沒有存成檔案；兩者在代數上本來就相同，因為2cos²x = 1 + cos2x）。獨立審查時，審查者表示這個數值比對和我們的模擬結果無法從論文核對，因為不在論文裡。

## 適用範圍

- 只對很小的擾動成立。
- 第4～5步的分界要N ≥ 3。
- 只適用沒有延遲、W = 0（不看相對速度）、所有駕駛相同的模型。Orosz第4467頁提到，延遲夠大時可能改成短的波（k大）先失去穩定，這時上面的結論不一定成立。
- 這份推導說明的是「模型」在22台時的分界，不代表真實駕駛的分界。


========== 檔案：wiki/disputes.md ==========

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
| 相變 | phase transition | 相轉變 | tadaki2013、sugiyama2008；作者把順暢變塞車比喻成動態的相變 |
| 反應延遲 | reaction time, delay | 反應時間 | orosz2010第4462頁；Bando 1995沒有加 |
| 跟車模型 | car-following model | — | orosz2010第4461頁；每台車看前車決定怎麼開的模型 |
| 自動駕駛車 | autonomous vehicle, AV | 自駕車 | stern2018；這篇的車只有速度自動控制，方向盤由人操作 |
| 平滑車 | — | — | 我們簡報裡自己取的名字，指「照平均速度穩定開的那台車」，不是論文用語 |


========== 檔案：wiki/index.md ==========

# 幽靈塞車Wiki索引

這份Wiki整理「沒有事故為什麼也會塞車」的研究，是教學簡報的知識來源。每篇文獻和每張證據卡都要列在這裡，`scripts/check_wiki.py`會檢查。

- 術語：[glossary.md](glossary.md)
- 研究差異與未解問題：[disputes.md](disputes.md)
- 簡報頁面和證據卡的對照：[slide-map.md](slide-map.md)
- 我們自己的推導：[derivations/finite-n-threshold.md](derivations/finite-n-threshold.md)

## 文獻

| id | 種類 | 閱讀狀態 | 檔案 |
|---|---|---|---|
| bando1995 | paper | 全文已讀 | [sources/bando1995.md](sources/bando1995.md) |
| nagel1992 | paper | 全文已讀 | [sources/nagel1992.md](sources/nagel1992.md) |
| tadaki2013 | paper | 全文已讀 | [sources/tadaki2013.md](sources/tadaki2013.md) |
| orosz2010 | paper | 部分章節 | [sources/orosz2010.md](sources/orosz2010.md) |
| stern2018 | paper | 全文已讀（arXiv預印本） | [sources/stern2018.md](sources/stern2018.md) |
| sugiyama2008 | paper | 全文已讀 | [sources/sugiyama2008.md](sources/sugiyama2008.md) |

## 證據卡

| id | 類型 | 狀態 | 主張 | 檔案 |
|---|---|---|---|---|
| orosz2010-ovm-family | review | confirmed | OV模型在跟車模型裡的位置；零延遲是Bando的設定 | [cards/orosz2010-ovm-family.md](cards/orosz2010-ovm-family.md) |
| orosz2010-stability-approaches | review | confirmed | 沒有延遲時：有限環道的分界跟車數N有關，車數趨近無限多（車距固定）時跟一排車的條件一致 | [cards/orosz2010-stability-approaches.md](cards/orosz2010-stability-approaches.md) |
| orosz2010-ring-stability | model_theory | confirmed | 環上N台車，沒有延遲時最先不穩定的是最長的波 | [cards/orosz2010-ring-stability.md](cards/orosz2010-ring-stability.md) |
| orosz2010-delays | review | confirmed | 延遲夠大時，可能改成短的波先不穩定 | [cards/orosz2010-delays.md](cards/orosz2010-delays.md) |
| stern2018-setup | experiment | confirmed | 260公尺環道、21～22台車、一台可自動控制速度 | [cards/stern2018-setup.md](cards/stern2018-setup.md) |
| stern2018-waves-emerge | experiment | confirmed | 三場全部由人開時都出現走走停停波 | [cards/stern2018-waves-emerge.md](cards/stern2018-waves-emerge.md) |
| stern2018-controllers | experiment | confirmed | 控制的想法：照車流平均速度開 | [cards/stern2018-controllers.md](cards/stern2018-controllers.md) |
| stern2018-results | experiment | confirmed | 比較表現最好的控制時段：車速變動、急煞、油耗都降低，C的通過量略降 | [cards/stern2018-results.md](cards/stern2018-results.md) |
| stern2018-wave-returns | experiment | confirmed | A的目標速度調得比車流快、A和B關掉控制後，波又回來；C控制期間出現第二個波也被減弱 | [cards/stern2018-wave-returns.md](cards/stern2018-wave-returns.md) |
| nagel1992-rules | model_theory | confirmed | 格子模型的4條規則 | [cards/nagel1992-rules.md](cards/nagel1992-rules.md) |
| nagel1992-randomization | model_theory | confirmed | 作者說隨機減速是這個模型像真實交通的關鍵 | [cards/nagel1992-randomization.md](cards/nagel1992-randomization.md) |
| nagel1992-circle-jams | model_theory | confirmed | 密度高時塞車隨機出現、往後移動 | [cards/nagel1992-circle-jams.md](cards/nagel1992-circle-jams.md) |
| nagel1992-transition | model_theory | confirmed | 轉變在每格約0.08台附近，確切位置不清楚 | [cards/nagel1992-transition.md](cards/nagel1992-transition.md) |
| nagel1992-real-units | model_theory | confirmed | 一格7.5公尺、一步約0.5～1秒 | [cards/nagel1992-real-units.md](cards/nagel1992-real-units.md) |
| nagel1992-bottleneck | model_theory | confirmed | 瓶頸情境下車流自己穩定在某個狀態 | [cards/nagel1992-bottleneck.md](cards/nagel1992-bottleneck.md) |
| tadaki2013-setup | experiment | confirmed | 名古屋巨蛋314公尺環道，10～40台車 | [cards/tadaki2013-setup.md](cards/tadaki2013-setup.md) |
| tadaki2013-density-dependence | experiment | confirmed | 車少順、車多塞，塞車團約20 km/h往後 | [cards/tadaki2013-density-dependence.md](cards/tadaki2013-density-dependence.md) |
| tadaki2013-critical-density | experiment | confirmed | 作者估的臨界密度在每公尺0.08到0.09台之間 | [cards/tadaki2013-critical-density.md](cards/tadaki2013-critical-density.md) |
| tadaki2013-metastable | experiment | confirmed | 中間密度時順暢和塞車都會出現 | [cards/tadaki2013-metastable.md](cards/tadaki2013-metastable.md) |
| tadaki2013-expressway-consistency | experiment | confirmed | 作者說跟高速公路的臨界密度一致 | [cards/tadaki2013-expressway-consistency.md](cards/tadaki2013-expressway-consistency.md) |
| tadaki2013-high-density | experiment | confirmed | 40台時反而均勻，但作者說還不確定 | [cards/tadaki2013-high-density.md](cards/tadaki2013-high-density.md) |
| bando1995-ovm-equation | model_theory | confirmed | 跟車方程式：加速度＝a×(想開的速度－現在速度) | [cards/bando1995-ovm-equation.md](cards/bando1995-ovm-equation.md) |
| bando1995-linear-stability | model_theory | confirmed | 同一個跟車方程式下，長波極限的分界是V'(b)=a/2；有限環道要逐一看離散的波 | [cards/bando1995-linear-stability.md](cards/bando1995-linear-stability.md) |
| bando1995-large-n-note | model_theory | confirmed | 作者：車數和環長夠大時邊界條件不重要 | [cards/bando1995-large-n-note.md](cards/bando1995-large-n-note.md) |
| bando1995-velocity-function | model_theory | confirmed | 簡單函數會倒車撞車，改用tanh(Δx−2)+tanh2 | [cards/bando1995-velocity-function.md](cards/bando1995-velocity-function.md) |
| bando1995-spontaneous-jam | model_theory | confirmed | 模擬：一台車偏0.1，就長出5團往後移動的塞車 | [cards/bando1995-spontaneous-jam.md](cards/bando1995-spontaneous-jam.md) |
| bando1995-cluster-values | model_theory | confirmed | 塞住後分成幾乎停住和接近全速兩種 | [cards/bando1995-cluster-values.md](cards/bando1995-cluster-values.md) |
| bando1995-stable-regions | model_theory | confirmed | 在這個模型和參數下：很稀疏或很密集時穩定，中間密度不穩定 | [cards/bando1995-stable-regions.md](cards/bando1995-stable-regions.md) |
| bando1995-capacity | model_theory | confirmed | 塞車流的模擬估計和均勻車流解的計算值，通過量都約0.48 | [cards/bando1995-capacity.md](cards/bando1995-capacity.md) |
| bando1995-no-delay | model_theory | confirmed | 模型刻意不加反應延遲 | [cards/bando1995-no-delay.md](cards/bando1995-no-delay.md) |
| ours-finite-n-threshold | our_derivation | confirmed | 都用a表示時，有限環道（N≥3）的分界是a=V'(b)(1+cos(2π/N))，長波極限是a=2V'(b)；22台、b=2時是1.9595 | [cards/ours-finite-n-threshold.md](cards/ours-finite-n-threshold.md) |
| ours-finite-n-simulation | our_simulation | confirmed | 模擬量到的22台分界跟推導相符 | [cards/ours-finite-n-simulation.md](cards/ours-finite-n-simulation.md) |
| sugiyama2008-setup | experiment | confirmed | 環道實驗：230公尺、22台車、約30 km/h起步 | [cards/sugiyama2008-setup.md](cards/sugiyama2008-setup.md) |
| sugiyama2008-jam-emerges | experiment | confirmed | 均勻車流自己變成走走停停 | [cards/sugiyama2008-jam-emerges.md](cards/sugiyama2008-jam-emerges.md) |
| sugiyama2008-backward-wave | experiment | confirmed | 塞車團以約20 km/h往後傳，車子進進出出 | [cards/sugiyama2008-backward-wave.md](cards/sugiyama2008-backward-wave.md) |
| sugiyama2008-highway-comparison | experiment | confirmed | 作者說這個速度跟高速公路上的塞車波差不多 | [cards/sugiyama2008-highway-comparison.md](cards/sugiyama2008-highway-comparison.md) |
| sugiyama2008-23-vehicles | experiment | confirmed | 23台車也塞，速度一樣 | [cards/sugiyama2008-23-vehicles.md](cards/sugiyama2008-23-vehicles.md) |
| sugiyama2008-mechanism | model_theory | confirmed | 三個層次分開：作者對模型的說明、環道實驗的觀察、作者對瓶頸的解釋 | [cards/sugiyama2008-mechanism.md](cards/sugiyama2008-mechanism.md) |
| sugiyama2008-fundamental-diagram | experiment | confirmed | 高速公路基本圖，臨界密度約每公里25台 | [cards/sugiyama2008-fundamental-diagram.md](cards/sugiyama2008-fundamental-diagram.md) |


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
- 數字幾乎都是「約」「roughly」，是從影片和圖讀出來的估計值。
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


========== 上一輪的審查意見原文 ==========

## 第一部分｜上一輪問題逐條複核

按上一輪的 29 張卡、`disputes.md` 的 8 條，以及推導文件的 3 項意見計數。頁碼採論文印刷頁碼，Stern 採上傳的 arXiv v1 頁碼。

| 卡片id或檔案 | 上一輪的問題 | 修好了嗎（修好／部分修好／沒修好） | 說明 |
|---|---|---|---|
| `bando1995-capacity` | 兩個 0.48 的取得方式 | 修好 | 卡片已區分塞車流的模擬估計與均勻流解的公式計算，符合第1041頁式（25）（26）。索引仍有同一處表述問題，見第二部分。bando |
| `bando1995-cluster-values` | 圖9頁碼、50台的判定條件 | 修好 | 已標為第1041頁圖9，並補上車距小於2才計入擁擠區，符合第1040–1041頁。bando |
| `bando1995-large-n-note` | 用有限車數推導判斷真車實驗的邊界影響 | 修好 | 已限定為同一週期邊界模型內的比較。第1036頁只說車數與環長要夠大，未給22台實驗的判定。bando |
| `bando1995-linear-stability` | \(a/2\) 的適用範圍、速度函數的範圍 | 修好 | 卡片已區分長波極限與有限環道的離散波數，並把 \(V\) 限定在同一跟車方程內。依據是第1036–1037頁式（9）–（12）。索引仍需同步。bando |
| `bando1995-ovm-equation` | 把無因次列成一般模型條件 | 修好 | 已改為原文未指定物理單位。由第1036頁式（1）可知，採物理單位時 \(a\) 的量綱是時間的倒數。bando |
| `bando1995-spontaneous-jam` | 把初始靜止寫成已在巡航 | 修好 | 第1038頁引用第1037頁式（17）–（19）。修訂稿正確寫出第1台位置前移0.1、其他車維持等距位置、所有車初速為零。bando |
| `bando1995-velocity-function` | 混淆目標速度與實際速度、過度保證不超車 | 修好 | 已寫明 \(V(0)=0\) 指目標速度，並把無倒車與無超越的描述限定於作者討論的模擬情境。見第1036頁式（1）、第1038頁式（24）、第1039頁圖5。bando |
| `nagel1992-bottleneck` | 開放邊界與環道的比較基準、\(v_{\max}=1\) 特例 | 部分修好 | 圖6的比較基準已修正，原文依據也補了隨機逐車更新。主張仍只寫 \(v_{\max}=1\)，建議把更新方式也放進主張。第2227頁第4節的特例同時有這兩個條件。ajp-jp1v2p2221 |
| `nagel1992-real-units` | 原文 0.7 秒與算式不符 | 修好 | 已區分第2228頁印出的約 0.7 秒和按 \(2.25/4.2\) 重算的約 0.54 秒，並保留作者的秒量級結論。ajp-jp1v2p2221 |
| `nagel1992-rules` | 隨機減速適用範圍、把一步寫成一秒 | 修好 | 主張已加 \(v>0\)，教學說法使用「時間步」。符合第2222頁第2節與第2227–2228頁的粗估換算。ajp-jp1v2p2221 |
| `nagel1992-transition` | 把流量峰值的尺寸效應寫成轉變點移動 | 修好 | 已區分約 0.08 台／格附近的轉變、流量峰值的尺寸效應，以及確切轉變點未定。符合第2224–2225頁、圖4。ajp-jp1v2p2221 |
| `orosz2010-ovm-family` | 車距定義的式號、物理量綱 | 修好 | 已把 \(h_n\) 的定義定位在式（3.7）前，並保留距離、速度與鬆弛時間的量綱。見第4461–4462頁。PTRSA2published |
| `orosz2010-ring-stability` | 證據類型、共軛模態、偶數車數的特殊模態、量綱 | 修好 | 已標為 `model_theory`，補上共軛模態、\(k=N/2\) 無有限 Hopf 分界及係數量綱。附錄式（A2）（A6）（A7）支持這些修正。車數下限另見第二部分。PTRSA2published |
| `orosz2010-stability-approaches` | 把三種方法的結果無條件視為相同 | 修好 | 卡片已補上附錄的零延遲設定、有限環道的離散波數，以及固定車距的大 \(N\) 極限。符合第4467頁及式（A6）–（A10）。索引仍需同步。PTRSA2published |
| `ours-finite-n-threshold` | 零模態、共軛對、偶數模態及延遲語氣 | 修好 | 已補 \(k=0\)、\(k\) 與 \(N-k\) 的關係、\(k=N/2\) 的處理，以及延遲下「可能」先出現短波。22台、\(b=2\) 的 1.9595 可由原式重算。車數下限另見第二部分。bando PTRSA2published |
| `stern2018-controllers` | 前車速度的估算、B 的人工策略、38秒視窗的定位 | 修好 | 第5頁支持用車距變化估算前車速度，第6頁有38秒，第8頁第3.4節交代 B 由受訓駕駛執行。修訂稿均已補上。1705.01693v1 |
| `stern2018-results` | 車隊統計被讀成逐車結果、節號錯誤、煞車指標 | 修好 | 已明寫車隊及時段合併計算的標準差，使用第4.1節的過度煞車指標，並將結果定位到表3與第4.2節末段。控制期的例外另見第二部分。1705.01693v1 |
| `stern2018-setup` | 駕駛指示漏了禁止貼車、CAT 車半徑偏移 | 修好 | 已補空隙拉大才追上、禁止貼車，以及 CAT 車向外偏半個車寬，符合第5頁。1705.01693v1 |
| `stern2018-wave-returns` | 把減弱寫成消除、B 的頁碼、教學說法的範圍 | 部分修好 | A 調回 7.50 m/s 及 C 的第二個波均已改為減弱，B 的定位也改到第12頁。教學說法仍用「這幾場」概括開得較快會讓波回來。第10頁直接報告這項速度調整與復波的是 A。1705.01693v1 |
| `stern2018-waves-emerge` | B、C 首次出波的頁碼 | 修好 | A 的79秒在第9頁，B 的55秒與 C 的161秒在第10頁，也能與表1、2、4對照。1705.01693v1 |
| `sugiyama2008-fundamental-diagram` | 把速度列入圖1的變數 | 修好 | 已改為密度與流量，符合第3頁圖1的兩軸。NewJPhys_10_033001 |
| `sugiyama2008-jam-emerges` | 斷言無人故意踩煞車 | 修好 | 教學說法已改用第4–5頁報告的駕駛指示、車距波動與短暫停車。NewJPhys_10_033001 |
| `sugiyama2008-mechanism` | 混用模型、觀察與瓶頸解釋，先行判定研究不衝突 | 修好 | 已區分第3頁的模型、第4–5頁的環道觀察，以及摘要與第7頁的瓶頸解釋。高密度比較與 Kerner 的具體立場已留待確認。NewJPhys_10_033001 |
| `tadaki2013-critical-density` | 省略2030、2934兩場的基本圖例外 | 修好 | 已補兩場確有塞車、圖8另列、以及定點量測主要記錄通過車輛。臨界密度 \(0.08\)–\(0.09\) 台／公尺保留正確。新用語的精度見第二部分。NewJPhys_15_103034 |
| `tadaki2013-density-dependence` | 2125場次的波動種類、附錄涵蓋範圍 | 修好 | 已恢復第6頁的「密度波動」，並明列1110未出現在附錄B、C。「同車數其他場次」的限制另見第二部分。NewJPhys_15_103034 |
| `tadaki2013-expressway-consistency` | 40 km/h 的來源、三倍車距的論證強度 | 修好 | 已寫出第10頁的擬合係數與第11頁的粗略比例。依該比例換算 26.7–30 台／公里，算術正確。高速公路的數值出處另見第二部分。NewJPhys_15_103034 |
| `tadaki2013-high-density` | 讓人以為40台資料全被排除 | 修好 | 已交代1940場次列入圖5及第12頁討論，排除範圍限於用來估計臨界密度的選定資料。NewJPhys_15_103034 |
| `tadaki2013-metastable` | 圖7(c)場次、局部與全環平均密度、踩煞車歸因 | 修好 | 已正確列出2228、2328、2830，將2030另列圖8，區分兩種密度，並移除踩煞車與運氣的歸因。符合第5–6、9–10頁。NewJPhys_15_103034 |
| `tadaki2013-setup` | 暖身場次錯誤、1110計數不明 | 修好 | 已改為三場10台及一場12台，並保留第5頁表1、正文與附錄C的計數差異。NewJPhys_15_103034 |
| `disputes.md`／瓶頸 | 移除「可能是3」，區分觀察與解釋 | 修好 | 已保留分類4。Sugiyama 第4–5頁支持特定環道條件下無瓶頸也會塞，第7頁交代作者的解釋。NewJPhys_10_033001 |
| `disputes.md`／極高密度 | 把40台結果限定為單一觀察 | 修好 | 已保留分類4，寫明第一天單一場次觀察到均勻流，以及作者尚未確認是否對應模型預測。見 Bando 圖10、Tadaki 第12頁。bando NewJPhys_15_103034 |
| `disputes.md`／實驗與模擬波速 | 比較前要建立長度與時間尺度 | 修好 | 已寫明換算條件。Sugiyama 第5–6頁的約 20 km/h 可核對，Wiki 自己的模擬設定列在第三部分。NewJPhys_10_033001 |
| `disputes.md`／22台分界 | 區分有限環道、大 \(N\) 極限及自有模擬 | 部分修好 | 離散波數、固定車距的極限、自有模擬的證據範圍均已補齊。這列仍直接寫「22台的分界1.9595」，少了所求參數 \(a\) 與 \(V'(b)=1\) 的條件。建議明列式（24）的速度函數與 \(b=2\)。bando PTRSA2published |
| `disputes.md`／反應延遲 | 恢復「可能」先出現短波 | 修好 | 已恢復「可能」，符合 Orosz 第4467頁。Bando 無顯式延遲的描述也符合第1035、1042頁。PTRSA2published bando |
| `disputes.md`／隨機減速與不穩定 | 分開擾動來源和擾動演化 | 修好 | 已區分 Nagel 第2222頁的隨機減速與 Bando 式（17）–（19）先設定的位置擾動。兩篇環道觀察也沒有被用來排除其中一個模型。ajp-jp1v2p2221 bando |
| `disputes.md`／15或20 km/h | 移除測法不同的斷言，按條件並列 | 部分修好 | 正文已按高速公路轉述與環道觀察並列，並註明 Nagel 未交代測法。簡報欄仍把數值合成「十幾到二十公里」的通用說法，宜在簡報也標明各自條件。ajp-jp1v2p2221 NewJPhys_10_033001 NewJPhys_15_103034 |
| `disputes.md`／平滑車示範 | 分清 Stern 的 A、B、C 與 Wiki 示範 | 修好 | 已分別標出 A 的 FollowerStopper、B 的受訓駕駛和 C 的飽和 PI 控制，符合第3頁、第3節與第4.2節。1705.01693v1 |
| `finite-n-threshold.md`／模態 | \(k=0\)、共軛對及 \(k=N/2\) | 修好 | 已補式（10）的零模態兩根 \(0,-a\)，也正確處理偶數 \(N\) 時的二次式。通式的車數下限另見第二部分。bando |
| `finite-n-threshold.md`／Orosz 代換 | 直接核對（A2），標明 \(G=0\) 的位置 | 修好 | 已用 \(F=aV'\)、\(G=0\)、\(H=a\) 得到與 Bando 式（10）相同的特徵方程，也說明 \(G=0\) 位在附錄所述正參數區的邊界。PTRSA2published bando |
| `finite-n-threshold.md`／取極限 | 明寫固定車距或固定環長 | 修好 | 已明寫固定 \(b\) 才有 \(a_{\mathrm c}\to2V'(b)\)，以及固定環長時 \(b=L/N\) 會變。與 Orosz 第4467頁的固定均勻車距設定一致。PTRSA2published |

## 第二部分｜新發現的問題

| 卡片id | 問題類型 | 嚴重程度 | 原文在哪裡 | 問題是什麼 | 建議怎麼改 |
|---|---|---|---|---|---|
| `ours-finite-n-threshold`、`orosz2010-ring-stability`、`finite-n-threshold.md` | 推導 | 不精確 | Bando 第1036頁式（9）（10），Orosz 第4475–4476頁式（A2）（A4）（A6）。bando PTRSA2published | 推導第3步已提 \(N\ge3\)，但第4–5步及兩張卡的通則仍未帶上這項條件。\(N=2\) 時唯一的非零模態就是 \(k=N/2=1\)，依修訂稿自己的二次式，在正參數下沒有有限失穩分界。 | 在「第一對失穩模態」與通式前明列 \(N\ge3\)。22台的計算值仍為 1.9595。 |
| `stern2018-results` | 忠實度 | 不精確 | 第9頁表1、第11頁表2、第12頁表3、第13頁表4。1705.01693v1 | 限制說表3的比較時段一律排除整段控制期。A、B 有多個控制時段可選。C 只有一個控制時段，第218–413秒，表3的 C 就使用這段。 | 寫成「A、B 取各自表現最佳的控制時段，C 使用完整的 PI 控制時段」。 |
| `tadaki2013-critical-density` | 忠實度 | 小問題 | 第10頁圖8及說明、第11頁第4節。NewJPhys_15_103034 | 新增文字把「停止或幾乎停止」縮成「有停住的車」，並用「失真」概括量測結果。原文具體說明定點統計取自通過的車，因此圖形接近自由流。 | 保留「停止或幾乎停止」，用「依定點通過資料繪出的基本圖接近自由流」描述結果。 |
| `tadaki2013-density-dependence` | 忠實度 | 小問題 | 第5頁表1、附錄B、第17頁圖C.1(b)、第18頁圖C.2(a)。NewJPhys_15_103034 | 限制仍說「同車數的其他場次在附錄B」。第一天的25台1625及30台1730也屬同車數場次，兩者都在附錄C。 | 加上「第二天」限定，或把附錄B、C都列出。 |
| `tadaki2013-expressway-consistency` | 忠實度 | 不精確 | Tadaki 第3頁圖1、第11頁第4節，Sugiyama 第3頁圖1。NewJPhys_15_103034 NewJPhys_10_033001 | 條件欄把高速公路的數字一併歸給 Sugiyama。兩份 PDF 都可核對約25台／公里。約120 km/h 的自由流速度在 Tadaki 第11頁的比較敘述中，Sugiyama 圖1只有密度與流量。 | 將約25台／公里定位到基本圖，約120 km/h 定位到 Tadaki 第11頁的敘述。 |
| `wiki/sources/sugiyama2008.md` | 忠實度 | 小問題 | 所附 `NewJPhys_10_033001.pdf` 第1–3個 PDF 頁面。NewJPhys_10_033001 | 文獻頁寫 PDF 前面只多一張封面。檔案先有典藏庫封面及出版商前置頁，期刊第1頁從第3個 PDF 頁面開始。 | 改成「本 PDF 有兩張前置頁，PDF 頁碼比期刊頁碼多2」。 |
| `wiki/index.md`／`bando1995-capacity` | 忠實度 | 不精確 | Bando 第1041頁式（25）（26）。bando | 「這組模擬裡有沒有塞車，運輸量都約0.48」仍讓兩個值看起來都來自模擬。 | 寫成「塞車流的模擬估計和均勻流解的計算值都約0.48」。 |
| `wiki/index.md`／`bando1995-linear-stability` | 忠實度 | 不精確 | Bando 第1036–1037頁式（9）–（12）。bando | 摘要仍寫「對任何速度函數都成立」，未交代同一跟車方程的範圍及有限環道的分界。 | 寫成「同一跟車模型下，長波極限的分界為 \(V'(b)=a/2\)，有限環道依離散模態判定」。 |
| `wiki/index.md`／`orosz2010-stability-approaches` | 條件比較 | 會誤導讀者 | Orosz 第4467頁、第4475–4476頁式（A6）–（A10）。PTRSA2published | 摘要仍寫三種方法結果相同，沒有帶出零延遲與有限環道保留 \(N\) 的條件。 | 寫成「零延遲時，有限環道分界依賴 \(N\)，大 \(N\) 極限與鏈式車隊條件對應」。 |
| `wiki/index.md`／`orosz2010-delays` | 忠實度 | 不精確 | Orosz 第4467頁，附錄A之前的延遲討論。PTRSA2published | 摘要仍把延遲足夠大時短波先失穩寫成必然。 | 補成「延遲夠大時，可能先在短波失穩」。 |
| `wiki/index.md`／`ours-finite-n-threshold` | 推導 | 不精確 | Bando 第1036–1037頁式（7）（9）–（12）。bando | 摘要將以 \(a\) 表示的有限分界直接與 \(a/2\) 比較。式（12）是拿 \(V'(b)\) 與 \(a/2\) 比較。 | 若都用 \(a\) 表示，並列有限環道的 \(a_{\mathrm c}=V'(b)[1+\cos(2\pi/N)]\) 與長波極限的 \(a_{\mathrm c}=2V'(b)\)。 |

## 第三部分｜無法確認的地方

- 六篇 PDF 可核對22台的解析分界。Wiki 自有模擬的初始條件、無因次設定、RK4 執行結果、成長率、內插值，以及手動比對到小數第10位的紀錄，無法從這六篇 PDF 確認。
- Tadaki 表1把1110列為 N/A。正文報告19場，附錄C報告第一天9場。原文未交代1110標為 N/A 的原因或是否計入19場。NewJPhys_15_103034
- Tadaki 第3頁明確把自己的研究稱為先前環道實驗的延伸。Sugiyama 腳註15沒有指名後續論文，因此無法確認腳註當時特指 Tadaki 2013。NewJPhys_10_033001 NewJPhys_15_103034
- Kerner 對瓶頸的具體主張、Nagel 所提高速公路約15 km/h的原始量測來源與方法，以及個別煞車動作是否觸發環道中的流態轉換，均無法由這批 PDF 確認。NewJPhys_10_033001 ajp-jp1v2p2221 NewJPhys_15_103034

上一輪問題修好 36 條、部分修好 4 條、沒修好 0 條；新問題 11 條。
