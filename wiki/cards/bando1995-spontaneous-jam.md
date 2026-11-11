---
id: bando1995-spontaneous-jam
type: model_theory
source: bando1995
locator: 第1037頁式(17)～(19)、第1038頁式(24)後段、第1039頁圖5、第1040頁圖6
conditions: 模擬，不是實驗；N=100、L=200（車距2）、a=1、V=tanh(Δx−2)+tanh2；初始位置幾乎等距，第1台車往前偏0.1，所有車的初速都是0（式(19)）
units: 無因次
status: confirmed
related: bando1995-velocity-function, bando1995-cluster-values, sugiyama2008-backward-wave
---

## 主張

在模擬裡，100台車的初始位置幾乎等距，只有第1台往前移0.1，所有車從靜止（初速0）開始，之後車流自己分成幾段幾乎停住的塞車和幾段快速前進的車，最後形成5團塞車；這些塞車團都以相同的速度慢慢往後移動。

## 原文依據

第1038頁說模擬用N=100、L=200，加上跟簡單模型一樣的初始條件（第1037頁式(17)～(19)：第1台車往前偏0.1，其他車在等距位置，所有車初速為0）。第1039頁圖5是t=100、300、1000時所有車的速度：沒有負速度，速度逐漸分成接近0和接近最大速度兩種。第1039～1040頁圖6是所有車位置隨時間的圖，看得到5團塞車從很小的擾動長出來。

> From this figure, we find that five clusters of congestion are formed even from a very tiny disturbance existing in the almost uniform vehicle distribution.

第1039頁最後一句接到第1040頁說，圖6也顯示所有塞車團都以相同的速度慢慢往後移動（這句跨頁，所以不直接引用）。

## 限制

- 這是電腦模擬的結果，作者是用模擬來示範，不是真實道路。
- 車數100、車距2，跟2008年實驗的條件不同。
- 初速是0，不是已經在等速巡航；選題階段的模擬（`audition/`）是從等速巡航開始，兩者的初始條件不同。

## 教學說法

在電腦裡只讓一台車稍微往前一點點，什麼都不做，過一陣子整圈就塞成好幾段。
