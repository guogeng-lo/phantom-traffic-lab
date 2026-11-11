# 科學內容修正：第4輪的兩條不精確

- **類別**：科學內容修正
- **日期**：2026-11-12
- **依據**：`runs/2026-11-12-n3-review-r4.md`（第4輪不通過），以及使用者第4輪後的決定第1點：照論文修正、重建索引、保留核對紀錄，不再送完整科學審查
- **範圍**：只有下面兩條，其他研究內容沒有重審

## 修正

| 檔案 | 改了什麼 | 原文依據 |
|---|---|---|
| `wiki/cards/sugiyama2008-23-vehicles.md` | 主張改成「這個塞車團的移動速度跟22台時的塞車團一樣」；原文依據註明its指塞車團 | Sugiyama第5頁：「In the case of 23, a jam cluster was formed and its velocity was the same as the case of 22」 |
| `wiki/cards/stern2018-wave-returns.md` | `conditions`裡實驗C的部分，從「沒有外部參數」改成：PI控制器自己算目標速度；控制器的參數在實驗前用模擬和現地跟車測試定好；實驗期間沒有調整外部參數。原文依據補上第7頁，`locator`補第7頁第3.2節 | Stern第7頁第3.2節：兩種控制器的參數是在實驗前用模擬環境和現地跟車測試決定的。第10頁：「there are no external parameters that are changed during the experiment」 |

頁碼用`pdftotext -layout`的頁尾頁碼對過：Stern第3.2節的參數段落在第7頁。

## 重建索引和核對

改完跑`python3 scripts/build_index.py`。索引裡這兩張卡的條件和主張跟卡片一致，`build_index.py --check`的結果是同步。

```
$ python3 scripts/check_wiki.py
文獻 6 篇（算進5篇的獨立論文 6 篇），證據卡 39 張（pending 0 張）。
錯誤 0 個，警告 0 個。
exit=0                                  （runs/logs/2026-11-12-eng-science-check.log）

$ python3 scripts/build_index.py --check
index.md跟文獻檔、證據卡同步
exit=0                                  （runs/logs/2026-11-12-eng-science-index.log）

$ python3 scripts/check_quotes.py
引用 31 段：逐字找到 22，OCR逐字 8，OCR近似 1，找不到 0，無法比對 0。
exit=0                                  （runs/logs/2026-11-12-eng-science-quotes.log）
```

英文引用沒有改，所以引用數不變。

## 第4輪的「無法確認」：Stern B的6.25和6.26

第10、12頁寫6.25 m/s，表2的時段名稱寫6.26 m/s。卡片用的是第10頁正文的「14 mph（6.25 m/s）」，沒有改。這是原文自己有兩種寫法，不是我們讀錯。
