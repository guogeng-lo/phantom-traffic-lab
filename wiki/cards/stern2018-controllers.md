---
id: stern2018-controllers
type: experiment
source: stern2018
locator: 第5頁第3節開頭、第6～8頁第3.1～3.2節
conditions: 控制器只用那台車自己量到的速度、跟前車的距離，以及（實驗A、B）外部給的目標速度
units: s
status: confirmed
related: stern2018-results
---

## 主張

兩種控制器的共同想法是：那台車照著車流的平均速度開，而不是跟著前車忽快忽慢。前車加速時讓空隙變大、前車減速時把空隙吃掉，同樣的時間走同樣的距離，但加速和煞車少很多；距離太近時一定以安全為先。

## 原文依據

第5頁說，平均速度在波來之前比前車慢、在波裡面比前車快，照平均速度開可以用較少的加減速走同樣的距離，另外要有防止距離太近或太遠的邏輯。第6～7頁的FollowerStopper在安全時用目標速度U，距離太近時降低速度；第7～8頁的PI控制器用自己過去約38秒（大約繞一圈）的平均速度當目標，距離太近時跟著前車速度、距離太大時加速追上。

> By simply driving at the average speed, a vehicle covers the same distance in the same amount of time, but with less acceleration and breaking.

（原文braking拼成breaking，照原文引用。）

## 限制

- 實驗A的目標速度是外部觀察者給的，不是車子自己算的。
- 簡報如果做「平滑車」示範，會是我們自己簡化的規則，不是這兩種控制器，要在頁面上寫清楚。
