# 審查包：幽靈塞車Wiki的研究差異與忠實度審查

## 你的角色

你是獨立審查者。這份Wiki是另一個AI依6篇論文整理的，整理的人沒有參與這次審查。請對照我同時上傳的論文PDF，檢查證據卡有沒有讀錯原文。你的意見不會被直接採用，有爭議的地方我們會再回原文核對，所以請只寫你在PDF裡確認得到的事，不確定就寫不確定。

## 上傳的PDF和對應的文獻id

| 文獻id | 檔案 | 注意 |
|---|---|---|
| bando1995 | bando.pdf | 掃描檔，頁碼看頁首的1035～1042 |
| sugiyama2008 | NewJPhys_10_033001.pdf | 前面多一張典藏庫封面，頁碼看頁首的1～7 |
| nagel1992 | ajp-jp1v2p2221.pdf | 掃描檔，頁碼2221～2229 |
| tadaki2013 | NewJPhys_15_103034.pdf | 前面多兩頁，頁碼看頁首 |
| stern2018 | 1705.01693v1.pdf | arXiv預印本，頁碼就是PDF頁碼 |
| orosz2010 | PTRSA2published.pdf | 頁碼4455～4479；Wiki只讀了部分章節，見文獻檔的read_scope |

## 要檢查的五件事

1. **忠實度**：每張卡的「主張」和「原文依據」有沒有讀錯、誇大、或漏掉會改變意思的條件。數字、單位、頁碼、圖表和式子編號對不對。
2. **證據類型**：`type`有沒有放錯。experiment是論文裡真實車輛的實驗或觀測；model_theory是論文裡的模型、推導或電腦模擬；review是綜述的整理；our_derivation、our_simulation是我們自己的。特別注意：有沒有把模型或模擬的結果寫得像真實道路已經證實。
3. **條件能不能比**：卡片之間或`disputes.md`裡拿來比較的東西，條件（車數、環長、密度單位、有沒有因次、實驗或模型）是不是真的能比。
4. **研究差異的分類**：`disputes.md`每一條的分類（1假設或方法不同、2條件不同、3結論真的衝突、4資料不足）和「目前判斷」合不合理，有沒有被強行統一或選邊。
5. **我們自己的推導**：`derivations/finite-n-threshold.md`從Bando 1995式(9)(11)和Orosz 2010附錄A推出22台車分界的過程，代換和適用條件有沒有錯。

不用檢查中文文筆，也不用提新的研究方向。

## 請照這個格式回覆

第一部分，有問題的卡片，一張一列（沒問題的不用列）：

| 卡片id | 問題類型（忠實度／證據類型／條件比較／分類／推導） | 嚴重程度（會誤導讀者／不精確／小問題） | 原文在哪裡（頁、段、式、圖） | 問題是什麼 | 建議怎麼改 |

第二部分，`disputes.md`各條的意見。

第三部分，推導文件的意見。

第四部分，你沒辦法確認的地方（例如掃描檔看不清楚、PDF裡找不到），列出來就好，不要猜。

最後一行寫：總共檢查了幾張卡、有問題的幾張。


## 這份審查包包含的檔案版本

| 檔案 | SHA-256 |
|---|---|
| `wiki/glossary.md` | `33247e391f43781218f9fe3e8c44d65ad7d248eeb0528825e1df7399d91d8986` |
| `wiki/disputes.md` | `c327c402aa6ed6e10b0e53b77c406fac16aea91afc95f7ba7f5e97b907b700e7` |
| `wiki/derivations/finite-n-threshold.md` | `130de7fe08a720321ea909eed9580d1da2f221883665918b5d9807220140ffc4` |
| `wiki/sources/bando1995.md` | `fa31a7abc9f7265f818f479dc4e92b4f7f7eb8d7806316324c2a75b94a47ecc6` |
| `wiki/sources/nagel1992.md` | `3b2d4e6facadd89f4e5ebf57a14cb67e586512eed18fa59690e7202db04c8825` |
| `wiki/sources/orosz2010.md` | `0ccdc9adeabfc3ff3f8c29794dae350fca93faf088587526e291e965aade7676` |
| `wiki/sources/stern2018.md` | `dddbab143c9aec53262e7ea21843b7ba4d94611dba23c8e6ec9b87fc29889e09` |
| `wiki/sources/sugiyama2008.md` | `3f8ea04764d68b79f29625bf97f7c0c64683096b493f34fed66c0b307f7f53c9` |
| `wiki/sources/tadaki2013.md` | `820a2f2c9cf91befb7078f6411b119c6ab4fd4a0ecbdec11e35876a30e988f1a` |
| `wiki/cards/bando1995-capacity.md` | `8e68f40f8cc22169e4af2c51b4ae485ce71bb399cd8223c666a4eb1db116e76a` |
| `wiki/cards/bando1995-cluster-values.md` | `c3cca9ac121c98078ae0c7e711837e8519f304144244bc11669baf136dc2c686` |
| `wiki/cards/bando1995-large-n-note.md` | `5357722ead23b1482fc3cee17d8255d35879b65c9c6f11d45e1c261793896be4` |
| `wiki/cards/bando1995-linear-stability.md` | `a70fe50a9d65c5cbf0048e57125d8a29fc93239e33bc79fbd66f4149839d0cf5` |
| `wiki/cards/bando1995-no-delay.md` | `527e89639f6d403e14ea511d978df1332796f8ef9ab50ac895878d1b8c5cba27` |
| `wiki/cards/bando1995-ovm-equation.md` | `ca17434288d8b9f1fe3941b64c8fe652664d05264636a0afdb738a5e1cf01d94` |
| `wiki/cards/bando1995-spontaneous-jam.md` | `aa6a80284bfddc0545b7089dcab4e44edc8c4730ae1d7888504ca8f3a197706d` |
| `wiki/cards/bando1995-stable-regions.md` | `4341b82ffec1ec800591c1b601e789a5bee7f79bf169c9e491e3fee48f4cb0c4` |
| `wiki/cards/bando1995-velocity-function.md` | `535e554e39f50ad30abe544fdda42244073a886880c7970fc22dbffb5b89355e` |
| `wiki/cards/nagel1992-bottleneck.md` | `87e3f9f192a83b8355790a1f4a779eeb9dd0ff5d1b5876179c346fcdaa02ff34` |
| `wiki/cards/nagel1992-circle-jams.md` | `11d952d1a97abd63a048bcf2f91ead24b526f8440024687239a3efda7e1012f1` |
| `wiki/cards/nagel1992-randomization.md` | `228d143002bd566baf9e7241935de8a8d775a9bcb87c2f49896f820851cb521b` |
| `wiki/cards/nagel1992-real-units.md` | `3b33653a0e8b1156dd235ce89929df761acf129e886dd610a56d6a365ca6a9ff` |
| `wiki/cards/nagel1992-rules.md` | `36c8da9b06d4a6fde9f7f3715d5d9deab754b4cf9b2146109f052b65142d10a4` |
| `wiki/cards/nagel1992-transition.md` | `23a07b5e66fa82a38f43062d4a2f1656e7b5f140d0e0a4dfa70790eaeb5d1031` |
| `wiki/cards/orosz2010-delays.md` | `d9c562f5d7016899e6905612496f9f7d6564253edca9b78ec99c8d61445a6bab` |
| `wiki/cards/orosz2010-ovm-family.md` | `4325a00881e378b3a391c7c0a18f6b46e476c3fb83673daec185672d3cfb0c7d` |
| `wiki/cards/orosz2010-ring-stability.md` | `aae7729f8a8858196bcb98cf4628edb07a64b77c07d2a52e4529c8a375d3dad5` |
| `wiki/cards/orosz2010-stability-approaches.md` | `cf4e4f89b218ea69557583643f77a313b96d1166079af273e08e05b07552605e` |
| `wiki/cards/ours-finite-n-simulation.md` | `e1d21332119095e1f4a59e155db96bb56dc901156c9abc1e9e0f4ed327a3cc7c` |
| `wiki/cards/ours-finite-n-threshold.md` | `b1bf04167fec5ef215cc04461de0bc9c613f77b8a7ef37e6170851fd30d34985` |
| `wiki/cards/stern2018-controllers.md` | `e8d62c1c754b1ca8ddde48358fe60d8c88efd3bf294c8a4e33487efc0474fd98` |
| `wiki/cards/stern2018-results.md` | `343353d10cce44fa240426ef9c9bac6c216e4a1afdac9197a27ba1603230c047` |
| `wiki/cards/stern2018-setup.md` | `e8cbca3443070e6157432c02f31e590c4329efa6990189f4bb47a0d9f778a48c` |
| `wiki/cards/stern2018-wave-returns.md` | `b5289336150658b2ecaa249ef94973713467ca1be40fec1334fa4fc39617c04c` |
| `wiki/cards/stern2018-waves-emerge.md` | `c7c4308389e3fd67b1288a82833564d9578f4f26836ec37fb60852abe2c1fedd` |
| `wiki/cards/sugiyama2008-23-vehicles.md` | `59a1918f28237f05d49bf2d6f87fa272f2f3b52c7a50b613110f5e667ee088d7` |
| `wiki/cards/sugiyama2008-backward-wave.md` | `7c805e9157bead59c55e004ae342ca3c8bd68059641fcb69f3790497aba6893c` |
| `wiki/cards/sugiyama2008-fundamental-diagram.md` | `0a50ee930019d2159775d9c0fb2f812d8abcca3d0ee881dbade56f7b9441ae86` |
| `wiki/cards/sugiyama2008-highway-comparison.md` | `1821b3ebdfa55608111d23ca1c8428c0ca89c1e5c94b5b79d19e6daf92b818b7` |
| `wiki/cards/sugiyama2008-jam-emerges.md` | `7625bb1a2a10ac85dabcf5ccdecd3022a4926793dd2e3584ef4150fb0b1ebdcc` |
| `wiki/cards/sugiyama2008-mechanism.md` | `c171dd6f4282607bef9d5000cc745cf61346e5b4e7b0f05b48dc43e5c66eb688` |
| `wiki/cards/sugiyama2008-setup.md` | `b49e2bf508faee3154534651e6c9748f8172b5f0c1c5e2bcb9eb0af629c01e13` |
| `wiki/cards/tadaki2013-critical-density.md` | `c282e8d16f2a712f2efc24bfbce150a08f0762abb7752dd2002431443ca02090` |
| `wiki/cards/tadaki2013-density-dependence.md` | `84bf481c7b740bcfe38382bd063c6b2ee500d81590abb62ce21aba8ad3d74444` |
| `wiki/cards/tadaki2013-expressway-consistency.md` | `88aa82c866fd4ca0e4f37069b8819cd91a2d1e7e4d57d506b32e78185422af2b` |
| `wiki/cards/tadaki2013-high-density.md` | `0f6e68d8b83e9bc100bb80c41e103be3a44a8a76aa6bc479f1113a52106c9e7c` |
| `wiki/cards/tadaki2013-metastable.md` | `fed8c09566c533314e3e8ed05efe2d7e3412c3b10443b0990bfd7f3e71dd2823` |
| `wiki/cards/tadaki2013-setup.md` | `0acf79282f951bd83c9906c48a2951742de11dce8b853347df959dc1a1e07e9e` |

# 以下是要審查的Wiki內容



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
| NaSch模型 | Nagel–Schreckenberg model | — | 指nagel1992提出的模型；這個簡稱是後來文獻的叫法 |
| 隨機減速 | randomization | 隨機化 | nagel1992第2222頁第3步；暫定譯名 |
| 介穩態 | metastable state | 亞穩態 | tadaki2013第10頁；同一個密度下兩種狀態都可能出現；台灣物理學常用「介穩態」，待確認 |
| 相變 | phase transition | 相轉變 | tadaki2013、sugiyama2008；作者把順暢變塞車比喻成動態的相變 |
| 反應延遲 | reaction time, delay | 反應時間 | orosz2010第4462頁；Bando 1995沒有加 |
| 跟車模型 | car-following model | — | orosz2010第4461頁；每台車看前車決定怎麼開的模型 |
| 自動駕駛車 | autonomous vehicle, AV | 自駕車 | stern2018；這篇的車只有速度自動控制，方向盤由人操作 |
| 平滑車 | — | — | 我們簡報裡自己取的名字，指「照平均速度穩定開的那台車」，不是論文用語 |


========== 檔案：wiki/disputes.md ==========

# 研究差異與未解問題

每一條都要連回相關的證據卡。分類：1假設或方法不同、2條件不同、3結論真的衝突、4資料不足。

| 問題 | 分類 | 相關證據卡 | 目前判斷 | 會不會影響簡報核心主張 |
|---|---|---|---|---|
| 瓶頸只是觸發，還是塞車的成因之一？ | 4資料不足（可能是3） | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md) | 目前無法判斷。Sugiyama 2008依自己的模型說瓶頸只是觸發；它引用的Kerner理論看法不同，我們還沒讀Kerner | 不影響「沒有瓶頸也會塞」（有實驗支持），但簡報不能寫「塞車都跟瓶頸無關」 |
| 密度很高時還會不穩定嗎？ | 4資料不足 | [sugiyama2008-mechanism](cards/sugiyama2008-mechanism.md)、[bando1995-stable-regions](cards/bando1995-stable-regions.md)、[tadaki2013-high-density](cards/tadaki2013-high-density.md) | Sugiyama 2008沒討論很擠的情況；Bando 1995的模型（圖10）很擠時是穩定的；Tadaki 2013的40台那一場車流均勻，但只有一場、是第一天，作者自己說不確定是不是模型預測的那種。目前無法判斷真實車流是否如此 | 第3頁可以講「模型預測」和「實驗有一個跡象」，不能講成「已經證實」 |
| 實驗的塞車波速度能不能跟我們的模擬比？ | 2條件不同 | [sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md) | 目前不能直接比：實驗是約20 km/h，選題階段的模擬是無因次單位。要先有一組有出處、對應真實單位的參數 | 影響簡報能不能說「模擬跟實驗一致」 |
| 22台車的分界是不是a/2？ | 2條件不同 | [bando1995-linear-stability](cards/bando1995-linear-stability.md)、[orosz2010-ring-stability](cards/orosz2010-ring-stability.md)、[ours-finite-n-threshold](cards/ours-finite-n-threshold.md)、[ours-finite-n-simulation](cards/ours-finite-n-simulation.md) | 不衝突。Bando式(12)的a/2是車數很多時的條件；Orosz 2010附錄A的一般公式代入Bando模型（W=0、沒有延遲、不計車長）得到22台的分界1.9595，跟我們從Bando式(11)推的、模擬量的都一樣。代換那一步是我們做的 | 只影響第3頁的進階展開區 |
| 要不要加入反應延遲？ | 1假設或方法不同 | [bando1995-no-delay](cards/bando1995-no-delay.md)、[orosz2010-delays](cards/orosz2010-delays.md) | Bando 1995刻意不加，認為二階方程式已經包含延遲效果；Orosz 2010說延遲夠大時，最先不穩定的會變成短的波。我們的模型沒有延遲，所以「最先不穩定的是最長的波」只在這個前提下成立。不判誰對 | 不影響核心主張；簡報不能把a講成反應時間 |
| 塞車的火種是隨機減速，還是車流本身不穩定？ | 1假設或方法不同 | [nagel1992-randomization](cards/nagel1992-randomization.md)、[bando1995-ovm-equation](cards/bando1995-ovm-equation.md) | NaSch模型靠隨機減速產生塞車，Bando模型沒有隨機性、靠不穩定放大一點小擾動。兩者假設不同，不判誰對；實驗（Sugiyama 2008、Tadaki 2013）兩種解釋都沒有排除 | 簡報第3頁以Bando為主要模型時，要說明這只是其中一種解釋 |
| 塞車波往後的速度是15 km/h還是20 km/h？ | 2條件不同 | [nagel1992-real-units](cards/nagel1992-real-units.md)、[sugiyama2008-backward-wave](cards/sugiyama2008-backward-wave.md)、[tadaki2013-density-dependence](cards/tadaki2013-density-dependence.md) | 不算衝突。NaSch引用的高速公路量測約15 km/h（未標出處），Sugiyama和Tadaki的環道實驗約20 km/h；都是「約」，道路和量法不同 | 簡報講「大約每小時十幾到二十公里往後跑」比只講一個數字安全 |
| 真實實驗裡消掉波的方法，跟我們簡報的平滑車示範一樣嗎？ | 1假設或方法不同 | [stern2018-controllers](cards/stern2018-controllers.md)、[stern2018-results](cards/stern2018-results.md) | 不一樣。Stern 2018用的是FollowerStopper和PI控制器（或受過訓練的人），在真實車上測；我們如果做平滑車示範，是在Bando模型裡用自己簡化的規則。只能說「參考同樣的想法」 | 平滑車是加分功能；要做的話頁面上必須寫清楚 |


========== 檔案：wiki/derivations/finite-n-threshold.md ==========

# 有限車數時的穩定分界（我們的推導）

這份是我們自己的推導，不是任何一篇論文直接寫的。證據卡`ours-finite-n-threshold`指向這份。

## 從Bando 1995推

1. Bando 1995第1036頁式(9)：環上N台車，擾動只能拆成α_k = 2πk/N（k = 0, 1, ..., N−1）這幾種波。
2. 第1037頁式(11)：分開穩定和不穩定的臨界曲線是f = a / (2cos²(α/2))，其中f = V'(b)（式(7)）。f比這條曲線大，那個波就會變大。
3. 把α_k代進去：第k個波在V'(b) > a / (2cos²(πk/N)) 時變大。k = 0是整體平移，不算。
4. k = 1時cos²(π/N)最大，右邊最小，所以a從大往小調時，最先變不穩定的是k = 1。
5. 分界：V'(b) = a / (2cos²(π/N))，也就是a = 2V'(b)cos²(π/N) = V'(b)(1 + cos(2π/N))（用2cos²x = 1 + cos2x）。
6. N = 22、b = 2（V'(2) = 1）：a = 1 + cos(2π/22) ≈ 1.9595。N越大越接近2，也就是Bando式(12)的V'(b) < a/2。

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

**代入的結果：**
- G = 0代進(A6)：F = ½H²(1 + tan²(kπ/N)) = H² / (2cos²(kπ/N))。
- 再代入F = aV'、H = a：aV' = a² / (2cos²(kπ/N))，也就是V' = a / (2cos²(kπ/N))，跟上面第3步一樣。
- k = 1時跟第5步一樣；N趨近無限大時，(A8)變成aV' < a²/2，也就是V' < a/2，跟Bando式(12)一樣。

數值上，用`audition/ovm.py`的`critical_a`和上面從Orosz代入的公式，各算N = 22、30、100、10⁶，V' = 1和0.7864兩組，結果到小數第10位都相同（2026-11-11手動跑過）。

## 適用範圍

- 只對很小的擾動成立。
- 只適用沒有延遲、W = 0（不看相對速度）、所有駕駛相同的模型。Orosz第4467頁提到，延遲夠大時最先不穩定的會變成短的波（k大），這時上面的結論不成立。
- 這份推導說明的是「模型」在22台時的分界，不代表真實駕駛的分界。


========== 檔案：wiki/sources/bando1995.md ==========

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

## 這篇在做什麼

提出一個描述每台車怎麼跟車的數學模型（後來的文獻叫它最佳速度模型，這篇自己叫legal velocity function），用來解釋「沒有事故、沒有紅綠燈，一點小擾動也能自己長成塞車」。作者先用線性穩定性分析算出均勻車流什麼時候會不穩定，再用電腦模擬看塞車怎麼形成。均勻車流指每台車的速度和間距大致相同；線性穩定性分析是用來判斷一點小變化會慢慢消失，還是越來越嚴重。

頁碼用期刊頁碼（第1035～1042頁）。

## 研究條件

- 單一車道、不能超車的環狀道路（週期邊界），N台車、環長L（第1036頁）。
- 所有駕駛的敏感度a都一樣，而且是常數；沒有加入反應延遲（第1035頁）。
- 不考慮車長（第1036頁）。
- 論文裡的長度、時間、速度都沒有給單位，可以看成無因次，也就是模型裡的數字還沒有直接對應到公尺、秒或公里。
- 模擬用的是N=100台車，不是22台（第1037～1038頁）。

## 主要結果

- 跟車方程式：[cards/bando1995-ovm-equation.md](../cards/bando1995-ovm-equation.md)
- 線性穩定性：[cards/bando1995-linear-stability.md](../cards/bando1995-linear-stability.md)
- 車數和環長夠大時邊界條件不重要：[cards/bando1995-large-n-note.md](../cards/bando1995-large-n-note.md)
- 速度函數的選擇（簡單模型會倒車撞車，改用tanh(Δx−2)+tanh2）：[cards/bando1995-velocity-function.md](../cards/bando1995-velocity-function.md)
- 塞車自己形成、往後移動：[cards/bando1995-spontaneous-jam.md](../cards/bando1995-spontaneous-jam.md)
- 塞車形成後的車距和速度：[cards/bando1995-cluster-values.md](../cards/bando1995-cluster-values.md)
- 在這篇的模型和參數條件下，車很稀疏或非常密集時，均勻車流可能保持穩定；介於兩者之間的密度，小擾動反而可能逐漸放大：[cards/bando1995-stable-regions.md](../cards/bando1995-stable-regions.md)
- 有沒有塞車，運輸量差不多：[cards/bando1995-capacity.md](../cards/bando1995-capacity.md)
- 沒有加反應延遲：[cards/bando1995-no-delay.md](../cards/bando1995-no-delay.md)

我們自己根據這篇推的有限車數分界和模擬驗證：[cards/ours-finite-n-threshold.md](../cards/ours-finite-n-threshold.md)、[cards/ours-finite-n-simulation.md](../cards/ours-finite-n-simulation.md)

## 限制

- 這是模型和電腦模擬，不是真實道路的實驗。
- 所有駕駛一模一樣、沒有隨機性、沒有反應延遲，都是簡化。作者在第1042頁也提到可以讓每個駕駛的敏感度不同。
- 第1037頁的穩定條件總結V'(b)<a/2，是把所有可能的波都考慮進去的寫法，車數有限時實際分界會稍微不同，見[ours-finite-n-threshold](../cards/ours-finite-n-threshold.md)。作者說詳細的有限車數分析留到之後的論文。
- 第1040頁的模擬用「1000 steps」描述時間，但沒有寫一步是多少時間，圖的橫軸標的是time。

## ingest紀錄

- [runs/2026-11-11-n1-bando1995-r1.md](../../runs/2026-11-11-n1-bando1995-r1.md)


========== 檔案：wiki/sources/nagel1992.md ==========

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

## 這篇在做什麼

用一個很簡單的電腦規則模擬高速公路車流：把道路切成一格一格，每台車每一步照4條規則加速、減速、隨機慢一下、往前走。這種方法叫細胞自動機（cellular automaton），後來常被叫做NaSch模型。作者發現車變多時，車流會從順暢變成走走停停，而且塞車是隨機出現的。

頁碼用期刊頁碼（第2221～2229頁）。

## 研究條件

- 單一車道，路切成L格，每格最多一台車；車速是0到v_max的整數（第2222頁）。
- 大部分模擬用v_max=5（第2222頁）。
- 第3節是環狀道路（週期邊界），第4節是一端有瓶頸的開放道路（第2222、2227頁）。
- 第5節才把格子和時間步換算成真實單位：一格約7.5公尺、一步約1秒（第2227頁）。
- 隨機減速的機率p，文中沒有寫主要模擬用的數值（圖6的標籤看起來是p=0.5，但內文沒寫，所以不採用）。

## 主要結果

- 4條規則：[cards/nagel1992-rules.md](../cards/nagel1992-rules.md)
- 隨機減速這一步是關鍵：[cards/nagel1992-randomization.md](../cards/nagel1992-randomization.md)
- 環狀道路上，密度高時塞車隨機出現、往後移動：[cards/nagel1992-circle-jams.md](../cards/nagel1992-circle-jams.md)
- 從順暢到塞車的轉變在密度約0.08附近，但確切位置不清楚：[cards/nagel1992-transition.md](../cards/nagel1992-transition.md)
- 換算真實單位：[cards/nagel1992-real-units.md](../cards/nagel1992-real-units.md)
- 瓶頸路段：[cards/nagel1992-bottleneck.md](../cards/nagel1992-bottleneck.md)

## 限制

- 這是模型和模擬，不是實驗。
- 它對塞車成因的解釋跟Bando 1995不同：這裡的塞車靠隨機減速觸發，Bando的模型沒有隨機性，是車流本身不穩定。這是假設不同，不判誰對，見[disputes.md](../disputes.md)。
- 換算真實單位的幾種方法只「數量級一致」，作者自己說是粗略的論證（第2227頁）。

## ingest紀錄

- [runs/2026-11-11-n1-nagel1992-r1.md](../../runs/2026-11-11-n1-nagel1992-r1.md)


========== 檔案：wiki/sources/orosz2010.md ==========

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


========== 檔案：wiki/sources/stern2018.md ==========

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

## 這篇在做什麼

照Sugiyama的環道實驗再做一次，但車隊裡有一台可以自動控制速度的車（CAT Vehicle）。先讓所有人照常開、等走走停停波出現，再打開那台車的控制，看一台車能不能把波消掉。比較了車速的變動、急煞次數、油耗和通過量。

頁碼用arXiv預印本的頁碼（第1～18頁），不是期刊頁碼。

## 研究條件

- 單車道環道，半徑41.4公尺、周長260公尺，21～22台車（第3頁）。
- 只有一台車被控制；那台車的方向盤一直由受過訓練的人操作，只有速度是自動的（第4頁）。
- 其他駕駛是亞利桑那大學的職員，受過安全駕駛訓練，被要求像尖峰時段那樣開、盡量跟上前車，刻意不讓他們自己去消波（第4～5頁）。
- 三場實驗：A用FollowerStopper控制器（目標速度由外部觀察者給）、B由受過訓練的人照同樣策略開、C用自己算平均速度的PI控制器（第3、8～10頁）。
- 每場7～10分鐘，每種控制器只做一場。

## 主要結果

- 實驗設定：[cards/stern2018-setup.md](../cards/stern2018-setup.md)
- 三場都出現走走停停波：[cards/stern2018-waves-emerge.md](../cards/stern2018-waves-emerge.md)
- 控制的想法：照平均速度開：[cards/stern2018-controllers.md](../cards/stern2018-controllers.md)
- 打開控制後車速變動、急煞、油耗都降低：[cards/stern2018-results.md](../cards/stern2018-results.md)
- 目標速度設太高或關掉控制，波又回來：[cards/stern2018-wave-returns.md](../cards/stern2018-wave-returns.md)

## 限制

- 讀的是arXiv預印本，正式期刊版的內容和數字可能不同。
- 每種控制器只有一場，沒有重複和統計檢定。
- 本文的數字有小地方對不上：實驗B的油耗降幅，內文寫22.0%、表3寫22.1%；實驗C內文寫27.9%、表3寫28.1%。卡片以表3為準，並註明。
- 這是真實車輛實驗，但只在一條260公尺的環道上，作者說推廣到多車道高速公路還需要更多研究（第14頁）。
- 如果簡報要做「平滑車」示範，那會是我們自己的簡化版本，不是這篇的兩種控制器。

## ingest紀錄

- [runs/2026-11-11-n1-stern2018-r1.md](../../runs/2026-11-11-n1-stern2018-r1.md)


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

頁碼用期刊本身印的頁碼（第1～7頁）。大阪大學典藏庫的PDF前面多一張封面，PDF的頁數會比期刊頁碼多。

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

- 只有一個場地、一種車數設定的詳細結果，沒有重複次數和統計。作者在腳註15說更詳細的結果和不穩定的密度範圍會在之後的論文發表（可能是Tadaki 2013，要讀過才知道）。
- 數字幾乎都是「約」「roughly」，是從影片和圖讀出來的估計值。
- 「瓶頸只是觸發、不是塞車的根本原因」是作者依自己的模型做的解釋，實驗本身支持的是「沒有瓶頸也可能塞車」。文中也引用了Kerner的研究（參考文獻[3]、[8]），Kerner的理論對塞車成因有不同看法，我們還沒讀，見[disputes.md](../disputes.md)。
- 文中沒有寫出模型方程式和穩定條件，要另外從模型的原始論文確認。

## ingest紀錄

- [runs/2026-11-11-n1-sugiyama2008-r1.md](../../runs/2026-11-11-n1-sugiyama2008-r1.md)


========== 檔案：wiki/sources/tadaki2013.md ==========

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

## 這篇在做什麼

Sugiyama 2008那群人做的後續實驗。這次在名古屋巨蛋的室內環道，讓車數從10台到40台一場一場改變，看密度多高時會從順暢變成塞車，並估出臨界密度。作者刻意不用任何模型，只用實驗資料和高速公路常用的分析方法來估。

頁碼用期刊頁碼（第1～20頁）。典藏庫的PDF前面多兩頁，PDF頁數等於期刊頁碼加2。

## 研究條件

- 名古屋巨蛋室內平地，半徑50公尺、周長314公尺的環道（第3～4頁、圖2～3）。
- 用雷射掃描器量車的位置，大約每0.2秒一筆，空間解析度在50公尺處約0.16公尺（第5頁、附錄A）。上一次實驗是從影片人工讀，誤差約±0.5公尺。
- 兩天共19場，車數10～40台；車都是同一款（Toyota Vitz）；52位大學生輪流開（第5頁、表1）。
- 駕駛被要求用自己的方式安全駕駛，目標速度30 km/h（第5頁）。
- 第一天駕駛非常小心、沒有開到想要的速度，所以主要分析只用第一天的暖身場和第二天的資料（第6頁）。

## 主要結果

- 實驗設定：[cards/tadaki2013-setup.md](../cards/tadaki2013-setup.md)
- 車少時順、車多時塞，塞車團以約20 km/h往後傳：[cards/tadaki2013-density-dependence.md](../cards/tadaki2013-density-dependence.md)
- 臨界密度在每公尺0.08到0.09台之間：[cards/tadaki2013-critical-density.md](../cards/tadaki2013-critical-density.md)
- 中間密度時順暢和塞車兩種狀態都會出現（介穩態）：[cards/tadaki2013-metastable.md](../cards/tadaki2013-metastable.md)
- 作者說這個臨界密度跟高速公路的觀測一致：[cards/tadaki2013-expressway-consistency.md](../cards/tadaki2013-expressway-consistency.md)
- 40台車時車流反而均勻，但作者說還不確定代表什麼：[cards/tadaki2013-high-density.md](../cards/tadaki2013-high-density.md)

## 限制

- 第二天28、30、32、34台各做了2～3場，25台只有1場；場次不多，文中沒有對重複場次做統計檢定。
- 駕駛是大學生，第一天和第二天的開法明顯不同，作者為此排除了大部分第一天的資料。
- 40台那一場是第一天、沒有用在主要分析的場次，所以「很擠時變均勻」只是一個跡象。
- 跟高速公路比較的那一步是粗略的論證（車速快三倍，車距也要大三倍）。

## ingest紀錄

- [runs/2026-11-11-n1-tadaki2013-r1.md](../../runs/2026-11-11-n1-tadaki2013-r1.md)


========== 檔案：wiki/cards/bando1995-capacity.md ==========

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

在這組模擬條件下，有塞車時和完全均勻時，單位時間通過一個點的車數都約0.48，作者覺得奇怪，說會在之後的論文討論。

## 原文依據

第1041頁用N/T估算運輸量：有塞車時約100/208≈0.48（式(25)），均勻車流時用L/V(b)算出的週期也得到約0.48（式(26)）。

> It seems strange that the existence of congestion does not affect the capacity of transportation.

## 限制

- 只有一組參數，作者自己也還沒解釋原因。
- 不能推論成「塞車不影響通行量」，這只是這個模型、這組條件的結果。


========== 檔案：wiki/cards/bando1995-cluster-values.md ==========

---
id: bando1995-cluster-values
type: model_theory
source: bando1995
locator: 第1040頁圖7～9和右欄
conditions: 同bando1995-spontaneous-jam的模擬條件；數值是作者從最後100步的分布讀出來的
units: 無因次
status: confirmed
related: bando1995-spontaneous-jam, bando1995-stable-regions
---

## 主張

塞車形成之後，塞車團裡的車距約0.32、速度約0.03（幾乎停住）；團外的車距約3.68、速度約1.88。100台車裡有50台在擁擠的區域。作者把模擬分成三個階段：前50步符合線性分析，50～400步看起來很亂，400步之後慢慢穩定下來。

## 原文依據

第1040頁從圖7、圖8最後100步的分布讀出：擁擠區車距約0.32、速度約0.03，順暢區車距約3.68、速度約1.88，這些值在5團塞車都一樣。如果把車距短於2的算擁擠區，總共50台。同頁依圖9(b)把模擬分成三個階段，並說850步左右兩團塞車合併。

## 限制

- 數值是「約」，作者從分布圖讀出。
- 只有這一組參數。

## 教學說法

塞住之後，車子不是平均慢一點，而是分成兩種：塞在裡面幾乎不動的，和跑在外面接近全速的。


========== 檔案：wiki/cards/bando1995-large-n-note.md ==========

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

## 原文依據

第1036頁說明模型用週期邊界（第N+1台就是第1台），接著說車數和環長夠大時這個條件不重要，詳細分析在後續論文。

> So far as we consider the case of a large enough number of vehicles N with enough circuit length L, this boundary condition is not essential for both analytical and numerical investigations.

## 限制

- 沒有說多少台算「夠大」。2008年的實驗只有22台，是不是「夠大」要另外判斷，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。


========== 檔案：wiki/cards/bando1995-linear-stability.md ==========

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

線性穩定性分析是判斷一點小變化會慢慢消失、還是越來越嚴重的方法。在均勻車流上加很小的擾動，把擾動拆成一個一個的波（第k個波的α_k=2πk/N）來看會不會變大。作者得到的總結是：速度函數在均勻車距的斜率V'(b)小於a/2時穩定，大於a/2時不穩定，而且這個條件對任何速度函數都成立。

## 原文依據

第1036頁式(5)～(10)把擾動線性化，用exp{iα_k n+zt}展開，得到z的二次方程式(10)；z的實部u>0代表那個波會變大。第1037頁式(11)是圖1裡分開穩定和不穩定的臨界曲線f=a/(2cos²(α/2))，其中f=V'(b)（式(7)）。作者整理成三種情況：f<a/2穩定、f=a/2臨界、f>a/2不穩定，總結成式(12) V'(b)<a/2。

> Note that the above criteria is valid in models with any legal velocity function V.

## 限制

- 只對很小的擾動成立，擾動變大之後要用模擬看（第1037頁）。
- 式(12)的a/2是把所有α都考慮進去的條件；車數有限時α只有幾個固定的值，實際分界會比a/2稍微不同，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。這是我們從式(9)(11)推出來的，不是論文直接寫的。

## 教學說法

駕駛對車距越敏感（只要距離一變，速度就跟著大幅改變），而調整得又不夠快，前車的一點點減速就會一台傳一台、越傳越大。


========== 檔案：wiki/cards/bando1995-no-delay.md ==========

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

## 原文依據

第1035頁說這篇的模型中，刺激是跟車距離的函數、敏感度是常數，而且不加入反應的時間延遲。第1042頁對比過去很多研究用加入延遲的方程式，說這個模型是透過二階方程式把延遲的效果帶進來，並說這是模型最主要的特徵。

> Moreover we do not introduce the time lag of response.

## 限制

- 「二階方程式就包含延遲的效果」是作者的看法。同一群作者1998年又發表了加入明確延遲的版本（這是從Orosz 2010的參考文獻看到的，還沒讀）。
- 教學時不能把a說成「反應時間幾秒」，a是敏感度，不是延遲。


========== 檔案：wiki/cards/bando1995-ovm-equation.md ==========

---
id: bando1995-ovm-equation
type: model_theory
source: bando1995
locator: 第1036頁式(1)～(4)
conditions: 單車道環狀道路，N台車、環長L，所有駕駛敏感度a相同，沒有反應延遲，無因次
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-velocity-function, bando1995-no-delay
---

## 主張

每台車的加速度由「它想開的速度」和「現在的速度」的差決定：想開的速度V只看自己到前車的距離，差距乘上敏感度a就是加速度。所有車等距、等速的均勻車流（每台車的速度和間距都一樣；車距b=L/N、速度V(b)）一定是這個方程式的一個解。

## 原文依據

第1036頁式(1)：第n台車的加速度等於a乘上{V(Δx_n)減去自己的速度}，式(2)：Δx_n是第n+1台和第n台的位置差。a是代表駕駛敏感度的常數，V是只看前車距離的legal velocity：單調遞增、有上限。式(3)(4)：均勻車流的解是每台車間距b=L/N、速度c=V(b)，作者叫它steady state flow。

## 限制

- 所有駕駛的a和V都一樣，沒有隨機性，也沒有反應延遲（第1035頁）。
- 只看前一台車，不看更前面的車，也不看相對速度。

## 教學說法

每個駕駛心裡都有一個「這個距離開多快才安全」的速度。前車太近就慢下來，拉開了就加速，a是他調整得多快。


========== 檔案：wiki/cards/bando1995-spontaneous-jam.md ==========

---
id: bando1995-spontaneous-jam
type: model_theory
source: bando1995
locator: 第1038頁式(24)後段、第1039頁圖5、第1040頁圖6
conditions: 模擬，不是實驗；N=100、L=200（車距2）、a=1、V=tanh(Δx−2)+tanh2；初始只有一台車往前偏0.1
units: 無因次
status: confirmed
related: bando1995-velocity-function, bando1995-cluster-values, sugiyama2008-backward-wave
---

## 主張

在模擬裡，100台車原本均勻地繞，只把一台車往前移0.1，車流就自己分成幾段幾乎停住的塞車和幾段快速前進的車，最後形成5團塞車；這些塞車團都以相同的速度慢慢往後移動。

## 原文依據

第1038頁說模擬用N=100、L=200，加上跟簡單模型一樣的初始擾動（式(17)～(19)：第1台車往前偏0.1）。第1039頁圖5是t=100、300、1000時所有車的速度：沒有負速度，速度逐漸分成接近0和接近最大速度兩種。第1039～1040頁圖6是所有車位置隨時間的圖，看得到5團塞車從很小的擾動長出來。

> From this figure, we find that five clusters of congestion are formed even from a very tiny disturbance existing in the almost uniform vehicle distribution.

第1039頁最後一句接到第1040頁說，圖6也顯示所有塞車團都以相同的速度慢慢往後移動（這句跨頁，所以不直接引用）。

## 限制

- 這是電腦模擬的結果，作者是用模擬來示範，不是真實道路。
- 車數100、車距2，跟2008年實驗的條件不同。

## 教學說法

在電腦裡只讓一台車稍微往前一點點，什麼都不做，過一陣子整圈就塞成好幾段。


========== 檔案：wiki/cards/bando1995-stable-regions.md ==========

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

## 原文依據

第1041頁說初始車距b落在穩定區時，小擾動不會改變車流；落在不穩定區時，每台車會被推向左右兩邊的穩定區。圖10在tanh(Δx−2)+tanh2的曲線上畫出stable、unstable、stable三區，並標出擁擠時的車距Δx_min和順暢時的車距Δx_max。

## 限制

- 圖10是示意圖，沒有標出區域邊界的數值。我們用V'(Δx)=a/2自己算，a=1時邊界約在車距1.12和2.88，跟圖上虛線的位置相符；這是我們算的，不是論文寫的。
- 這是模型的結論。真實車流在很擠的時候是不是穩定，要看密度實驗（例如Tadaki 2013），見[disputes.md](../disputes.md)。

## 教學說法

在這個模型裡，車子很少時很順，車子多到一個程度會開始走走停停，但如果擠到幾乎貼在一起，大家只能一起慢慢開，反而不會出現走走停停的波。這是模型的結果，不代表所有真實道路都這樣。


========== 檔案：wiki/cards/bando1995-velocity-function.md ==========

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

作者先試了最簡單的速度函數V=tanh(Δx)，結果在不穩定時會有車往後倒退，等於撞車。所以改用V(Δx)=tanh(Δx−2)+tanh2：車距是0時速度是0，車子只會慢慢加減速、不會超過前車。

## 原文依據

第1037頁式(16)是簡單模型V=tanh(Δx)。第1037～1038頁說不穩定時會看到車往後移動（圖3、圖4），單車道上就代表兩台車撞在一起。第1038頁式(24)改用V(Δx)=tanh(Δx−2)+tanh2，並說這樣駕駛會慢慢加減速，不會超過前車。

> a driver controls the vehicle by gradually accelerating or braking in such a way that it never passes the preceding vehicle

## 限制

- tanh(Δx−2)+tanh2只是一個形狀合理的函數，論文沒有說它是從真實資料擬合出來的。
- 選題階段的模擬（`audition/ovm.py`）用的就是這個函數，現在有出處了。


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

在模擬的瓶頸情境下，車流自己穩定在密度約每格0.069台、流量約每步0.304台的狀態；作者說這個狀態不是流量最大的地方。

## 原文依據

第2227頁第4節說明開放邊界的設定，模擬放鬆之後密度<ρ_c>=0.069±0.002、流量<q_c>=0.304±0.001。第2228頁圖6的說明寫，模擬清楚顯示這個自我組織的瓶頸狀態並不在流量的最大值。

## 限制

- 模型裡的瓶頸是邊界條件，跟真實道路的匝道或隧道不同。
- 這張卡跟「瓶頸是不是塞車成因」的討論有關，但這篇沒有直接回答那個問題。


========== 檔案：wiki/cards/nagel1992-circle-jams.md ==========

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

## 原文依據

第2223頁圖1是密度0.03的模擬，圖說說低密度時車流不受干擾。第2224頁圖2是密度0.1，圖說請讀者注意塞車往後移動；內文說跟著一台車看，它以速度4到5開進來，碰到塞車團停下，在隊伍裡卡一陣子，離開後再加速到全速，所以這團塞車代表高速公路上典型的走走停停波。

> Whereas we find laminar traffic at low densities, there are congestion clusters (small jams) at higher densities, which are formed randomly due to velocity-fluctuations of the cars.

## 限制

- 「像高速公路上的走走停停波」是作者拿圖3的空拍軌跡（引用別人的資料）做的定性比較。


========== 檔案：wiki/cards/nagel1992-randomization.md ==========

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

## 原文依據

第2222頁說第3步代表人的行為或外在條件不同造成的自然速度波動；沒有隨機性時，每個初始配置都會很快到達一個穩定的樣式，每個時間步往後（跟車子相反方向）移一格。

> Step 3 is essential in simulating realistic traffic flow since otherwise the dynamics is completely deterministic.

## 限制

- 這是這個模型的設計。Bando 1995的模型完全沒有隨機性，也能產生塞車，兩種模型對「塞車從哪來」的假設不同，見[disputes.md](../disputes.md)。

## 教學說法

這個模型把「駕駛偶爾無緣無故慢一下」當成塞車的火種。


========== 檔案：wiki/cards/nagel1992-real-units.md ==========

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

作者把一格換算成7.5公尺（塞車時一台車佔的長度），並用幾種方法估算一個時間步大約0.5到1秒，結論是時間步的數量級是「秒」。其中一種方法用了高速公路上量到的塞車波往後速度約15 km/h。

## 原文依據

第2227頁：塞車時每台車佔約7.5公尺，自由行駛4.5格／步對應約120 km/h，得到一步約1秒（式(8)）；用基本圖最大值和高速公路容量估算，得到約0.5秒。第2228頁：用高速公路上量到的往後傳的走走停停波速度約15 km/h（約4.2 m/s）估算，得到約0.7秒。

> Thus all these estimates agree in order of magnitude: time steps correspond to seconds.

## 限制

- 作者自己說是粗略的論證。
- 15 km/h是作者引用的高速公路量測值，這段沒有標出處；Sugiyama 2008說的是約20 km/h，兩者來源和條件都不同，見[disputes.md](../disputes.md)。


========== 檔案：wiki/cards/nagel1992-rules.md ==========

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

每一步，每台車依序做4件事：1. 還沒到最高速、前面空間夠，就加速1；2. 前車太近，就減到不會撞上的速度；3. 以機率p隨機減速1；4. 照速度往前走。

## 原文依據

第2222頁第2節列出四個步驟：Acceleration（速度低於v_max且前車距離大於v+1時加1）、Slowing down（看到前車在i+j格、j≤v時，速度降到j−1）、Randomization（以機率p，速度大於0的車減1）、Car motion（往前走v格）。所有車同時進行。

## 限制

- 速度和位置都是整數，跟Bando的連續模型不同。
- 每台車只看前車。

## 教學說法

把道路想成一格一格的棋盤，每台車每一秒都照四條很簡單的規則走，其中一條是「偶爾會無緣無故慢一下」。


========== 檔案：wiki/cards/nagel1992-transition.md ==========

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

這個模型裡，從順暢到塞車的轉變大約發生在密度每格0.08台附近；但轉變的位置和形狀會隨道路長度改變，作者也說從模擬圖看不出確切的轉變點在哪。

## 原文依據

第2224頁說圖4是模型的基本圖，可以清楚看到在密度約0.08附近有轉變，但更多模擬顯示最大值的位置和形狀跟系統大小有關（沒有隨機減速的模擬則沒有這種關係）。

> However, it is not clear from these pictures where to locate an exact transition point.

## 限制

- 0.08是這個模型、這組設定的值，單位是每格的車數，不能直接跟真實道路或其他模型比。


========== 檔案：wiki/cards/orosz2010-delays.md ==========

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

## 原文依據

第4467頁說，沒有延遲時特徵方程只有有限個解，所有方法都得到相同的條件，穩定性在k=1失去；有延遲時特徵方程有無限多個解，延遲夠大時會在高頻、短波失去穩定，延遲更大時控制本身會不穩定。

> If the delays are sufficiently large, the flow may lose its stability to high-frequency, short-wavelength

## 限制

- 這段只是概述，細節引用其他論文，我們沒有讀。
- 我們的模型（Bando 1995）沒有延遲，這張卡的作用是標出「22台車分界在k=1」這個結論的適用範圍。


========== 檔案：wiki/cards/orosz2010-ovm-family.md ==========

---
id: orosz2010-ovm-family
type: review
source: orosz2010
locator: 第4461頁式(3.7)、第4462頁式(3.10)和三種延遲設定、第4462～4463頁式(3.12)
conditions: 單車道、車子一樣長、駕駛相同；綜述整理
units: 無因次
status: confirmed
related: bando1995-ovm-equation, bando1995-no-delay
---

## 主張

在Orosz等人的整理裡，動態跟車模型把加速度寫成車距、車距變化和自己速度的函數，可以有反應延遲；OV模型是其中一類，加速度＝（想開的速度－現在速度）÷T，再加一項看相對速度的W。作者說，延遲全部設為0的做法就是Bando 1995用的。

## 原文依據

第4461頁式(3.7)定義車距h是兩車保險桿之間的距離（扣掉車長）。第4462頁式(3.10)是一般的動態模型，列出三種常見的延遲設定，第一種「零反應時間」引用Bando 1995。第4462頁式(3.12)是OV模型，第一項是以鬆弛時間T趨向最佳速度V(h)，W是看相對速度的項；第4462～4463頁說W=0、沒有延遲的情況已被大量研究，引用Bando 1995。

> This is usually justified by saying that dynamic models (3.10) may reproduce uniform flow as well as stop-and-go waves for zero reaction time

## 限制

- Bando 1995沒有W項、也不考慮車長，所以要對應時W=0、車長0，Bando的a對應這裡的1/T。這個對應寫在`wiki/derivations/finite-n-threshold.md`。


========== 檔案：wiki/cards/orosz2010-ring-stability.md ==========

---
id: orosz2010-ring-stability
type: review
source: orosz2010
locator: 第4467頁第3段、第4475～4476頁附錄A式(A1)～(A8)
conditions: 一般的跟車模型，沒有反應延遲；環上N台車；F、G、H大於0
units: 無因次
status: confirmed
related: orosz2010-stability-approaches, ours-finite-n-threshold
---

## 主張

在沒有反應延遲的跟車模型裡，環上N台車時，第k個波各有一條穩定分界；越過分界時最先失去穩定的是k=1（最長的波）。車數趨近無限多時，分界變成一個不分k的條件。

## 原文依據

第4475頁附錄A把式(5.1)在沒有延遲時寫成(A1)，用環上N台車的解得到(A3)，開N次方後回到(A2)，波數只能是(A4)的2kπ/N。第4476頁(A6)是第k個波穩定性改變的條件，作者說從F小往大越過分界時系統「更不穩定」，因此最先失去穩定的是k=1；N趨近無限大時條件變成(A8)。第4467頁也說，沒有延遲時穩定性會先在低頻、長波（k=1）失去。

> Consequently, the stability loss occurs for the lowest wavenumber

## 限制

- 這是一般模型的公式，用F、G、H表示。代入Bando的模型（W=0、車長0）得到22台車分界的那一步是我們做的，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。
- 只適用沒有延遲的情況，見[orosz2010-delays](orosz2010-delays.md)。


========== 檔案：wiki/cards/orosz2010-stability-approaches.md ==========

---
id: orosz2010-stability-approaches
type: review
source: orosz2010
locator: 第4466～4467頁第5節、式(5.1)～(5.3)
conditions: 均勻車流附近的小擾動（線性化）
units: 無數值
status: confirmed
related: bando1995-linear-stability, orosz2010-ring-stability
---

## 主張

分析均勻車流穩不穩定，文獻裡有三種做法：假設無限長道路上的波、看環上N台車、或看一排車的訊號會不會一台傳一台放大。作者說三種做法得到相同的結果；均勻車流失去穩定時，會出現往後傳的波。

## 原文依據

第4466頁式(5.1)把模型在均勻車流附近線性化，式(5.2)定義F、G、H三個係數。第4466～4467頁列出三種方法：「物理學家的方法」（無限長道路、波的假設，引用Bando 1995）、「動力系統的方法」（環上N台車）、「控制工程師的方法」（車隊的傳遞函數）。第4467頁說失去穩定時是Hopf分岔，波的形式是式(5.3)，k是離散的波數。

> There are (at least) three different methodologies to study the linear stability of the uniform flow

## 限制

- 只對很小的擾動成立。


========== 檔案：wiki/cards/ours-finite-n-simulation.md ==========

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

## 原文依據

這是我們的模擬，不是論文。`audition/run2.log`的A4用兩個a值的成長率內插出分界，A4b在a=1.98量到成長率−3.88e-04。

## 限制

- 這是選題階段的程式，還不是正式的`model/`。
- 驗證的是我們的推導跟我們的模擬一致，不代表真實駕駛也這樣。


========== 檔案：wiki/cards/ours-finite-n-threshold.md ==========

---
id: ours-finite-n-threshold
type: our_derivation
source: wiki/derivations/finite-n-threshold.md
locator: 「從Bando 1995推」第1～6步、「跟Orosz 2010對照」
conditions: bando1995的模型；環狀道路N台車；只看很小的擾動
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-large-n-note, ours-finite-n-simulation, orosz2010-ring-stability
---

## 主張

車數有限時，第k個波只有在a < 2V'(b)cos²(πk/N)時才會變大；a往下調時最先變不穩定的是k=1，所以N台車的實際分界是a = 2V'(b)cos²(π/N) = V'(b)(1+cos(2π/N))。22台車、車距2時是1.9595，不是a/2條件給的2；車數越多越接近2。

## 原文依據

這是我們推的，不是論文寫的，完整推導在`wiki/derivations/finite-n-threshold.md`。推法：bando1995式(11)的臨界曲線是f=a/(2cos²(α/2))，式(9)的α_k=2πk/N只能取這幾個值，把α_k代進去，第k個波不穩定的條件是f>a/(2cos²(πk/N))；k=1時右邊最小。f=V'(b)。

另外拿Orosz 2010附錄A的一般公式(A6)對照：取W=0、沒有延遲、不計車長，代入F=aV'、G=0、H=a，得到同一個條件；Orosz也寫明沒有延遲時最先不穩定的是k=1。

## 限制

- 我們自己推的。Orosz 2010的公式是一般跟車模型的，把它對應到Bando模型（W=0、沒有延遲、不計車長）的那一步是我們做的，Orosz沒有直接算Bando模型22台的分界。
- 只適用沒有延遲的模型；Orosz第4467頁說延遲夠大時，最先不穩定的會變成短的波。
- 只對很小的擾動成立。
- 差別只有約2%，對一般讀者不重要，放在進階展開區。


========== 檔案：wiki/cards/stern2018-controllers.md ==========

---
id: stern2018-controllers
type: experiment
source: stern2018
locator: 第5頁第3節開頭、第6～8頁第3.1～3.2節
conditions: 控制器只用那台車自己量到的速度、跟前車的距離，以及（實驗A、B）外部給的目標速度
units: s
status: confirmed
related: stern2018-results
---

## 主張

兩種控制器的共同想法是：那台車照著車流的平均速度開，而不是跟著前車忽快忽慢。前車加速時讓空隙變大、前車減速時把空隙吃掉，同樣的時間走同樣的距離，但加速和煞車少很多；距離太近時一定以安全為先。

## 原文依據

第5頁說，平均速度在波來之前比前車慢、在波裡面比前車快，照平均速度開可以用較少的加減速走同樣的距離，另外要有防止距離太近或太遠的邏輯。第6～7頁的FollowerStopper在安全時用目標速度U，距離太近時降低速度；第7～8頁的PI控制器用自己過去約38秒（大約繞一圈）的平均速度當目標，距離太近時跟著前車速度、距離太大時加速追上。

> By simply driving at the average speed, a vehicle covers the same distance in the same amount of time, but with less acceleration and breaking.

（原文braking拼成breaking，照原文引用。）

## 限制

- 實驗A的目標速度是外部觀察者給的，不是車子自己算的。
- 簡報如果做「平滑車」示範，會是我們自己簡化的規則，不是這兩種控制器，要在頁面上寫清楚。


========== 檔案：wiki/cards/stern2018-results.md ==========

---
id: stern2018-results
type: experiment
source: stern2018
locator: 第12頁表3、第13頁第4.3節
conditions: 比較「第一次出現波、沒有控制」和「控制開啟中表現最好」的時段；每種控制器一場
units: %、次/車/km
status: confirmed
related: stern2018-controllers, stern2018-wave-returns
---

## 主張

三場實驗打開控制後，所有車的車速標準差都下降（A降80.8%、B降49.5%、C降54.7%），油耗下降（42.5%、22.1%、28.1%），急煞次數大幅減少；通過量A增加14.1%、B增加9.8%，但C減少2.5%。

## 原文依據

第12頁表3列出三場實驗「波剛出現時」和「控制開啟時表現最好的時段」的車速標準差、油耗、急煞次數和通過量，以及變化百分比。第13頁整理成四點：車速標準差在三場都下降、油耗都下降、急煞大幅減少（從每車每公里8.58～9.66次降到最差2.47次、最好0.12次）、通過量A和B增加、C略降。

> The velocity standard deviation is reduced in all experiments

## 限制

- 比較的是「表現最好的時段」，不是整段控制期間的平均。
- 每種控制器只有一場，沒有統計檢定。
- 油耗降幅內文和表3有小差異（B：22.0%和22.1%；C：27.9%和28.1%），這裡用表3。
- 實驗C的控制器只用自己的資訊，平均速度略降，所以通過量反而少一點。


========== 檔案：wiki/cards/stern2018-setup.md ==========

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

實驗在周長260公尺的單車道環道進行，21～22台車，其中一台是可以自動控制速度的車；其他駕駛被要求像尖峰時段那樣開、盡量跟緊前車，目的是不讓他們自己把波消掉。

## 原文依據

第3頁說環道半徑41.4公尺（到車道中心）、周長260公尺，21到22台車，比Sugiyama的場地大，是因為美國的車比較大。第4頁說只有一台車被用來消波，方向盤一直由人控制；其他駕駛是受過安全駕駛訓練的大學職員。第5頁列出給駕駛的指示，並說明這是為了避免駕駛刻意消波。

> Drive as if you were in rush hour traffic.

## 限制

- 場地、車種、駕駛都跟Sugiyama 2008不同。
- 駕駛知道場上有一台會切換自動模式的車。


========== 檔案：wiki/cards/stern2018-wave-returns.md ==========

---
id: stern2018-wave-returns
type: experiment
source: stern2018
locator: 第10頁第1～2段、第11頁、第13頁
conditions: 實驗A調整目標速度；實驗A、B關閉控制之後；實驗C控制期間
units: m/s
status: confirmed
related: stern2018-results
---

## 主張

控制不是開了就一勞永逸：實驗A把目標速度從7.50調到8.00 m/s、比車流平均還快時，波又出現了；實驗A、B關掉控制後波也回來了；實驗C在控制期間又產生了第二個波，但也被消掉。

## 原文依據

第10頁說實驗A在目標7.50 m/s時，控制車的速度幾乎剛好等於車流平均、不需要減速；調到8.00 m/s時平均比車流快，又引發了波，調回7.50 m/s後波再次被消掉，控制器關掉後波又出現。第11頁說實驗B回到一般駕駛後波又出現。第13頁說實驗C消掉了一開始的波，但控制期間又產生了一個波。

> which inevitably induces a wave again

## 限制

- 只有這幾場的觀察，沒有說明「目標速度要設多少」的一般規則。

## 教學說法

一台車要能消掉塞車波，關鍵是開得穩、而且速度要剛好接近大家的平均；想開得比大家快，反而會把波帶回來。


========== 檔案：wiki/cards/stern2018-waves-emerge.md ==========

---
id: stern2018-waves-emerge
type: experiment
source: stern2018
locator: 第4頁第2.2節、第9頁實驗A～C的描述
conditions: 所有車都由人開的時段
units: s
status: confirmed
related: stern2018-setup, sugiyama2008-jam-emerges
---

## 主張

三場實驗在全部由人開的時候都出現了走走停停波：實驗A在第79秒、實驗B在第55秒、實驗C在第161秒看到第一個波。

## 原文依據

第4頁說每場實驗都出現交通波，並讓不穩定的車流至少持續45秒才打開控制器。第9頁記錄實驗A第79秒、實驗B第55秒、實驗C第161秒出現第一個波。

> Traffic waves appear in all experiments

## 限制

- 只有三場，但三場都出現，跟Sugiyama 2008的結果一致（不同國家、不同駕駛、不同場地）。


========== 檔案：wiki/cards/sugiyama2008-23-vehicles.md ==========

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

## 原文依據

第5頁說作者做了幾次不同車數的實驗，23台時也形成塞車團，速度跟22台相同；腳註15說更詳細的結果和不穩定的密度範圍會在之後的論文和實驗發表。

> In the case of 23, a jam cluster was formed and its velocity was the same as the case of 22

## 限制

- 只有一句話，沒有數據或圖。
- 其他車數（例如比22台少的）結果沒有寫，所以不能從這篇推論「車少就不會塞」。


========== 檔案：wiki/cards/sugiyama2008-backward-wave.md ==========

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

## 原文依據

第5頁說塞車團內的車完全停止、團外的車自由行駛（約40 km/h），前端的車加速脫離、另一台車到達後端，這樣重複讓塞車團維持下去，塞車團本身以大約20 km/h往後移動。第6頁圖4是2分鐘內每台車在環上的軌跡（0公尺和230公尺是同一點），作者在圖上加了一條約20 km/h的參考線。

> it propagates in the opposite direction to the movement of vehicles

## 限制

- 速度都是「約」「roughly」，是從影片軌跡讀出的估計，文中沒有誤差範圍。
- 這次的塞車團只有5台車。作者認為塞車團的速度跟長短無關，但這次實驗本身沒有比較不同長度的塞車團。

## 教學說法

塞車不是一個固定的地點，是一道往後跑的波。車子一台一台進去、一台一台出來，塞住的位置卻一直往後退。


========== 檔案：wiki/cards/sugiyama2008-fundamental-diagram.md ==========

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

把高速公路上的車流密度和流量畫成圖（基本圖：用圖表示車流密度、速度和通過車輛數之間的關係），資料點在臨界密度附近明顯分成兩群：自由流和擁擠車流。圖1這個地點的臨界密度約每公里25台。

## 原文依據

第2頁說真實資料的密度和流量關係有共通的性質，資料在臨界密度分成自由流和擁擠車流兩部分。第3頁圖1是某高速公路一個地點一個月的資料，圖說寫臨界密度接近每公里25台。

## 限制

- 只有一個地點的資料。作者說其他地點形狀相似、臨界密度也差不多，但文中沒有給其他地點的資料。
- 每公里25台是高速公路的數字，跟環道實驗的密度條件不同（22台在230公尺，我們自己換算約每公里96台，論文沒有這樣比），不能直接比較。


========== 檔案：wiki/cards/sugiyama2008-highway-comparison.md ==========

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

## 原文依據

第5頁說塞車團往後的速度約20 km/h，是高速公路上量到的塞車速度的常見值，並引用參考文獻[13]～[15]。第6頁圖5是從Treiterer和Myers的空拍圖描下來的高速公路車輛軌跡，綠線是作者加上去、代表往後20 km/h的參考線。

> the common value of the velocity of a jam measured on real highways

## 限制

- 高速公路的數字來自別的研究（[13]～[15]），我們沒有讀那些文獻。
- 圖5的綠線是作者加上去當參考的，不是對高速公路資料做擬合的結果。
- 這是作者的比較和說法，要當成「這篇論文說」，不能寫成我們確認過的事實。


========== 檔案：wiki/cards/sugiyama2008-jam-emerges.md ==========

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

## 原文依據

第4頁最後一段描述過程：自由流先維持一陣子，接著車距的小波動出現並隨時間變大，要經過一段時間才大到破壞自由流，最後幾台車被迫短暫完全停下，出現清楚的走走停停波。第5頁圖3的說明寫(a)是初始的自由流，(b)是3分鐘後的畫面，塞車由5台車組成。

> small fluctuations appeared in the headway distances and developed as time progressed

## 限制

- 「3分鐘」是圖3(b)那張照片的時間，不是量出來的「塞車開始形成的時間」。文中沒有給出波動從多小長到多大、花了多久。
- 只描述一次實驗的過程。

## 教學說法

沒有人故意踩煞車，大家只是照平常那樣跟車，幾分鐘後還是有幾台車被迫停下來。


========== 檔案：wiki/cards/sugiyama2008-mechanism.md ==========

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


========== 檔案：wiki/cards/sugiyama2008-setup.md ==========

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

## 原文依據

第4頁說明場地是平地上的環形單車道，圖2是現場照片。車數是依模型估算、讓密度滿足自由流不穩定的條件才放上去的。開始前車子被調成同一速度（約30 km/h）、間距大致均勻，駕駛被要求以約30 km/h巡航；實驗開始後只要求安全跟車並盡量維持巡航速度。

> The circumference is 230 m, and the number of vehicles is 22.

## 限制

- 車數不是隨便選的，是照模型預測挑在會不穩定的範圍。所以這個實驗支持的是「條件對了，沒有瓶頸也可能塞車」，不是「任何車數都會塞」。
- 作者自己說約30 km/h以這個車距來看偏快，是為了滿足不穩定條件。
- 沒有寫駕駛是誰、重複了幾次。

## 教學說法

研究者在一個圓形場地放了22台車，請大家用差不多的速度、保持差不多的距離繞圈，沒有紅綠燈也沒有障礙物。


========== 檔案：wiki/cards/tadaki2013-critical-density.md ==========

---
id: tadaki2013-critical-density
type: experiment
source: tadaki2013
locator: 第6頁第3段、第8頁圖5、第9頁圖7、第10～11頁
conditions: 用第一天暖身場和第二天的資料；臨界密度由車速波動和基本圖估計，沒有用任何模型
units: 台/m、台
status: confirmed
related: tadaki2013-density-dependence, tadaki2013-metastable, tadaki2013-expressway-consistency
---

## 主張

25台以下時，車速的波動小、流量隨密度增加，是順暢的自由流；28台以上時，車速波動變大、基本圖的點散開，代表出現塞車。所以臨界密度在每公尺0.08台（25台）到0.09台（28台）之間。

## 原文依據

第6頁用每一場的平均車速和標準差（圖5）判斷：第二天28到34台的場次車速波動很大，代表有塞車。第9頁圖7分開畫自由流和塞車的基本圖。第10～11頁的結論是N≤25時是自由流、N≥28時出現塞車，臨界密度在0.08和0.09之間（單位每公尺）。

> the drivers were extremely cautious on the first day and did not appear to drive at the desired speed

（這句是第6頁說明為什麼大部分第一天的資料不用。）

## 限制

- 26、27台沒有做，所以只能說臨界值在25和28台之間。
- 第一天的資料大多被排除，理由是駕駛太小心。


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

25台時所有車都順順地開，車距雖有波動但沒有變成塞車；30台時出現走走停停，停住或幾乎停住的車團以約20 km/h往後移動；34台時則是慢速的塞車團時而出現、時而消失。整體來看，車少時維持順暢、車多時出現塞車。

## 原文依據

第6頁描述圖4的三個時空圖：25台（場次2125）全部順暢；30台（場次2030）有停停走走、車團以約20 km/h往後移動，跟高速公路上的速度差不多；34台（場次2534）慢速的塞車團出現又消失。附錄B、C有每一場的時空圖。

> these show that jammed flow occurs in high density conditions while free flow is maintained at low density

## 限制

- 圖4只各挑一場當例子；同車數的其他場次在附錄B，作者沒有對重複場次做統計比較。
- 約20 km/h跟Sugiyama 2008的數字相同，是同一群作者在不同場地量到的。


========== 檔案：wiki/cards/tadaki2013-expressway-consistency.md ==========

---
id: tadaki2013-expressway-consistency
type: experiment
source: tadaki2013
locator: 第11頁第2段、第3頁圖1
conditions: 高速公路的數字來自Sugiyama 2008引用的東名高速公路資料；比較方法是作者的粗略論證
units: 台/km、台/m、km/h
status: confirmed
related: tadaki2013-critical-density, sugiyama2008-fundamental-diagram
---

## 主張

作者說，高速公路自由流平均約120 km/h、臨界密度約每公里25台；實驗自由流約40 km/h、臨界密度每公尺0.08～0.09台。車速快三倍，需要的車距也大約大三倍，所以兩者是一致的。

## 原文依據

第11頁拿高速公路的臨界密度（自由流約120 km/h時約每公里25台）跟實驗比較（自由流約40 km/h，臨界密度0.08～0.09每公尺），用車距跟車速成正比的說法認為兩者一致。

> As a car will require a headway that is three times larger when driving three times faster, our measured experimental critical density is consistent with values observed on the expressway.

## 限制

- 「車速三倍、車距三倍」是粗略的換算，不是嚴格的推導。
- 這段解決了Sugiyama 2008那張基本圖卡片裡「高速公路25台/km跟環道密度不能直接比」的問題的一部分，但只是作者的論證。


========== 檔案：wiki/cards/tadaki2013-high-density.md ==========

---
id: tadaki2013-high-density
type: experiment
source: tadaki2013
locator: 第12頁第2段、第8頁圖5、第18頁圖C.2
conditions: 40台那一場（場次1940），是第一天、沒有用在主要分析的場次
units: 台
status: confirmed
related: bando1995-stable-regions
---

## 主張

40台那一場的車速波動非常小，時空圖上車流是均勻的。作者提到有些理論模型預測密度高到一定程度時均勻車流又會變穩定，但說目前還不清楚這場觀察到的是不是那種情況。

## 原文依據

第12頁說可以看一下密度極高的情況：圖5顯示40台那一場車速波動很小，附錄的圖C.2時空圖也顯示車流均勻；有些理論模型預測超過某個高密度時均勻車流也會穩定，但目前不清楚這次觀察到的是不是模型預測的那種。

> it is not clear at present that the observed high density–flow in this case corresponds to that predicted

## 限制

- 只有一場，而且是第一天（作者說第一天駕駛特別小心）。
- 作者自己說不確定，所以不能拿來證實Bando模型「很擠時會變穩定」的結果，只能說「有一個一致的跡象」。


========== 檔案：wiki/cards/tadaki2013-metastable.md ==========

---
id: tadaki2013-metastable
type: experiment
source: tadaki2013
locator: 第9頁圖7(c)、第10頁第2段
conditions: 28～30台的場次
units: 台、台/m
status: confirmed
related: tadaki2013-critical-density
---

## 主張

車數在28到30台之間時，同一個密度下有時是順暢的自由流、有時是塞車，兩種狀態都會出現，作者稱為介穩態。

## 原文依據

第10頁說明圖7(c)：中間車數（28～30台）的場次，基本圖上一部分點落在塞車的參考線附近、其餘落在自由流的參考曲線上，所以同一個密度下兩種流都有。

> this indicates the presence of metastable states, which have previously been suggested by models and reported from observation

## 限制

- 介穩態的範圍跟臨界密度是兩件事：臨界密度是作者估的「在25台和28台之間」（每公尺0.08～0.09台），介穩態是在28～30台觀察到的。換算成密度約每公尺0.089～0.096台（環道314公尺，我們自己換算，論文沒有這樣寫）。不要跟Sugiyama 2008的230公尺環道混用。
- 只有28、30台的幾場（表1：28台2場、30台2場）。
- 「介穩態」是作者對資料的解讀。

## 教學說法

在剛好卡在邊界的擁擠程度，車流有時候撐得住、有時候會塞，要看運氣和有沒有人踩一下煞車。


========== 檔案：wiki/cards/tadaki2013-setup.md ==========

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

## 原文依據

第3～4頁說為了避免道路不均勻造成瓶頸，選了平地上的圓形環道，把巨蛋的投手丘和人工草皮移掉，周長314公尺。第5頁說用雷射掃描器量位置、兩天19場、車數10到40台、車種都是Toyota Vitz，表1列出每一場的車數和分析用的時間段。

> Fifty-two college students drove the cars by turns.

## 限制

- 第一天10台做了4場（暖身），其他車數1場；第二天28、30、32、34台各2～3場，25台1場（表1）。
- 駕駛不是隨機抽樣的一般人。
- 場次數對不上：第5頁寫兩天共19場，附錄C寫第一天做了9場，但表1列了20列（第一天10列，其中1110分析時間段是N/A）。可能是1110沒算進去，但文中沒說明，目前無法判斷。
