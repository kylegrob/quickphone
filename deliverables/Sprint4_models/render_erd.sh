#!/bin/bash
# Renders the ERD slides (2x PNG + vector PDF) for both views into slides/logical and slides/physical.
D="$(pwd -W | tr '\' '/')"
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
run() { # folder name query w h
  mkdir -p "slides/$1"
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 "--window-size=$4,$5" "--screenshot=$D/slides/$1/$2.png" "file:///$D/erd_slides.html?$3" >/dev/null 2>&1
  "$CH" --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=$D/slides/$1/$2.pdf" "file:///$D/erd_slides.html?$3" >/dev/null 2>&1
  echo "$1/$2"
}
for v in log phys; do
  if [ $v = log ]; then f=logical; p=Logical; else f=physical; p=Physical; fi
  run $f "15_ERD_Overview_$p" "v=$v&s=overview" 1920 1080
  run $f "ERD_Full_$p" "v=$v&s=full" 3040 2210
  for k in 1 2 3; do run $f "1$((k+5))_ERD_Detail${k}_$p" "v=$v&s=$k" 1920 1080; done
done
