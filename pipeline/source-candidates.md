# 文獻候選和全文取得方式（2026-11-11查）

這份是ingest前的準備，**不是**Wiki內容。書目資料是從出版社、典藏庫或arXiv的頁面查的，查不到的寫「待查證」；內容一律等拿到全文、照`AGENTS.md`第5節ingest之後才算數。

## 候選

| 候選 | 書目（查到的） | 全文 | 備註 |
|---|---|---|---|
| Bando等1995 | Dynamical model of traffic congestion and numerical simulation，Physical Review E，DOI 10.1103/PhysRevE.51.1035。Sugiyama 2008的參考文獻[4]寫Phys. Rev. E 51 1035，作者Bando、Hasebe、Nakayama、Shibata、Sugiyama（從別篇的引用看到，不是讀原文確認） | APS付費，大同沒有訂。11/11使用者後來提供了掃描版PDF，已經ingest | 摘要把V叫做「legal velocity function」，後來的文獻多叫optimal velocity，術語表要記 |
| Bando等1995（備案） | Phenomenological Study of Dynamical Model of Traffic Flow，J. Phys. I France 5(11):1389–1399，DOI 10.1051/jp1:1995206 | 出版社頁面要付費；HAL上有沒有免費全文待查證 | 同一群作者、同一個模型。PRE那篇拿不到時再考慮 |
| Sugiyama等2008 | Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam，New Journal of Physics 10, 033001，DOI 10.1088/1367-2630/10/3/033001。作者8位：Sugiyama、Fukui、Kikuchi、Hasebe、Nakayama、Nishinari、Tadaki、Yukawa | 免費：大阪大學典藏庫PDF | 授權說法不一致：典藏庫寫CC BY 4.0，PDF首頁寫© IOP Publishing和DPG。我們只放連結，不影響 |
| Nagel、Schreckenberg 1992 | A cellular automaton model for freeway traffic，J. Phys. I France 2(12):2221–2229，DOI 10.1051/jp1:1992277 | 出版社頁面要付費；HAL（jpa-00246697）有全文，但我這邊被擋，要用瀏覽器下載 | 隨機模型，跟Bando的機制不同，照AGENTS第6節第1類處理 |
| Stern等2018 | Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments，Transportation Research Part C，DOI 10.1016/j.trc.2018.02.005。作者14位。卷期和頁碼待查證 | 免費：arXiv 1705.01693（2017-05-04，只有v1） | arXiv是投稿前的版本，可能跟正式版不同，ingest時`read_scope`要寫清楚讀的是預印本 |
| Tadaki等2013 | Phase transition in traffic jam experiment on a circuit，New Journal of Physics 15, 103034，DOI 10.1088/1367-2630/15/10/103034。作者9位 | 免費：大阪大學典藏庫PDF | 314公尺的室內環道、10～40台車，有不同車數的實驗。授權說法也不一致（典藏庫CC BY-NC-SA 4.0，文章註腳CC BY 3.0） |
| Orosz、Wilson、Stépán 2010 | Traffic jams: dynamics and control，Phil. Trans. R. Soc. A 368:4455–4479，DOI 10.1098/rsta.2010.0205 | 免費：作者個人網站PDF | 綜述，也是主題特刊的導論。附錄A是「沒有延遲的跟車模型的穩定性」，可能可以拿來對照我們自己推的22台車分界，要讀過才知道 |

## 查過但先不用的

- Bando等1996，Delay of Vehicle Motion in Traffic Dynamics，arXiv patt-sol/9608002：講OV模型本身造成的延遲，不是之前討論提到的「1998年明確加入延遲」那篇。1998那篇還沒查到。
- Dissipation of traffic jams using a single autonomous vehicle on a ring road：HAL上有（hal-03354282），但頁面被擋，作者、期刊、年份待查證。平滑車是加分功能，先不追。

## 建議的讀法

1. 先讀Bando 1995（PRE）和Sugiyama 2008，給使用者確認（AGENTS第5節第7步）。
2. 第2批：NaSch 1992、Tadaki 2013。
3. 第3批：Stern 2018、Orosz 2010。

這樣是6篇，比5篇多一篇。原因是Orosz 2010可能讓第3頁的有限車數分界有文獻可以對照，不只有我們自己的推導。讀完發現用不到就不算。

## 連結

- Sugiyama 2008：https://ir.library.osaka-u.ac.jp/repo/ouka/all/93262/NewJPhys_10_033001.pdf
- Tadaki 2013：https://ir.library.osaka-u.ac.jp/repo/ouka/all/93261/NewJPhys_15_103034.pdf
- NaSch 1992（HAL）：https://hal.archives-ouvertes.fr/jpa-00246697
- Stern 2018（arXiv）：https://arxiv.org/pdf/1705.01693
- Orosz 2010：https://public.websites.umich.edu/~orosz/articles/PTRSA2published.pdf
- Bando 1995（APS）：https://link.aps.org/doi/10.1103/PhysRevE.51.1035
