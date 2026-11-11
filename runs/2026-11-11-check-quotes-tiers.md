# 引用比對程式改成分層回報（2026-11-11）

這份不是Graph節點的執行紀錄，是第2關要用的`scripts/check_quotes.py`在準備第二批（NaSch 1992、Tadaki 2013）時發現問題、修改、再測試的紀錄。

## 發現的問題

1. **NaSch 1992的文字層不能信**：PDF有文字層，但跨欄的字被混在一起，字的順序是亂的。舊版只有在文字層幾乎是空的時候才用OCR，所以NaSch的引用大多會被判成找不到。
2. **之前的報告把兩種查核方式混在一起**：舊版遇到Bando 1995這種掃描檔，會直接用OCR文字，OCR裡逐字找到的也報成「逐字找到」。所以前兩篇的紀錄寫「逐字找到11」，實際上有5段是OCR逐字。使用者確認前兩篇時剛好提醒過「OCR的結果不能改稱逐字驗證」，結果是程式本身就混在一起了。已經在`2026-11-11-n1-bando1995-r1.md`和`2026-11-11-review-first-two.md`後面補上更正。

## 怎麼判斷文字層可不可靠

用「三個連續英文字」的重疊比例：OCR文字裡的三字組，有多少也出現在文字層裡。先量現有的4份PDF：

```
sugiyama2008 overlap=0.96
nagel1992 overlap=0.39
tadaki2013 overlap=0.96
bando1995 overlap=0.00
```

依這個結果把門檻定在0.8。定門檻的時候，第二批的證據卡還沒寫，也還沒有拿任何新引用去比對。

## 新的規則

1. 先在文字層逐字找 →「逐字找到」
2. 找不到才做OCR，算重疊比例。文字層可靠（>= 0.8）的話，找不到就是錯誤。
3. 文字層不可靠時：OCR裡逐字找到 →「OCR逐字」；不然做近似比對，相似度 >= 0.9、而且數字完全相同 →「OCR近似」；其他都是錯誤。
4. OCR逐字和OCR近似都要人對照頁面確認，報告要照實寫。

## 故意改壞引用的測試

改了3張卡的引用（測完都改回來）：

| 改法 | 預期 | 第1次結果 |
|---|---|---|
| Sugiyama「22」改成「23」（文字層可靠） | 錯誤 | 錯誤 |
| Bando「five」改成「6」（掃描檔，數字變了） | 錯誤 | 錯誤（最接近的相似度0.98） |
| Bando「do not introduce」改成「do introduce」（意思相反） | 錯誤 | **OCR近似，相似度0.96，沒抓到** |

第1次輸出：

```
[OCR近似] bando1995-no-delay.md：相似度 0.96，要對照PDF頁面確認：Moreover we do introduce the time lag of response.
[錯誤] bando1995-spontaneous-jam.md：PDF裡找不到這段引用（最接近的相似度 0.98）：From this figure, we find that 6 clusters of congestion are formed even from a very tiny disturbance existing in the almost uniform vehicle distribution.
[錯誤] sugiyama2008-setup.md：PDF裡找不到這段引用：The circumference is 230 m, and the number of vehicles is 23.
```

**修改**：OCR近似除了數字要一樣，否定詞（not、no、never、without等）和un開頭的字（例如unstable）也要一樣。這條是看過測試結果才加的。

第2次只重測意思相反的那一段：

```
[錯誤] bando1995-no-delay.md：PDF裡找不到這段引用（最接近的相似度 0.96）：Moreover we do introduce the time lag of response.
```

改回正確內容後，全部重跑：

```
引用 12 段：逐字找到 6，OCR逐字 5，OCR近似 1，找不到 0，無法比對 0。
```

## 還擋不住的

掃描檔裡，一般字詞被換掉（例如backward改成forward），相似度還是可能超過0.9，會被當成OCR近似。所以OCR近似一定要人對照頁面圖片確認，這是程式做不到、要人做的部分。這支程式也還沒有自動化測試，目前只有這份紀錄裡的手動改壞測試。
