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

共52張。每張的條件取自卡片的conditions欄位，主張直接取自卡片的「## 主張」，都沒有另外縮寫；原文依據和限制請點進卡片看。

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
- 條件：實驗A的目標速度由外部設定、逐步調整；實驗B由受訓駕駛照外部給的目標速度開，中途調高一次；實驗C的目標速度由PI控制器自己算；控制器的參數在實驗前用模擬和現地跟車測試定好，實驗期間沒有調整外部參數

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

作者做過不同車數的實驗，文中只提到23台的結果：也形成了塞車團，這個塞車團的移動速度跟22台時的塞車團一樣。

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

#### [ours-model-click-brake](cards/ours-model-click-brake.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py第3版（煞車用整數步數判定）；N=22、L=44、a=1；點擊前用解析解；煞車β=0.25、持續τ=0.5（剛好10步）；「塞車」照model/CRITERIA.md的定義：有任何一台車的車速低於0.1；RK4，dt=0.05

第2頁的展示做法：讀者點擊之前，均勻車流用公式算，永遠保持等距等速；點擊那一刻才開始數值積分並讓那台車短暫減速。用最輕的煞車（β=0.25、τ=0.5），點擊後模型時間89.3出現塞車；不論在20還是500點擊，結果都一樣。切換時位置、速度、時間都連續。

#### [ours-model-fast-adjust](cards/ours-model-fast-adjust.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py第3版；N=22、L=44；a=2.2、2.5、3.0；跟第2頁一樣的煞車；「塞車」照model/CRITERIA.md的定義：有任何一台車的車速低於0.1

每台車調整速度夠快（a=2.2、2.5、3.0）時，同樣點一下，不會形成塞車，擾動在300模型時間內衰減到0.01以下（4e−4、1e−4、2e−5）。

#### [ours-model-n-sweep](cards/ours-model-n-sweep.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；L=44、a=1；N=3～60；k=1的小擾動；RK4，dt=0.05；量法照model/CRITERIA.md第2、3版

環長44、a=1時，解析推導預測16～39台會放大。正式模型的數值驗證：58個N裡57個量測資料足夠，全部跟理論相符；其中會放大的是16～20、22～39台。21台因為成長太快、量測區間不到事先規定的200，標為數值無法判定，不能說已經通過數值驗證。

#### [ours-model-near-threshold](cards/ours-model-near-threshold.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py第3版；N=22、L=44；a=1.90～2.10；第2頁的煞車和三倍煞車；跑到點擊後1500；「塞車」照model/CRITERIA.md的定義：有任何一台車的車速低於0.1

分界（約1.96）附近變化很慢。a=1.90、1.94理論上會放大，但點擊後1500模型時間內都還沒形成塞車，擾動只是慢慢變大；a=1.98～2.10的擾動慢慢變小。這次測的煞車大小，沒有看到理論說穩定、卻出現塞車的情況。

#### [ours-model-offset-jam](cards/ours-model-offset-jam.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；N=22、L=44、a=1；一開始均勻，只把第0台車往前移ε；RK4，dt=0.05；平均車距2（L/N）

模型裡，只把一台車往前偏一點點，也會長成塞車（有車的速度低於0.1）。偏0.1時在模型時間92出現，偏0.01時在120.5，偏0.2時在87。

#### [ours-model-propagation](cards/ours-model-propagation.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py第3版；N=22、L=44；第2頁的煞車；a=1和a=2.5對照；平均車距2（L/N）；在t0=20點第0台；整體擾動是所有車裡車速跟均勻車流差最多的值，比較點擊後5和200模型時間的大小；逐台的最低速度取點擊後100模型時間內

同樣點一下，a=1時擾動在200模型時間內放大28倍，a=2.5時縮到0.03倍。a=1時，被點那台後面21台的最低速度，有19台比前一台低，但不是每一台都更低。

#### [ours-model-threshold](cards/ours-model-threshold.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；V=tanh(h−2)+tanh2；N=22、L=44（車距2）；RK4，dt=0.05；只加k=1的小擾動（10^−6）；沒有延遲

正式模型用二分法量出22台、車距2的分界a是1.959494，公式是1.959493。分界附近7個a值，量到的成長率跟理論的差都在1e−5以下，而且正負號一致。

#### [ours-model-uniform-dense](cards/ours-model-uniform-dense.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；N=44、L=44（車距1）、a=1；RK4，dt=0.05

44台擠在環長44的環上時，均勻車流的速度是0.2024（V(1)），模擬跑到1000一直維持這個速度，誤差2e−11；加上小擾動也會衰減，衰減率跟理論一樣。也就是大家一起很慢地走，但小擾動不會放大。

#### [ours-model-wave-direction](cards/ours-model-wave-direction.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py第3版；N=22、L=44、a=1；第2頁的煞車；取樣間隔0.5和0.05；追同一團塞車（至少3台相鄰的車速度低於0.1才開始）

模型裡，車的平均速度是+0.9632（往前），塞車團的移動速度是−0.1505（往後）。兩種取樣間隔量到的一樣，畫時空圖時跨越起點的處理沒有錯誤。

#### [ours-smoothing-r1](cards/ours-smoothing-r1.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；N=22、L=44、a=1；同R3的情境；規則：a_s·(min(U_avg, V(h))−v)，U_avg是自己過去50的平均速度，a_s=1

在我們的模型裡，平滑車改成照自己過去的平均速度開時，分三方面看：車速波動完全消失（剩0%），整條車流變成均勻；但平均車速從0.966降到0.763，少了約21%；安全方面，最小車距0.325，沒有撞車。

#### [ours-smoothing-r2-collision](cards/ours-smoothing-r2-collision.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；N=22、L=44、a=1；同R3的情境；規則：照原本的模型，但加速度限制在±0.05

在我們的模型裡，只限制平滑車的加速度、沒有安全機制時會撞車（最小車距變成−14.5，物理檢查失敗）。車速波動雖然剩50%，但這是失敗的規則，不能當可用的策略。

#### [ours-smoothing-r3](cards/ours-smoothing-r3.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；N=22、L=44、a=1；先讓塞車形成，t=300把第0台換成平滑車；比較區間[1000, 1500]；規則：a_s·(min(U, V(h))−v)，U=V(2)=0.9640，a_s=1

在我們的模型裡，把一台車換成「固定目標速度、但車距不夠就照模型減速」的平滑車後，分三方面看：車速波動剩原本的42%，比較區間裡沒有車慢到0.1以下；平均車速從0.966變成0.887；安全方面，最小車距0.326，沒有撞車。

#### [ours-smoothing-target-speed](cards/ours-smoothing-target-speed.md)

- 類型：our_simulation
- 狀態：confirmed
- 條件：model/ovm.py；同R3的情境；目標速度U=V(2)×0.9、1.0、1.05、1.1、1.2

在我們的模型裡，R3平滑車的目標速度設得越快，剩下的車速波動越大：U=V(2)時是原本的42%，×1.05是49%，×1.1是55%，×1.2是63%；但這幾組都沒有重新形成塞車。U設得比大家慢（×0.9）時，車流反而完全均勻，平均車速0.868。

<!-- 自動產生結束 -->
