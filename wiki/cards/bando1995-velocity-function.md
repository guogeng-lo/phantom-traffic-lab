---
id: bando1995-velocity-function
type: model_theory
source: bando1995
locator: 第1037頁式(16)、第1038頁式(24)和圖3～4、第1042頁圖11
conditions: 無因次；a=1
units: 無因次
status: confirmed
related: bando1995-ovm-equation, bando1995-spontaneous-jam
---

## 主張

作者先試了最簡單的速度函數V=tanh(Δx)，結果在不穩定時會有車往後倒退，等於撞車。所以改用V(Δx)=tanh(Δx−2)+tanh2：車距是0時速度是0，車子只會慢慢加減速、不會超過前車。

## 原文依據

第1037頁式(16)是簡單模型V=tanh(Δx)。第1037～1038頁說不穩定時會看到車往後移動（圖3、圖4），單車道上就代表兩台車撞在一起。第1038頁式(24)改用V(Δx)=tanh(Δx−2)+tanh2，並說這樣駕駛會慢慢加減速，不會超過前車。

> a driver controls the vehicle by gradually accelerating or braking in such a way that it never passes the preceding vehicle

## 限制

- tanh(Δx−2)+tanh2只是一個形狀合理的函數，論文沒有說它是從真實資料擬合出來的。
- 選題階段的模擬（`audition/ovm.py`）用的就是這個函數，現在有出處了。
