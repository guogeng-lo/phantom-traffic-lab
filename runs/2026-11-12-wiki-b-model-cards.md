# B：模型結果的證據卡、術語、頁面對照

- **類別**：Wiki補充（節點1的小修改），`production-plan.md`的B
- **日期**：2026-11-12
- **依據**：使用者在模型A階段結束時的決定（核心模型驗證結束，進入B）

## 做了什麼

### 術語表

加「時空圖（time-space diagram）」。出處寫Sugiyama 2008第6頁圖4，那張圖畫的是每台車在環道上的軌跡（位置對時間）。也寫了簡報採用的方向：橫軸位置、縱軸時間、時間往下增加。

### 13張【我們的模擬】證據卡（`type: our_simulation`）

每張的source都是repo裡的log或紀錄，locator是測試名稱。主張裡的數字都對過log。

| 卡片 | 測試 | 給哪一頁 |
|---|---|---|
| `ours-model-threshold` | M1 | 5 |
| `ours-model-n-sweep` | M2（三版的結果都寫進卡片） | 6 |
| `ours-model-uniform-dense` | M3 | 6 |
| `ours-model-offset-jam` | M4 | 1 |
| `ours-model-click-brake` | M5a v2、M5b | 2 |
| `ours-model-fast-adjust` | M5c | 4、5 |
| `ours-model-near-threshold` | M5d | 5 |
| `ours-model-wave-direction` | M6v2 | 3 |
| `ours-model-propagation` | M7 | 4 |
| `ours-smoothing-r3` | M8 R3 | 8 |
| `ours-smoothing-r1` | M8 R1 | 8 |
| `ours-smoothing-r2-collision` | M8 R2 | 8 |
| `ours-smoothing-target-speed` | M9 | 8 |

照使用者的要求：

- **M2**：卡片分開寫三件事：
  - 解析推導預測16～39台會放大。
  - 數值驗證了16～20、22～39台。
  - 21台量到的成長率接近理論，但未達事先規定的有效區間長度，不能說已經通過數值驗證。
- **第8頁的四張卡**：
  - 都把車速波動、平均車速、安全性分開寫。
  - 都註明是我們自己設計的規則，不是Stern的控制器。
  - R1寫明平均車速少約21%的代價。
  - R2寫明撞車、只能當失敗案例。
  - M9寫明沒有重新形成塞車，不能說重現了Stern實驗A。
  - 也寫明平均車速跟Stern的通過量不是同一個指標。
- **M8、M9的模擬是第3版求解器修正之前跑的**，卡片限制裡都寫了，並引用R7的逐位元相同結果。

### 頁面對照

`wiki/slide-map.md`原本還沒建的模擬卡，全部換成上面的正式卡片。第6頁的核心主張改寫成理論預測、模擬驗證、21台無法判定三段。第8頁拆成兩列：平滑車規則、第三題。

## 檢查結果

```
$ python3 scripts/build_index.py
$ python3 scripts/check_wiki.py
文獻 6 篇（算進5篇的獨立論文 6 篇），證據卡 52 張（pending 0 張）。
錯誤 0 個，警告 0 個。
exit=0                                   （runs/logs/2026-11-12-wiki-b-check.log）

$ python3 scripts/build_index.py --check
index.md跟文獻檔、證據卡同步
exit=0                                   （runs/logs/2026-11-12-wiki-b-index.log）

$ python3 scripts/check_quotes.py
引用 31 段：逐字找到 22，OCR逐字 8，OCR近似 1，找不到 0，無法比對 0。
exit=0                                   （runs/logs/2026-11-12-wiki-b-quotes.log）
```

新卡片都沒有英文引用，所以引用數不變。

## 寫卡片時改掉的錯

`ours-model-offset-jam`第一稿把ε = 0.01的塞車時間寫成「120」，log是120.5。對log時發現，改成120.5後重建索引、重跑檢查，上面的輸出是改過之後的。
