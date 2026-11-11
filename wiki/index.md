# 幽靈塞車Wiki索引

這份Wiki整理「沒有事故為什麼也會塞車」的研究，是教學簡報的知識來源。每篇文獻和每張證據卡都要列在這裡，`scripts/check_wiki.py`會檢查。

- 術語：[glossary.md](glossary.md)
- 研究差異與未解問題：[disputes.md](disputes.md)
- 簡報頁面和證據卡的對照：[slide-map.md](slide-map.md)

## 文獻

| id | 種類 | 閱讀狀態 | 檔案 |
|---|---|---|---|
| bando1995 | paper | 全文已讀 | [sources/bando1995.md](sources/bando1995.md) |
| nagel1992 | paper | 全文已讀 | [sources/nagel1992.md](sources/nagel1992.md) |
| tadaki2013 | paper | 全文已讀 | [sources/tadaki2013.md](sources/tadaki2013.md) |
| sugiyama2008 | paper | 全文已讀 | [sources/sugiyama2008.md](sources/sugiyama2008.md) |

## 證據卡

| id | 類型 | 狀態 | 主張 | 檔案 |
|---|---|---|---|---|
| nagel1992-rules | model_theory | confirmed | 格子模型的4條規則 | [cards/nagel1992-rules.md](cards/nagel1992-rules.md) |
| nagel1992-randomization | model_theory | confirmed | 隨機減速是這個模型產生真實感的關鍵 | [cards/nagel1992-randomization.md](cards/nagel1992-randomization.md) |
| nagel1992-circle-jams | model_theory | confirmed | 密度高時塞車隨機出現、往後移動 | [cards/nagel1992-circle-jams.md](cards/nagel1992-circle-jams.md) |
| nagel1992-transition | model_theory | confirmed | 轉變在每格約0.08台附近，確切位置不清楚 | [cards/nagel1992-transition.md](cards/nagel1992-transition.md) |
| nagel1992-real-units | model_theory | confirmed | 一格7.5公尺、一步約0.5～1秒 | [cards/nagel1992-real-units.md](cards/nagel1992-real-units.md) |
| nagel1992-bottleneck | model_theory | confirmed | 瓶頸情境下車流自己穩定在某個狀態 | [cards/nagel1992-bottleneck.md](cards/nagel1992-bottleneck.md) |
| tadaki2013-setup | experiment | confirmed | 名古屋巨蛋314公尺環道，10～40台車 | [cards/tadaki2013-setup.md](cards/tadaki2013-setup.md) |
| tadaki2013-density-dependence | experiment | confirmed | 車少順、車多塞，塞車團約20 km/h往後 | [cards/tadaki2013-density-dependence.md](cards/tadaki2013-density-dependence.md) |
| tadaki2013-critical-density | experiment | confirmed | 臨界密度在每公尺0.08到0.09台之間 | [cards/tadaki2013-critical-density.md](cards/tadaki2013-critical-density.md) |
| tadaki2013-metastable | experiment | confirmed | 中間密度時順暢和塞車都會出現 | [cards/tadaki2013-metastable.md](cards/tadaki2013-metastable.md) |
| tadaki2013-expressway-consistency | experiment | confirmed | 作者說跟高速公路的臨界密度一致 | [cards/tadaki2013-expressway-consistency.md](cards/tadaki2013-expressway-consistency.md) |
| tadaki2013-high-density | experiment | confirmed | 40台時反而均勻，但作者說還不確定 | [cards/tadaki2013-high-density.md](cards/tadaki2013-high-density.md) |
| bando1995-ovm-equation | model_theory | confirmed | 跟車方程式：加速度＝a×(想開的速度－現在速度) | [cards/bando1995-ovm-equation.md](cards/bando1995-ovm-equation.md) |
| bando1995-linear-stability | model_theory | confirmed | V'(b)<a/2時均勻車流穩定，對任何速度函數都成立 | [cards/bando1995-linear-stability.md](cards/bando1995-linear-stability.md) |
| bando1995-large-n-note | model_theory | confirmed | 作者：車數和環長夠大時邊界條件不重要 | [cards/bando1995-large-n-note.md](cards/bando1995-large-n-note.md) |
| bando1995-velocity-function | model_theory | confirmed | 簡單函數會倒車撞車，改用tanh(Δx−2)+tanh2 | [cards/bando1995-velocity-function.md](cards/bando1995-velocity-function.md) |
| bando1995-spontaneous-jam | model_theory | confirmed | 模擬：一台車偏0.1，就長出5團往後移動的塞車 | [cards/bando1995-spontaneous-jam.md](cards/bando1995-spontaneous-jam.md) |
| bando1995-cluster-values | model_theory | confirmed | 塞住後分成幾乎停住和接近全速兩種 | [cards/bando1995-cluster-values.md](cards/bando1995-cluster-values.md) |
| bando1995-stable-regions | model_theory | confirmed | 在這個模型和參數下：很稀疏或很密集時穩定，中間密度不穩定 | [cards/bando1995-stable-regions.md](cards/bando1995-stable-regions.md) |
| bando1995-capacity | model_theory | confirmed | 這組模擬裡有沒有塞車，運輸量都約0.48 | [cards/bando1995-capacity.md](cards/bando1995-capacity.md) |
| bando1995-no-delay | model_theory | confirmed | 模型刻意不加反應延遲 | [cards/bando1995-no-delay.md](cards/bando1995-no-delay.md) |
| ours-finite-n-threshold | our_derivation | confirmed | 22台車的分界是V'(b)(1+cos(2π/N))，不是剛好a/2 | [cards/ours-finite-n-threshold.md](cards/ours-finite-n-threshold.md) |
| ours-finite-n-simulation | our_simulation | confirmed | 模擬量到的22台分界跟推導相符 | [cards/ours-finite-n-simulation.md](cards/ours-finite-n-simulation.md) |
| sugiyama2008-setup | experiment | confirmed | 環道實驗：230公尺、22台車、約30 km/h起步 | [cards/sugiyama2008-setup.md](cards/sugiyama2008-setup.md) |
| sugiyama2008-jam-emerges | experiment | confirmed | 均勻車流自己變成走走停停 | [cards/sugiyama2008-jam-emerges.md](cards/sugiyama2008-jam-emerges.md) |
| sugiyama2008-backward-wave | experiment | confirmed | 塞車團以約20 km/h往後傳，車子進進出出 | [cards/sugiyama2008-backward-wave.md](cards/sugiyama2008-backward-wave.md) |
| sugiyama2008-highway-comparison | experiment | confirmed | 作者說這個速度跟高速公路上的塞車波差不多 | [cards/sugiyama2008-highway-comparison.md](cards/sugiyama2008-highway-comparison.md) |
| sugiyama2008-23-vehicles | experiment | confirmed | 23台車也塞，速度一樣 | [cards/sugiyama2008-23-vehicles.md](cards/sugiyama2008-23-vehicles.md) |
| sugiyama2008-mechanism | model_theory | confirmed | 作者的解釋：超過臨界密度，小波動就會長大 | [cards/sugiyama2008-mechanism.md](cards/sugiyama2008-mechanism.md) |
| sugiyama2008-fundamental-diagram | experiment | confirmed | 高速公路基本圖，臨界密度約每公里25台 | [cards/sugiyama2008-fundamental-diagram.md](cards/sugiyama2008-fundamental-diagram.md) |
