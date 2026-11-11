---
id: ours-finite-n-threshold
type: our_derivation
source: wiki/derivations/finite-n-threshold.md
locator: 「從Bando 1995推」第1～6步、「跟Orosz 2010對照」
conditions: bando1995的模型；環狀道路N台車；只看很小的擾動
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-large-n-note, ours-finite-n-simulation, orosz2010-ring-stability
---

## 主張

車數有限時，非零的第k個波只有在a < 2V'(b)cos²(πk/N)時才會變大（k=0是整體平移，不算；k和N−k是一對共軛，分界相同；N是偶數時k=N/2要直接用式(10)，它在a>0、V'(b)>0時不會失穩）。a往下調時最先變不穩定的是k=1這一對，所以N台車的實際分界是a = 2V'(b)cos²(π/N) = V'(b)(1+cos(2π/N))。22台車、車距2時是1.9595，不是a/2條件給的2；車距b固定、車數越多（環長跟著變長），越接近2V'(b)。

## 原文依據

這是我們推的，不是論文寫的，完整推導在`wiki/derivations/finite-n-threshold.md`。推法：bando1995式(11)的臨界曲線是f=a/(2cos²(α/2))，式(9)的α_k=2πk/N只能取這幾個值，把α_k代進去，第k個波不穩定的條件是f>a/(2cos²(πk/N))；k=1時右邊最小。f=V'(b)。

另外拿Orosz 2010附錄A對照：取W=0、沒有延遲、不計車長，代入F=aV'、G=0、H=a。直接代進式(A2)得到的特徵方程式跟Bando式(10)相同；代進(A6)得到同一個分界。Orosz也寫明沒有延遲時最先不穩定的是k=1。G=0是Orosz附錄所討論參數範圍（F、G、H>0）的邊界。

## 限制

- 我們自己推的。Orosz 2010的公式是一般跟車模型的，把它對應到Bando模型（W=0、沒有延遲、不計車長）的那一步是我們做的，Orosz沒有直接算Bando模型22台的分界。
- 只適用沒有延遲的模型；Orosz第4467頁說延遲夠大時，可能改成短的波先失去穩定。
- 只對很小的擾動成立。
- 差別只有約2%，對一般讀者不重要，放在進階展開區。
