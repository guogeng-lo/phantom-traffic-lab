# 節點8：上游紀錄和SHA-256一致性核對

- **日期**：2026-11-13，commit `7e28eb8`
- **方法**：`python3 scripts/check_stale.py`列出每份紀錄記的檔案現在有沒有改過；過期的，再查改了什麼、有沒有被後面的審查涵蓋。照使用者的決定，只有實質影響證據、條件、限制或主張、而且沒被審查過的變更，才做限定範圍補查。
- **結論**：**沒有需要補查的變更**。程式檢查全部重跑，都通過。

## check_stale的結果

過期的紀錄：節點1的6份ingest紀錄、D階段逐頁稿初稿、節點5、節點7第1～3輪。最新的：節點6第4輪、節點7限定修補結果。（節點3的審查紀錄沒有SHA-256表格，用下面的方法核對。）

## 逐項核對

| 項目 | 改了什麼 | 有沒有被審查涵蓋 | 要不要補查 |
|---|---|---|---|
| 文獻檔、文獻證據卡（節點1→節點3） | 節點3第1～4輪照ChatGPT審查修改（到commit `7506be9`為止） | 節點3的科學審查本身就是審這些修改；之後**沒有任何文獻卡或文獻檔再改過**（`git diff --stat 7506be9 HEAD -- wiki/sources`和文獻卡都沒有差異） | 不用 |
| 我們的模擬卡13張（`ours-model-*`、`ours-smoothing-*`） | 節點3之後新增（`8eecb9f`），後來補條件和限制（`1e38557`、`682a889`） | 節點6第1～4輪的審查包都附了這些卡的全文；**現在的檔案跟第3、4輪審查包裡的全文一字不差**（44張用到的卡，44張一樣） | 不用 |
| `wiki/glossary.md` | 加「時空圖」、改「平滑車」的定義 | 27列都在節點6第3輪審查包裡，一字不差 | 不用 |
| `wiki/disputes.md` | 只把參照的頁碼改成大綱第2版（例如「第3頁」改成「第6頁（大綱第2版）」），沒有改主張 | 不影響證據或主張 | 不用 |
| `wiki/index.md` | 自動產生的文獻表和證據卡清單 | 由`build_index.py`產生，`check_wiki.py`會檢查跟卡片同步 | 不用 |
| `wiki/slide-map.md`（節點5過期） | 節點6期間依審查補對照列 | 節點5是程式檢查，重跑`check_slide_map.py`通過；slide-map用到的44張卡都在節點6審查包裡 | 不用（重跑） |
| `pipeline/outline.md` | 節點4使用者確認之後，記錄節點6各輪的使用者決定 | 都是使用者自己的決定 | 不用 |
| 逐頁稿p01～p10 | 節點6第4輪之後沒有再改 | 節點6第4輪紀錄是最新的 | 不用 |
| 節點7第1～3輪 | 後面的修補改了`web/deck.js`、`docs/index.html`、幾個測試 | 最新的狀態由`2026-11-13-n7-perf-patch-result.md`涵蓋（最新），節點7帶已知未通過項目轉入節點8（`2026-11-13-n7-risk-acceptance.md`） | — |

## 重跑的程式檢查

輸出原文在`runs/logs/2026-11-13-n8-*.log`，全部結束代碼0：

| 檢查 | 結果 |
|---|---|
| `check_wiki.py` | 錯誤0、警告0 |
| `tests/test_check_wiki.py` | 130個情境，失敗0 |
| `check_slide_map.py` | 10頁、24列，錯誤0 |
| `tests/test_check_slide_map.py` | 17個情境，失敗0 |
| `check_pages.py` | 10頁，錯誤0 |
| `tests/test_check_pages.py`、`mutation_check_pages.py` | 27個情境失敗0；把規則拿掉後測試都抓得到，還原後內容相同 |
| `check_quotes.py` | 31段引用：逐字22、OCR逐字8、OCR近似1、找不到0。結果跟2026-11-12的三次執行完全一樣（`eng-science-quotes.log`等）。OCR的9段照規則要人對照頁面；ingest紀錄記了當時的人工對照（例如`2026-11-11-n1-bando1995-r1.md`），**這次沒有重新逐段對照** |

## 輸入

| 檔案 | SHA-256 |
|---|---|
| `wiki/sources/bando1995.md` | `fa31a7abc9f7265f818f479dc4e92b4f7f7eb8d7806316324c2a75b94a47ecc6` |
| `wiki/sources/nagel1992.md` | `3b2d4e6facadd89f4e5ebf57a14cb67e586512eed18fa59690e7202db04c8825` |
| `wiki/sources/orosz2010.md` | `0ccdc9adeabfc3ff3f8c29794dae350fca93faf088587526e291e965aade7676` |
| `wiki/sources/stern2018.md` | `dddbab143c9aec53262e7ea21843b7ba4d94611dba23c8e6ec9b87fc29889e09` |
| `wiki/sources/sugiyama2008.md` | `a7a7113d3e307ef9324026ef7e3505ace5c80beba5e0a618ef140fffe1ed74b5` |
| `wiki/sources/tadaki2013.md` | `820a2f2c9cf91befb7078f6411b119c6ab4fd4a0ecbdec11e35876a30e988f1a` |
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
| `wiki/cards/ours-model-n-sweep.md` | `34e792230e3b22e943b7af0616914f03d19506540a199f042bffefc8826e7e8f` |
| `wiki/cards/ours-model-near-threshold.md` | `33012f965d2694add046eef0d7d258d91de3ba99558c9f2a21cdb2a90ccc0636` |
| `wiki/cards/ours-model-offset-jam.md` | `64bb00f8a518ecef8d52c36e5cba5fba814361aa4c5cbcb9495b042e1e6930ab` |
| `wiki/cards/ours-model-propagation.md` | `c4644e119e5c06ca6a06ca415bc82551820103e09c5e6151e0541e254b576b64` |
| `wiki/cards/ours-model-threshold.md` | `76eebbc7e168fb38ebbc70983a15cfa05c7bb7983dca82b9b399f11b674e49d5` |
| `wiki/cards/ours-model-uniform-dense.md` | `8088e5c0a764ca4df94de4d626cba6c06c0adb17474c3caa411db50a2dea2452` |
| `wiki/cards/ours-model-wave-direction.md` | `2d4e4c7546373903187cd4d8afd6675c1b1a74de5700d03c7ebea29f80fe4864` |
| `wiki/cards/ours-smoothing-r1.md` | `a5942071df96e66c14cceaed09244b875a8b97a0513dade0d678faebc4201048` |
| `wiki/cards/ours-smoothing-r2-collision.md` | `63aef5edb55e985a4ac2692caf64a3a9600d19d3e8a2fcceee53a82b4fe80205` |
| `wiki/cards/ours-smoothing-r3.md` | `93550a95b7c02f189034cc3df3bf3326f18c7d3826d0c57a30c4db6053824e4c` |
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
| `wiki/glossary.md` | `a31c4a3e793bcb9ad51ffe3a8ee8d9023b41b39d93f909dd7221ff39a28f1f51` |
| `wiki/disputes.md` | `ae811f4b92a606bf9177bc0826975ff0fd92be6459a2733ab26c1601a4667e14` |
| `wiki/index.md` | `ea8acaf26d439199cb2f962a700978e5eb05d6355d4f72047fa79a4df4f9bf34` |
| `wiki/slide-map.md` | `43aa24294226bb2afea31350a0f3a52838258def0336894ed8305f3822fdf764` |
| `pipeline/outline.md` | `da76c294d2e30881ae00acc2ce510b2dbf2b056f533dff07dfb25a452bbd225b` |
| `pipeline/pages/p01.md` | `a5a55c44fed05884436f0b1882d780d33d2bec8d41f8b8d97778c42b199ebab1` |
| `pipeline/pages/p02.md` | `e99e9b4430cd165310fe80b74bfd4d4687c8eb50d335d77b8054d7a9f9056fd8` |
| `pipeline/pages/p03.md` | `621c7aebe5efdc6d6d5dd23faaba132e1f8182f14d19d31dba9da191ab9c5f5f` |
| `pipeline/pages/p04.md` | `9b5c4fb7e17afc65dae54213b545c2c537372f3a5d235906ca726ed9fb360acd` |
| `pipeline/pages/p05.md` | `1e1686b92611178d58c50c1fcb00d3e1538cc4743df5085556efebb2407f7448` |
| `pipeline/pages/p06.md` | `3fe4f941f00f34eff748784a4feaa0c67f481740d6d51d36aef5caae06cb359e` |
| `pipeline/pages/p07.md` | `a95a23f79f162210e13f940621c70bd2d088b8823ee6d0839a9362a7efda88e9` |
| `pipeline/pages/p08.md` | `749075d133d57f41ba1ee1d7d1025ba4f3e55f276d1a90971d87428ff38bc42e` |
| `pipeline/pages/p09.md` | `469c62fd8121d7fb200b799055df93b03cde4dbea9e044828ca3649da2d5de3b` |
| `pipeline/pages/p10.md` | `428502ff618e25ac210e1713685eca8101ab72c1a8d167e0530a0f6756d899c7` |
