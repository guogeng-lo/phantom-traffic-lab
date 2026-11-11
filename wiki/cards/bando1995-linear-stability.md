---
id: bando1995-linear-stability
type: model_theory
source: bando1995
locator: 第1036～1037頁式(5)～(12)、圖1
conditions: 跟bando1995-ovm-equation相同；只看均勻車流附近很小的擾動（線性化）
units: 無因次
status: confirmed
related: bando1995-ovm-equation, ours-finite-n-threshold
---

## 主張

線性穩定性分析是判斷一點小變化會慢慢消失、還是越來越嚴重的方法。在均勻車流上加很小的擾動，把擾動拆成一個一個的波（第k個波的α_k=2πk/N）來看會不會變大。作者得到的總結（式(12)）是：速度函數在均勻車距的斜率V'(b)小於a/2時穩定，大於a/2時不穩定；在這個跟車方程式裡，換成別的速度函數V也適用。這個a/2是長波極限（車數很多）的分界；車數有限的環道，要依式(9)(11)逐一檢查那幾個非零的波，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。

## 原文依據

第1036頁式(5)～(10)把擾動線性化，用exp{iα_k n+zt}展開，得到z的二次方程式(10)；z的實部u>0代表那個波會變大。第1037頁式(11)是圖1裡分開穩定和不穩定的臨界曲線f=a/(2cos²(α/2))，其中f=V'(b)（式(7)）。作者整理成三種情況：f<a/2穩定、f=a/2臨界、f>a/2不穩定，總結成式(12) V'(b)<a/2。

> Note that the above criteria is valid in models with any legal velocity function V.

## 限制

- 只對很小的擾動成立，擾動變大之後要用模擬看（第1037頁）。
- 式(12)的a/2是把所有α都考慮進去的條件；車數有限時α只有幾個固定的值，實際分界會比a/2稍微不同，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。這是我們從式(9)(11)推出來的，不是論文直接寫的。

## 教學說法

駕駛對車距越敏感（只要距離一變，速度就跟著大幅改變），而調整得又不夠快，前車的一點點減速就會一台傳一台、越傳越大。
