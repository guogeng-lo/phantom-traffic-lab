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
