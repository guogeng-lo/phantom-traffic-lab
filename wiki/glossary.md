# 術語對照

全專案統一用這裡的譯名。簡報第一次出現時寫「中文（英文）」，之後用中文或縮寫。

| 中文 | 英文 | 其他常見譯名 | 出處或說明 |
|---|---|---|---|
| 幽靈塞車 | Phantom Traffic Jam | 待查 | 暫定，ingest時查可靠的繁體中文用法再確認 |
| 自由流 | free flow | — | sugiyama2008第2～3頁；所有車用差不多的速度、保持安全距離前進 |
| 塞車團 | jam cluster | 阻塞團、壅塞團 | sugiyama2008第5頁；暫定譯名，待查繁體中文學術用法 |
| 走走停停波 | stop-and-go wave | 停走波 | sugiyama2008第4頁；暫定譯名，待查 |
| 時空圖 | time-space diagram | 時空軌跡圖 | sugiyama2008第6頁圖4畫的是每台車在環道上的軌跡（位置對時間）；簡報裡橫軸是位置、縱軸是時間、時間往下增加 |
| 瓶頸 | bottleneck | — | sugiyama2008第2頁；例如匝道、隧道、上坡 |
| 臨界密度 | critical density | — | sugiyama2008第2～3頁 |
| 基本圖 | fundamental diagram | 流量密度圖 | sugiyama2008第2頁；密度和流量的關係圖；暫定，待查台灣交通工程用法 |
| 車頭間距 | headway distance | 車距、車頭距 | sugiyama2008第4頁；這裡指距離，不是時間；暫定，待查 |
| 最佳速度模型 | Optimal Velocity Model, OVM | — | bando1995提出，但原文把V叫legal velocity function；OVM這個名稱是後來文獻用的（例如Orosz 2010、Tadaki 2013） |
| 最佳速度函數 | optimal velocity function | 合法速度函數（直譯legal velocity function） | bando1995第1036頁；只看前車距離的「想開的速度」 |
| 敏感度 | sensitivity | — | bando1995第1036頁的a；不是反應時間 |
| 均勻車流 | steady state flow, uniform flow | 穩態流 | bando1995第1036頁；所有車等距等速 |
| 線性穩定性分析 | linear stability analysis | — | bando1995第1036～1037頁 |
| 週期邊界條件 | periodic boundary condition | — | bando1995第1036頁；第N+1台就是第1台，等於環狀道路 |
| 細胞自動機 | cellular automaton | 元胞自動機 | nagel1992第2221頁；把空間和時間切成格子、照規則更新的模型；暫定，待查繁體中文常用譯名 |
| 同時更新 | parallel update | 平行更新 | nagel1992第2227頁；每一步所有車一起照規則移動，一般NaSch模型用這種 |
| 隨機逐車更新 | random sequential update | 隨機序列更新 | nagel1992第2227頁；每次隨機挑一台車更新；暫定譯名 |
| NaSch模型 | Nagel–Schreckenberg model | — | 指nagel1992提出的模型；這個簡稱是後來文獻的叫法 |
| 隨機減速 | randomization | 隨機化 | nagel1992第2222頁第3步；暫定譯名 |
| 介穩態 | metastable state | 亞穩態 | tadaki2013第10頁；同一個密度下兩種狀態都可能出現；台灣物理學常用「介穩態」，待確認 |
| 相變 | phase transition | 相轉變 | sugiyama2008第3、7頁、tadaki2013第11頁；兩篇都用相變描述自由流變成塞車流：Sugiyama說是非平衡系統的相變，Tadaki說是動態相變，並說轉變似乎是一階 |
| 反應延遲 | reaction time, delay | 反應時間 | orosz2010第4462頁；Bando 1995沒有加 |
| 跟車模型 | car-following model | — | orosz2010第4461頁；每台車看前車決定怎麼開的模型 |
| 自動駕駛車 | autonomous vehicle, AV | 自駕車 | stern2018；這篇的車只有速度自動控制，方向盤由人操作 |
| 平滑車 | — | — | 我們簡報裡自己取的名字，指「照平均速度穩定開的那台車」，不是論文用語 |
