---
id: sugiyama2008
kind: paper
authors: Yuki Sugiyama, Minoru Fukui, Macoto Kikuchi, Katsuya Hasebe, Akihiro Nakayama, Katsuhiro Nishinari, Shin-ichi Tadaki, Satoshi Yukawa
year: 2008
title: Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam
venue: New Journal of Physics 10, 033001 (7pp)
doi: 10.1088/1367-2630/10/3/033001
url: https://doi.org/10.1088/1367-2630/10/3/033001
read_status: 全文已讀
read_scope: 期刊第1～7頁全文、圖1～5和圖說、腳註11～15、參考文獻；兩段補充影片沒有看
independent: 是
---

## 這篇在做什麼

在沒有紅綠燈、沒有障礙物的環形道路上放22台車，讓駕駛照平常的方式跟車。研究人員想確認：即使沒有路口、事故或道路瓶頸，車子彼此的跟車行為，是否仍可能讓塞車自己形成。實驗確實觀察到了這個現象。這是一篇很短的實驗報告（7頁），沒有寫出模型方程式，模型的部分引用他們自己1995年的論文（參考文獻[4]、[12]）。

頁碼用期刊本身印的頁碼（第1～7頁）。大阪大學典藏庫的PDF前面有兩張前置頁（典藏庫封面和出版商的頁面），PDF頁碼比期刊頁碼多2。

## 研究條件

- 平坦地面、單一車道的環形道路，周長230公尺，22台車，中間架一台360度攝影機量測（第4頁、圖2）。
- 車數是先用模型估過、刻意讓密度落在「均勻車流會不穩定」的範圍（第4頁）。
- 開始前讓車子以約30 km/h等速、間距大致均勻地繞；之後駕駛只被要求安全跟前車、盡量維持巡航速度（第4頁）。
- 作者自己說這個速度以平均車距來看偏快，是為了滿足不穩定條件才這樣設定（第4頁）。
- 也做過不同車數的實驗，但文中只提到23台的結果（第5頁）。
- 沒有寫駕駛是誰、做了幾次、每次的差異，也沒有統計分析。

## 主要結果

- 實驗設定：[cards/sugiyama2008-setup.md](../cards/sugiyama2008-setup.md)
- 均勻車流自己變成塞車：[cards/sugiyama2008-jam-emerges.md](../cards/sugiyama2008-jam-emerges.md)
- 塞車團往後傳、速度約20 km/h：[cards/sugiyama2008-backward-wave.md](../cards/sugiyama2008-backward-wave.md)
- 作者拿高速公路資料比較：[cards/sugiyama2008-highway-comparison.md](../cards/sugiyama2008-highway-comparison.md)
- 23台車也塞：[cards/sugiyama2008-23-vehicles.md](../cards/sugiyama2008-23-vehicles.md)
- 作者對機制的解釋：[cards/sugiyama2008-mechanism.md](../cards/sugiyama2008-mechanism.md)
- 高速公路的基本圖（用圖表示車流密度和通過車輛數之間的關係）：[cards/sugiyama2008-fundamental-diagram.md](../cards/sugiyama2008-fundamental-diagram.md)

## 限制

- 只有一個場地、一種車數設定的詳細結果，沒有重複次數和統計。作者在腳註15說更詳細的結果和不穩定的密度範圍會在之後的論文發表，但沒有指名是哪一篇。Tadaki 2013第3頁說自己是先前環道實驗的延伸，不過無法確認腳註當時指的就是它。
- 數字的性質要分開看：230公尺、22台是實驗設定（第4頁）；約30 km/h是開始前調好的巡航速度，也是要求駕駛的速度（第4頁）；團外車速約40 km/h、塞車團約20 km/h往後是觀察到的約略值（第5頁，原文roughly），第6頁圖4的車輛軌跡上也標了約20 km/h。
- 「瓶頸只是觸發、不是塞車的根本原因」是作者依自己的模型做的解釋，實驗本身支持的是「沒有瓶頸也可能塞車」。文中也引用了Kerner的研究（參考文獻[3]、[8]），我們只能確認有引用，Kerner的具體立場還沒讀，見[disputes.md](../disputes.md)。
- 文中沒有寫出模型方程式和穩定條件，要另外從模型的原始論文確認。

## ingest紀錄

- [runs/2026-11-11-n1-sugiyama2008-r1.md](../../runs/2026-11-11-n1-sugiyama2008-r1.md)
