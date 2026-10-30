#!/bin/bash
# Renders Sprint 4 DFD views to slides/{logical,physical}: 2x PNG (cropped to the page size) + vector PDF.
# usage: ./render_dfd.sh [name ...]   names: context level0 l0a l0b l0c l0d l1_1 l1_2 l1_3 l1_4 l1_5 l1_6 l1_7 l1_9 align (default: all)
# Headless Chrome's screenshot viewport is shorter than --window-size, so each PNG is taken in a taller window and cropped.
D="$(pwd -W | tr '\' '/')"
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
declare -A NM=( [context]=01_DFD_Context [level0]=02_DFD_Level0_Complete [l0a]=03_DFD_Level0_Part1_Booking_CheckIn [l0b]=04_DFD_Level0_Part2_Bench
 [l0c]=05_DFD_Level0_Part3_Notice_Release [l0d]=06_DFD_Level0_Part4_BackOffice [l1_1]=07_DFD_Level1_1.0_ScheduleAppointment
 [l1_2]=08_DFD_Level1_2.0_RegisterRepairJob [l1_3]=09_DFD_Level1_3.0_RecordDiagnosis [l1_4]=10_DFD_Level1_4.0_RecordRepairWork
 [l1_5]=11_DFD_Level1_5.0_SendCompletionNotice [l1_6]=12_DFD_Level1_6.0_RecordDeviceRelease [l1_7]=13_DFD_Level1_7.0_ProcessPurchaseOrders
 [l1_9]=14_DFD_Level1_9.0_MaintainShopRecords [align]=19_DFD_ERD_Alignment )
ALL="context level0 l0a l0b l0c l0d l1_1 l1_2 l1_3 l1_4 l1_5 l1_6 l1_7 l1_9 align"
for k in ${@:-$ALL}; do
  for v in log phys; do
    [ $k = align ] && [ $v = phys ] && continue
    if [ $v = log ]; then f=logical; p=Logical; else f=physical; p=Physical; fi
    [ $k = align ] && { f=.; p=; }
    mkdir -p "slides/$f"; out="slides/$f/${NM[$k]}${p:+_$p}"
    u="file:///$D/dfd_slides.html?v=$v&d=$k"
    sz=$("$CH" --headless=new --disable-gpu --dump-dom "$u" 2>/dev/null | grep -o '<svg id="s"[^>]*>' | head -1)
    w=$(echo "$sz" | grep -o ' width="[0-9]*"' | grep -o '[0-9]*'); h=$(echo "$sz" | grep -o ' height="[0-9]*"' | grep -o '[0-9]*')
    "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 "--window-size=$w,$((h+90))" "--screenshot=$D/$out.png" "$u" >/dev/null 2>&1
    python -c "
from PIL import Image
im=Image.open('$out.png'); im.crop((0,0,$w*2,$h*2)).save('$out.png')"
    "$CH" --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=$D/$out.pdf" "$u" >/dev/null 2>&1
    echo "$k $v ${w}x$h -> $out"
  done
done
