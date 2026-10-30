#!/bin/bash
# usage: r1.sh "query" width height out.png [file]
D="$(pwd -W | tr '\' '/')"
F="${5:-erd_slides.html}"
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 "--window-size=$2,$3" "--screenshot=$4" "file:///$D/$F?$1" 2>/dev/null >/dev/null
echo "$4"
