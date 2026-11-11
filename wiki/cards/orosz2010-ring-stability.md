---
id: orosz2010-ring-stability
type: model_theory
source: orosz2010
locator: 第4467頁第3段、第4475～4476頁附錄A式(A1)～(A8)
conditions: 一般的跟車模型，沒有反應延遲；環上N台車；F、G、H大於0
units: 保留物理量綱（F、G、H是有單位的係數）
status: confirmed
related: orosz2010-stability-approaches, ours-finite-n-threshold
---

## 主張

（這是綜述附錄裡的數學推導，所以類型是model_theory。）在沒有反應延遲的跟車模型裡，環上N台車時，非零的波各有穩定分界，k和N−k是一對共軛、共用同一條分界；N是偶數時k=N/2沒有有限的分界。N≥3時，越過分界時最先失去穩定的是k=1（和它的共軛N−1，最長的波）。固定均勻車距、讓N趨近無限多時，最先失穩的k=1的波數2π/N趨近0（長波），整體的穩定條件變成(A8)。

## 原文依據

第4475頁附錄A把式(5.1)在沒有延遲時寫成(A1)，用環上N台車的解得到(A3)，開N次方後回到(A2)，波數只能是(A4)的2kπ/N。第4476頁(A6)是第k個波穩定性改變的條件，作者說從F小往大越過分界時系統「更不穩定」，因此最先失去穩定的是k=1；N趨近無限大時條件變成(A8)。第4467頁也說，沒有延遲時穩定性會先在低頻、長波（k=1）失去。

> Consequently, the stability loss occurs for the lowest wavenumber

## 限制

- 這是一般模型的公式，用F、G、H表示。代入Bando的模型（W=0、車長0）得到22台車分界的那一步是我們做的，見[ours-finite-n-threshold](ours-finite-n-threshold.md)。
- 只適用沒有延遲的情況，見[orosz2010-delays](orosz2010-delays.md)。
- (A6)含tan²(kπ/N)，k=N/2時發散，所以那個波沒有有限的Hopf分界；作者也寫只有k≤N/2的分界出現在F、G、H>0的範圍。
- 原文沒有寫車數下限。N=2時唯一非零的波就是k=N/2=1，沒有有限的分界，所以「k=1最先失穩」要N≥3才有意義；這個條件是我們從(A6)看出來的。
