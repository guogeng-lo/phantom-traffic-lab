#!/bin/bash
# 診斷的固定執行順序（次數事先決定，不因結果加測）。輸出存在 <out>。
set -u
cd "$(dirname "$0")"
OUT=$1; mkdir -p $OUT
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
envsnap() { echo "== 環境：$1"; nproc; cat /sys/fs/cgroup/cpu.max 2>/dev/null || echo "沒有cpu.max"; cat /proc/loadavg; free -m | head -2; ps -eo pcpu,rss,comm --sort=-pcpu | head -6; }
envsnap "開始" > $OUT/env-0.txt
log "B0：新開環境之後的第一次Lighthouse（1次）"; node lh.js B0 1 $OUT
log "B1：同一個環境接著跑（4次）"; node lh.js B1 4 $OUT
log "B2：清掉系統檔案快取後的第一次（2組，各1次）"
for k in 1 2; do sync; echo 3 > /proc/sys/vm/drop_caches; node lh.js B2c$k 1 $OUT; done
log "B3：預熱過、一直開著的瀏覽器（5次，用--port接上）"
node -e '
const {serve}=require("../../tests/site_server");
(async()=>{const {srv,url}=await serve();require("fs").writeFileSync(process.argv[1],url);await new Promise(()=>{});})();' $OUT/warm-url.txt &
SRV=$!; sleep 1
node warm_browser.js "$(cat $OUT/warm-url.txt)" > $OUT/warm.txt 2>&1 &
WB=$!; sleep 9
node lh.js B3 5 $OUT --port=9222
kill $WB $SRV 2>/dev/null; sleep 2
log "B4：背景有一個程式佔滿1顆CPU（3次）"
node -e 'for(;;){}' & BUSY=$!; sleep 2
node lh.js B4 3 $OUT
kill $BUSY; sleep 2
envsnap "B結束" > $OUT/env-1.txt
log "休息120秒，讓系統負載降下來"; sleep 120
envsnap "A1開始前" > $OUT/env-2.txt
log "A1：動畫CPU，獨立執行（p1、p2、p5各5次，冷＋熱）"; node cpu.js A1 $OUT/A1.json
log "Lighthouse 5次（跟正式效能測試一樣），接著馬上量A2"; node lh.js A2pre 5 $OUT
log "A2：Lighthouse之後馬上量（p1、p2、p5各2次，冷）"; node cpu.js A2 $OUT/A2.json
log "A3：Performance trace（p1、p2、p5各1次）"; node trace.js $OUT
envsnap "結束" > $OUT/env-3.txt
log "完成"
