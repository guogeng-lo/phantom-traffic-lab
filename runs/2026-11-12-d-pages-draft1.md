# D：逐頁稿第1版，和送審前的程式檢查

- **節點和輪次**：production-plan的D（逐頁稿），節點6送審前的程式檢查第1輪；另外重跑節點5
- **日期**：2026-11-12
- **輸入**：`pipeline/outline.md`第2版、`wiki/slide-map.md`、證據卡、`wiki/glossary.md`、`model/`的測試紀錄
- **產出**：`pipeline/pages/README.md`、`p01.md`～`p10.md`；`scripts/check_pages.py`、`tests/test_check_pages.py`、`tests/mutation_check_pages.py`

## 做了什麼

每頁一份逐頁稿，段落固定：畫面和互動、顯示設定、主線、知識、進階、數字從哪來、證據卡、要小心。主線、知識、進階就是簡報上的文字。

寫的時候照兩條規則：
- 讀者能操作的範圍只限`model/`測過的參數（例如第5頁的滑桿只能停在測過的6個a值，第8頁換車的時間固定在300）。
- 頁面上的每一個數字都要列在「數字從哪來」，對到一張證據卡。

## 寫逐頁稿時發現、已經修的問題

照實記錄。這些都是寫頁面時對照證據卡和log才發現的，有幾個是檢查程式逼出來的。

| # | 問題 | 怎麼發現 | 處理 |
|---|---|---|---|
| 1 | 術語表的「平滑車」寫成「照平均速度開」，但第8頁的主要互動R3是固定目標速度 | 寫第8頁時 | 另一個commit修好（`runs/2026-11-12-n1-wiki-small-fix.md`） |
| 2 | `disputes.md`有三處還是大綱第1版之前的頁碼 | 寫第5、6、9頁時 | 同上 |
| 3 | 「塞車」的門檻（車速低於0.1）只寫在`model/CRITERIA.md`，`ours-model-click-brake`、`fast-adjust`、`near-threshold`三張卡沒寫 | 第2頁要在畫面上標「幾乎停住」 | 補進三張卡的條件 |
| 4 | `ours-model-propagation`沒寫被點的車、點擊時間、平均車距和「放大28倍」是跟哪個時間點比 | 寫第4頁時對照`model/run_core.py`的M7 | 補進條件：第0台、t0=20、車距2、比較點擊後5和200 |
| 5 | `ours-model-offset-jam`沒寫平均車距，`ours-model-click-brake`沒寫步長 | 檢查程式（數字找不到） | 補進條件 |
| 6 | **3台的結果**：第6頁第一版寫「3～15台、40～60台也跟公式一樣，小擾動不會放大」。但3台的理論成長率只有約−6e−11，照`model/CRITERIA.md`第2版只比差距、不比正負號，模擬量到的是+2.4e−8。所以不能說模擬確認3台會變小 | 檢查程式說15和40在卡片裡找不到，我去翻M2v2的逐N結果，才看到3台這一行 | 補進`ours-model-n-sweep`的限制；第6頁改成4～15台、40～60台會變小，3台另外寫「只比差距」 |
| 7 | 21台停下來的原因：卡片寫「成長太快」，實際停止條件是k=3的波超過k=1的十分之一 | 寫第6頁進階層時 | 補進`ours-model-n-sweep`的限制，頁面照實寫 |
| 8 | 第3頁主線用了「塞車團」，但正式名稱在知識層才介紹；第1頁進階層用了「均勻車流」，第2頁才介紹 | 檢查程式（P6） | 主線改成「塞住的那一團車」；第1頁改成「一樣的速度」 |
| 9 | 第5頁的有限車數分界是推導，標成【我們的模擬】會混淆 | 寫第5頁時 | 多加【我們的推導】標示（見下面「改了大綱的什麼」） |
| 10 | 第3頁寫「研究者畫實驗結果時也常用這種圖」，我們只看過兩篇 | 自己重讀 | 改成「2008年和2013年的環道實驗論文也用這種圖」 |

第6項是這次最重要的：我在整理A階段時也寫過「57個N全部相符」，這句話沒錯，但我自己推成「3～15台都確認不會放大」就錯了。檢查程式本身沒有判斷這件事的能力，它只是要求每個數字都要對到卡片，我才回頭看原始log。

## 改了大綱和slide-map的什麼

大綱第2版是使用者確認過的，這次沒有改頁面、互動或教學目標，只有兩個小地方：

- **標示多一種【我們的推導】**：大綱只有【實驗】【模型】【我們的模擬】三種。AGENTS第0節第3條本來就把推導和模擬歸成「我們自己的結果」，分開標只是更清楚，不改變證據的分類。寫在`pipeline/pages/README.md`。
- **slide-map加了逐頁稿實際用到的卡**（出處區從slide-map產生，所以兩邊要一致）：
  - 第1頁：新增一列（知識）：實驗支持「沒有瓶頸也可能塞」，不是「塞車都跟瓶頸無關」（`sugiyama2008-setup`、`sugiyama2008-mechanism`）。
  - 第3頁、第7頁：加`sugiyama2008-setup`（230公尺、22台、約30 km/h只寫在這張卡）。
  - 第5頁：加`ours-model-click-brake`（a=1會塞的結果）。
  - 第7頁：新增一列（知識、進階）：基本圖和高速公路的比較（`sugiyama2008-fundamental-diagram`、`tadaki2013-expressway-consistency`）。
  - 第9頁：加`nagel1992-rules`；新增四列：模型的其他簡化、模擬沒有單位、實驗場次少、瓶頸。

slide-map改了，所以節點5重跑：

```
$ python3 scripts/check_slide_map.py
頁數 10，對照列 23，錯誤 0 個。          exit=0（runs/logs/2026-11-12-d-slide-map-check.log）
$ python3 tests/test_check_slide_map.py
共17個情境，失敗0個。                    exit=0（runs/logs/2026-11-12-d-slide-map-tests.log）
```

## 逐頁稿的程式檢查（`scripts/check_pages.py`）

規則P1～P7寫在程式開頭，簡單說：
- P1、P2：每頁都有檔案、標題跟大綱一樣、段落齊全而且順序對。
- P3：證據卡存在、標示跟卡片類型對得上、跟slide-map那一頁的卡完全一樣。
- P4、P5：讀者看得到的每一個數字都列在「數字從哪來」，而且在那一列寫的卡片裡找得到（照小數位數四捨五入）。
- P6：術語表裡有英文的術語，第一次出現要寫「中文（英文）」。
- P7：文字用了某種標示，這頁就要有那種類型的卡。

### 跟`check_slide_map.py`不一樣的地方

- 數字可以在卡片的「限制」裡找到。頁面要照實寫限制裡的數字（例如21台只量了約190、第13台比第12台高）；slide-map的核心主張不能只靠限制，所以那邊不改。
- 「數字從哪來」可以把一列標成「顯示設定」，例如第4頁畫後面第1、5、10、15台。這種數字是呈現方式的選擇，不是證據；程式要求它出現在這頁的「顯示設定」段落裡，讓審查的人看得到。整份逐頁稿只有這一列。

### 第一次執行

寫完十頁第一次跑，**22個錯誤**。分成：
- 數字在卡片裡真的找不到：4個。第1頁的平均車距2、第2頁的步長0.05（上表第5項），第6頁的15和40（上表第6項，3台的問題就是從這裡查出來的）
- 數字在卡片的「限制」裡，程式原本只找主張、條件、原文依據：12個。這是規則本身要調整（見上一節），不是頁面錯
- 「RK4」的4、「節點7」的7被當成數字：2個。RK4改成程式排除大寫字母後面的數字；節點7改寫字
- 第4頁畫哪幾台車是顯示設定，不是證據：2個（第10、15台；第1、5台剛好在卡片裡找得到）
- 術語第一次出現沒有英文：2個（上表第8項）

上表第3、4項是寫頁面時自己對照發現的，在第一次執行之前就補進卡片，所以不在這22個裡。

**規則調整是看過第一次結果之後才做的**（多算「限制」、排除RK4這種名稱、加「顯示設定」的列）。這三項都是寫程式時沒想到的情況，不是為了讓頁面通過而放寬：每一項都有對應的測試，「顯示設定」的列還要求數字出現在顯示設定段落裡。照AGENTS第0節第5條，這裡寫明。

修完之後：

```
$ python3 scripts/check_pages.py
逐頁稿 10 頁，錯誤 0 個。                exit=0（runs/logs/2026-11-12-d-pages-check.log）
```

### 測試

- `tests/test_check_pages.py`：27個情境，失敗0個（`runs/logs/2026-11-12-d-pages-tests.log`）。
- `tests/mutation_check_pages.py`：把規則各拿掉一次，再跑測試（`runs/logs/2026-11-12-d-pages-mutation.log`）。
  - 第一次跑有一條「測試沒抓到」：行首清單編號（「1. 」）的排除。查了才知道，數字後面緊接著句點本來就不會被當成數字，所以那條規則從來沒有作用。**刪掉那條規則**，不留沒有測試的程式碼。
  - 刪掉之後，21種改法全部被測試抓到，跑完程式還原，內容相同。

### 程式檢查不到的事

- 說法有沒有超出證據、生活化的講法有沒有扭曲原意、會不會誤導：要靠節點6的獨立審查。
- 數字比對是寬鬆的：例如頁面寫「0」，卡片裡任何小於0.5的數字都算找到；數字只要在那張卡裡出現就算，不檢查是不是同一件事的數字。
- 數字後面緊接著英文句點的（例如「a=1.」）不會被抓出來。逐頁稿用中文句號，目前沒有這種寫法。
- 「畫面和互動」混著給建置的規格和讀者看得到的字，程式全部當成讀者看得到的來檢查（比較嚴，不會漏）。

## 其他檢查

| 檢查 | 結果 | log |
|---|---|---|
| `check_wiki.py` | 錯誤0、警告0 | `runs/logs/2026-11-12-d-wiki.log` |
| `tests/test_check_wiki.py` | 130個情境，失敗0 | `runs/logs/2026-11-12-d-wiki-tests.log` |
| `build_index.py --check` | 同步 | （指令輸出：index.md跟文獻檔、證據卡同步） |

## 判定

- 程式檢查：**通過**（錯誤0）。
- 這不是節點6的通過。節點6還要獨立審查，判定標準要在送審前寫好、commit。

## 下一步

1. 寫節點6的審查標準和審查包，commit之後才送審。
2. 請使用者轉貼給ChatGPT獨立對話，回覆原文貼回`runs/`。

## 輸入檔案的SHA-256

| 檔案 | SHA-256 |
|---|---|
| `pipeline/outline.md` | `8464c2aaca8ab71be8a2a21be7bd778de6532717f35f66bab2add40d7b9c84ff` |
| `wiki/slide-map.md` | `b160ea1e7b7bcd706fa0281d03d85efac8494191a065d778891cde781dde21d3` |
| `wiki/glossary.md` | `a31c4a3e793bcb9ad51ffe3a8ee8d9023b41b39d93f909dd7221ff39a28f1f51` |
| `scripts/check_pages.py` | `c25d750a91d1680f25a088fb5bdd6655b518acf523619eba7d09e752d0bb65aa` |
| `scripts/check_slide_map.py` | `d45afd114700ee10f143712750f9d41b10ac4d5de85d427c24baec1ffc6e77c7` |
| `pipeline/pages/README.md` | `802ba0afd39a5fcb88dd1bf2e1b70adfef83576262554bba8c7cdac46648d46e` |
| `pipeline/pages/p01.md` | `d64a971e753f385e552fe2745a54fab06e7f9050ec20a1e7c1e36d1d76a9810d` |
| `pipeline/pages/p02.md` | `bae2faea2ada3882b854c07a7d6005ac848f3edab30a366a2bdb93a59508299b` |
| `pipeline/pages/p03.md` | `06cbef4e1a5b5e06f6522e873322a138a123d68aecdca9578aaa8a6b8b934b42` |
| `pipeline/pages/p04.md` | `8d6ad897faa97ed246f7e40534f485911642df5577fbd9d45182bb4f35b74623` |
| `pipeline/pages/p05.md` | `652d33c6f49ffbc54b1e280a3a30d4ee6cd31262d672ae97a1787e1c931dc029` |
| `pipeline/pages/p06.md` | `7ec81f04bd0db244cda0c3dbe03f60c7770a8ada6aafeed8968d2ddf13d93075` |
| `pipeline/pages/p07.md` | `04062713264068739c90d6e06f3ebfd56e11665cbde8224d0f18fa6843791df6` |
| `pipeline/pages/p08.md` | `7cc758b737b999488a3d4274375a6da9b086b734d9e104a75ff31b0abbb77788` |
| `pipeline/pages/p09.md` | `2e5934e135710e06a0b12940b54b1d55fb028beb0ac5b079e087ace7cd247168` |
| `pipeline/pages/p10.md` | `f0e85a2c9155c5014acc03459a61543add8d115653b70b8d9a5023c82424a61b` |
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
| `wiki/cards/orosz2010-ring-stability.md` | `ccb72521184c38f5f2d47b5265b58a1d619d0cdcf2a5ef3e18761839820c283b` |
| `wiki/cards/orosz2010-stability-approaches.md` | `b18ce4b79567da3b13973d8bded3db23905c8854625c42c03db056ab44a8f317` |
| `wiki/cards/ours-finite-n-simulation.md` | `e1d21332119095e1f4a59e155db96bb56dc901156c9abc1e9e0f4ed327a3cc7c` |
| `wiki/cards/ours-finite-n-threshold.md` | `90ca47668742e4fe565927b43cc37d1f98be1ed44d5d5b1699839330d0a3de9a` |
| `wiki/cards/ours-model-click-brake.md` | `483ccb7712035bdf912320eba403b814c255e1bca315e37116b516262a278ad6` |
| `wiki/cards/ours-model-fast-adjust.md` | `c1eb1252a1f56074ba784587ae27861d87d3ea738444b6aa1ffd28df0f4399dd` |
| `wiki/cards/ours-model-n-sweep.md` | `f1cfd0354b16e501f7a7dc8aedfa551a68e9cfaa2f013c78acb139bad9c9334d` |
| `wiki/cards/ours-model-near-threshold.md` | `33012f965d2694add046eef0d7d258d91de3ba99558c9f2a21cdb2a90ccc0636` |
| `wiki/cards/ours-model-offset-jam.md` | `64bb00f8a518ecef8d52c36e5cba5fba814361aa4c5cbcb9495b042e1e6930ab` |
| `wiki/cards/ours-model-propagation.md` | `7ae400f815eda4622b2d6d960765aad1e3d98231d87624de07ee7466fab8546f` |
| `wiki/cards/ours-model-threshold.md` | `76eebbc7e168fb38ebbc70983a15cfa05c7bb7983dca82b9b399f11b674e49d5` |
| `wiki/cards/ours-model-uniform-dense.md` | `8088e5c0a764ca4df94de4d626cba6c06c0adb17474c3caa411db50a2dea2452` |
| `wiki/cards/ours-model-wave-direction.md` | `2d4e4c7546373903187cd4d8afd6675c1b1a74de5700d03c7ebea29f80fe4864` |
| `wiki/cards/ours-smoothing-r1.md` | `a5942071df96e66c14cceaed09244b875a8b97a0513dade0d678faebc4201048` |
| `wiki/cards/ours-smoothing-r2-collision.md` | `63aef5edb55e985a4ac2692caf64a3a9600d19d3e8a2fcceee53a82b4fe80205` |
| `wiki/cards/ours-smoothing-r3.md` | `6bfc1701081a921266ee5e57433f6fcd4e85b83a5c0b3883d1212dcc375645a7` |
| `wiki/cards/ours-smoothing-target-speed.md` | `40aa78936f7c3843204fc714a95df856914bc107851ba4943f055c0494475036` |
| `wiki/cards/stern2018-controllers.md` | `780ebe4917f2ece75e94a36aab12cc86fc07fd48e87e8c1dbfb0b645e54c253f` |
| `wiki/cards/stern2018-results.md` | `6c646aa9374adaa18cac7c3ba626e3aafa5e5f6a0b8cc631e6afb8aab08ee946` |
| `wiki/cards/stern2018-setup.md` | `285eb37718f26659de9a323a779108245859ccf0e8f10f2fd935377cecf06e39` |
| `wiki/cards/stern2018-wave-returns.md` | `44e1caba4342c94d97747611a7d9766fe34cd88fd74214de69b1e08598e2dae3` |
| `wiki/cards/stern2018-waves-emerge.md` | `2ec922b1026dc7c4571f94c520ac1f6788bfd9c1dc5671fab60c6abb7d1a0161` |
| `wiki/cards/sugiyama2008-23-vehicles.md` | `ee1fc7eba0ded5aea5d1c22abe32bb9fae0a821ecffc71a411c599b4dbc22b5f` |
| `wiki/cards/sugiyama2008-backward-wave.md` | `7c805e9157bead59c55e004ae342ca3c8bd68059641fcb69f3790497aba6893c` |
| `wiki/cards/sugiyama2008-fundamental-diagram.md` | `5b4e275cf71d7576e7aa5c4f3c9f2528bab4cee02dd90d6e73286b61d9145e6d` |
| `wiki/cards/sugiyama2008-highway-comparison.md` | `1821b3ebdfa55608111d23ca1c8428c0ca89c1e5c94b5b79d19e6daf92b818b7` |
| `wiki/cards/sugiyama2008-jam-emerges.md` | `52ada92ad185baee982284c6d9c8e9f2a1583845612e089d18681b04ce4974ca` |
| `wiki/cards/sugiyama2008-mechanism.md` | `edc56ceed98ead16bc7064cfddb41d9f8e09df920594445a7091ddbaebb79288` |
| `wiki/cards/sugiyama2008-setup.md` | `b49e2bf508faee3154534651e6c9748f8172b5f0c1c5e2bcb9eb0af629c01e13` |
| `wiki/cards/tadaki2013-critical-density.md` | `28172191e36bbbae688b796f526494a6bd099e65bd88445c0920fcf3319650be` |
| `wiki/cards/tadaki2013-density-dependence.md` | `11fc2986bd7fcb0a32c53dab2df341c364bb14e381573f8aab6dcd6d2a20dee1` |
| `wiki/cards/tadaki2013-expressway-consistency.md` | `866f64c147f861e072a1f3ab8ee1e51b52539c88bd7dd22a9f2c480a63b31bd4` |
| `wiki/cards/tadaki2013-high-density.md` | `21a9268b67acebb561d6d5efedb9a79295bac2e0a297759bb32485de932c315e` |
| `wiki/cards/tadaki2013-metastable.md` | `1825a7fad619e863ce2625f04adac717afdd73c9fbeca4843b4117efab7a26eb` |
| `wiki/cards/tadaki2013-setup.md` | `f0fbf5b2b1ca5762eb2f3779d37198f4623035eb789df7e79d7d1cdb5e89cb3a` |
