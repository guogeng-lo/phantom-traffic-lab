---
id: ours-finite-n-threshold
type: our_derivation
source: audition/ovm.py
locator: critical_a函式，根據bando1995第1036～1037頁式(9)(11)
conditions: bando1995的模型；環狀道路N台車；只看很小的擾動
units: 無因次
status: confirmed
related: bando1995-linear-stability, bando1995-large-n-note, ours-finite-n-simulation
---

## 主張

車數有限時，第k個波只有在a < 2V'(b)cos²(πk/N)時才會變大；a往下調時最先變不穩定的是k=1，所以N台車的實際分界是a = 2V'(b)cos²(π/N) = V'(b)(1+cos(2π/N))。22台車、車距2時是1.9595，不是a/2條件給的2；車數越多越接近2。

## 原文依據

這是我們推的，不是論文寫的。推法：bando1995式(11)的臨界曲線是f=a/(2cos²(α/2))，式(9)的α_k=2πk/N只能取這幾個值，把α_k代進去，第k個波不穩定的條件是f>a/(2cos²(πk/N))；k=1時右邊最小。f=V'(b)。

## 限制

- 我們自己推的，還沒有被另一篇文獻直接確認。Orosz 2010附錄A有一般跟車模型在N台車環道上的分界公式，初步代入結果相同，但Orosz 2010還沒ingest，正式對照等ingest之後。
- 只對很小的擾動成立。
- 差別只有約2%，對一般讀者不重要，放在進階展開區。
