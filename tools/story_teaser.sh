#!/usr/bin/env bash
# Usage: tools/story_teaser.sh input.mp4 output.mp4
# 7-second Instagram Story teaser: the video's hook + the "NEW REEL ON MY PROFILE" banner.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
ffmpeg -y -v error -t 7 -i "$1" -loop 1 -t 7 -i "$here/story_banner.png" -filter_complex \
"[0:v]scale=1080:1920,setsar=1[v];[1:v]format=rgba,fade=t=in:st=0.8:d=0.35:alpha=1[b];[v][b]overlay=0:0,fade=t=out:st=6.6:d=0.4,format=yuv420p[o];[0:a]afade=t=out:st=6.4:d=0.6[a]" \
-map "[o]" -map "[a]" -c:v libx264 -preset veryfast -crf 20 -r 30 -c:a aac -b:a 128k -movflags +faststart "$2"
