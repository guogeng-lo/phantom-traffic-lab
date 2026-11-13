# Phantom Traffic Lab：幽靈塞車

沒有紅燈、沒有事故、沒有施工，車流還是會自己塞住，而且塞車波會往後跑。這個專案把相關研究整理成一份可以追溯出處的LLM Wiki，再用它做一份讀者可以自己操作的教學HTML簡報。

這個專案由我負責選題、需求確認、各關的決策和最終驗收；Wiki整理、程式實作和自動測試主要交給Claude，科學內容、逐頁稿和簡報則另外交給ChatGPT獨立審查。

- **簡報**：https://guogeng-lo.github.io/phantom-traffic-lab/ （GitHub Pages，從`docs/`發佈）
- **Wiki入口**：[`wiki/index.md`](wiki/index.md)
- **Graph／Loop的總整理**：[`runs/2026-11-13-graph-loop-summary.md`](runs/2026-11-13-graph-loop-summary.md)

**目前進度：節點8完成，最終驗收通過。**節點7帶著一項已知沒通過的自動測試（動畫CPU）進入節點8，這是我授權的，見[`runs/2026-11-13-n7-risk-acceptance.md`](runs/2026-11-13-n7-risk-acceptance.md)；真機測試和交件檢查見[`runs/2026-11-13-n8-final-check.md`](runs/2026-11-13-n8-final-check.md)。
- **反思**：[`runs/2026-11-13-n8-reflection.md`](runs/2026-11-13-n8-reflection.md)

## 這個專案在做什麼

- **Wiki**：6篇論文，每篇記錄實際讀到哪裡；每個主張一張證據卡，標明是論文裡的實驗、論文裡的模型，還是我們自己推導或模擬的結果。
- **簡報**：10頁。讀者自己點車子踩煞車、看塞車波怎麼往後傳、調整條件看小擾動什麼時候會放大。所有模擬都在讀者的瀏覽器裡即時算（`web/ovm.js`），跟Python參考模型對過答案。每頁都可以展開「出處和檢查」，看到對應的證據卡和建置時實際執行的檢查結果。
- **流程**：從Wiki到簡報分成8個節點，程式檢查和AI審查分開，錯了就退回出問題的那一關。設計在`.agents/workflows/graph.md`，每次執行的紀錄在`runs/`，失敗的也都留著。

## 資料夾

| 位置 | 內容 |
|---|---|
| `wiki/` | 文獻、證據卡、術語表、研究差異、簡報對照表，從`wiki/index.md`開始看 |
| `pipeline/` | 需求摘要、教學大綱、逐頁稿、審查包 |
| `model/` | Python參考模型和它的測試 |
| `web/` | 簡報的樣板、樣式、互動程式、瀏覽器求解器 |
| `docs/` | 建置出來的簡報（不要手改，用`scripts/build_site.py`產生） |
| `runs/` | 每次執行的檢查和審查紀錄，包括失敗的。節點1～7的紀錄是當時邊做邊寫的，裡面的「使用者」指的就是我 |
| `diagnostics/` | 節點7效能診斷用的暫時性腳本（不是驗收測試） |
| `audition/` | 選題階段的模型驗證（不是正式流程） |
| `scripts/`、`tests/` | 檢查和建置程式、它們的測試 |
| `AGENTS.md` | 給AI的規則，也列出全部的檢查指令 |

## 怎麼建置和檢查

需要Python 3（只用標準函式庫）和Node.js。瀏覽器測試要Playwright；無障礙和效能測試要先`npm install`。

```
python3 scripts/check_wiki.py            # 文獻、證據卡、索引，並掃描個資和金鑰
python3 scripts/build_site.py            # 建置docs/index.html，會實際執行檢查和JS對答案，結果寫進每頁的出處
node tests/test_js_parity.js             # 瀏覽器求解器跟Python參考答案對答案
node tests/e2e_flow.js [--mobile]        # 用Playwright實際操作全部互動
```

完整的指令清單在`AGENTS.md`第9節。論文PDF不上傳，要檢查引用的話自己放到`raw/`。

## 已知限制

- 動畫CPU的自動測試（CPU慢4倍、忙碌比例≤60%）沒有通過，而且在無頭、沒有GPU的測試環境量不穩（同一個版本36次有19次超過60%）。我用真實Android手機開正式網址測過，操作都流暢。
- 模型是無因次的；平滑車的規則是我們自己設計的，不是實驗用的控制器。
- 檢查程式只能抓到測過的情境；個資掃描只認得常見格式。

## 授權

程式碼用MIT，Wiki文字和簡報內容保留所有權利，第三方素材照各自的授權。詳細範圍見`NOTICE.md`。
