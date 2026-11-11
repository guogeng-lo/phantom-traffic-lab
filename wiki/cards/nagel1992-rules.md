---
id: nagel1992-rules
type: model_theory
source: nagel1992
locator: 第2222頁第2節
conditions: 單車道，道路切成格子，每格最多一台車；所有車同時更新
units: 格、時間步
status: confirmed
related: nagel1992-randomization
---

## 主張

每一步，每台車依序做4件事：1. 還沒到最高速、前面空間夠，就加速1；2. 前車太近，就減到不會撞上的速度；3. 以機率p隨機減速1；4. 照速度往前走。

## 原文依據

第2222頁第2節列出四個步驟：Acceleration（速度低於v_max且前車距離大於v+1時加1）、Slowing down（看到前車在i+j格、j≤v時，速度降到j−1）、Randomization（以機率p，速度大於0的車減1）、Car motion（往前走v格）。所有車同時進行。

## 限制

- 速度和位置都是整數，跟Bando的連續模型不同。
- 每台車只看前車。

## 教學說法

把道路想成一格一格的棋盤，每台車每一秒都照四條很簡單的規則走，其中一條是「偶爾會無緣無故慢一下」。
