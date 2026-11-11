# 選題階段的模型驗證

這裡是選題時做的可行性測試，**不是**正式的Wiki → Graph → HTML流程。目的是在決定題目之前，先確認幽靈塞車的核心現象能不能用程式正確重現，而且能用數學條件檢查，不是只做出看起來像塞車的動畫。

## 模型

Bando等人1995年的最佳速度模型（Optimal Velocity Model），環狀道路，22台車：

- 每台車的加速度：`dv/dt = a[V(h) - v]`，h是到前車的距離，a是跟車調整強度
- `V(h) = tanh(h - 2) + tanh(2)`，無因次單位
- 用RK4積分，位置每一步對環長取餘數

假設和限制：所有駕駛都一樣、沒有隨機性、單車道不能超車、單位是無因次的（還沒對應到真實的公尺和秒）。這些都還要等正式的Wiki讀過原文才能確認。

## 怎麼重跑

需要Python 3，只用標準函式庫（畫圖的`plot.py`需要matplotlib）。在這個資料夾裡執行：

```
python3 test_ovm.py        # 17項測試，輸出應該跟run2.log一樣
python3 page3_check.py     # 固定環長改車數，輸出應該跟page3_check.log一樣
python3 plot.py            # 重畫timespace.png
```

## 檔案

| 檔案 | 內容 |
|---|---|
| `ovm.py` | 模擬和線性穩定性理論 |
| `test_ovm.py` | A穩定性、B數值正確性、C可觀察性，共17項 |
| `run1.log` | 第1次執行：16項失敗2項 |
| `run2.log` | 修正測試標準後第2次執行：17項全過 |
| `diag.py` | 查第1次失敗原因用的診斷程式 |
| `page3_check.py`、`page3_check.log` | 第3頁分鏡寫錯之後的補測 |
| `timespace.png` | 時空圖 |
| `CHECKLOG.md` | 失敗、原因、修正和更正的完整紀錄 |

第2次的測試標準是看過第1次結果之後才改的，`CHECKLOG.md`有寫清楚。
