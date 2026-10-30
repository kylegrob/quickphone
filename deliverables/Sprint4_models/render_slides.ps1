# Renders every slide-sized QuickPhone model (1920x1080) to a 2x PNG and a vector PDF, plus the full
# Level 0 poster (sized by the page) for documents. Output: slides\logical and slides\physical.
# -Check renders nothing: it lists, for every DFD, any two flows whose lines run along the same stretch.
param([string[]]$Only, [switch]$NoPdf, [switch]$Check)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir = $PSScriptRoot
function Url($file, $q) { "file:///" + (Join-Path $dir $file).Replace('\','/') + "?$q" }
$items = [ordered]@{}
foreach ($v in @('log','phys')) {
  $folder = if ($v -eq 'log') { 'logical' } else { 'physical' }
  $p = if ($v -eq 'log') { 'Logical' } else { 'Physical' }
  $items["context_$v"] = @($folder, "01_DFD_Context_$p", 'dfd_slides.html', "v=$v&d=context", 1920, 1080)
  $items["level0_$v"]  = @($folder, "02_DFD_Level0_Complete_$p", 'dfd_slides.html', "v=$v&d=level0", 0, 0)
  $items["l0a_$v"] = @($folder, "03_DFD_Level0_Part1_Booking_CheckIn_$p", 'dfd_slides.html', "v=$v&d=l0a", 1920, 1080)
  $items["l0b_$v"] = @($folder, "04_DFD_Level0_Part2_Bench_$p", 'dfd_slides.html', "v=$v&d=l0b", 1920, 1080)
  $items["l0c_$v"] = @($folder, "05_DFD_Level0_Part3_Notice_Release_$p", 'dfd_slides.html', "v=$v&d=l0c", 1920, 1080)
  $items["l0d_$v"] = @($folder, "06_DFD_Level0_Part4_BackOffice_$p", 'dfd_slides.html', "v=$v&d=l0d", 1920, 1080)
  $n = 7
  foreach ($d in @(@('l1_1','1.0_ScheduleAppointment'),@('l1_2','2.0_RegisterRepairJob'),@('l1_3','3.0_RecordDiagnosis'),@('l1_4','4.0_RecordRepairWork'),
                   @('l1_5','5.0_SendCompletionNotice'),@('l1_6','6.0_RecordDeviceRelease'),@('l1_7','7.0_ProcessPurchaseOrders'),@('l1_9','9.0_MaintainShopRecords'))) {
    $items["$($d[0])_$v"] = @($folder, ('{0:00}_DFD_Level1_{1}_{2}' -f $n, $d[1], $p), 'dfd_slides.html', "v=$v&d=$($d[0])", 1920, 1080); $n++
  }
  $items["erd_ov_$v"] = @($folder, "15_ERD_Overview_$p", 'erd_slides.html', "v=$v&s=overview", 1920, 1080)
  $items["erd_full_$v"] = @($folder, "ERD_Full_$p", 'erd_slides.html', "v=$v&s=full", 3040, 1860)
  foreach ($k in 1..3) { $items["erd_${k}_$v"] = @($folder, "1$($k+5)_ERD_Detail$k`_$p", 'erd_slides.html', "v=$v&s=$k", 1920, 1080) }
}
$items['align'] = @('.', '19_DFD_ERD_Alignment', 'dfd_slides.html', 'v=log&d=align', 1920, 1080)
foreach ($k in $items.Keys) {
  if ($Only -and $k -notin $Only) { continue }
  $folder, $name, $src, $q, $w, $h = $items[$k]
  $outDir = Join-Path (Join-Path $dir 'slides') $folder
  New-Item -ItemType Directory -Force $outDir | Out-Null
  $out = Join-Path $outDir $name
  $u = Url $src $q
  if ($Check) {
    if ($src -ne 'dfd_slides.html' -or $k -eq 'align') { continue }
    $dom = & $chrome --headless=new --disable-gpu --dump-dom "$u&check=1" 2>$null | Out-String
    $m = [regex]::Match($dom, '<pre id="chk">(.*?)</pre>', 'Singleline')
    $hits = @(if ($m.Success) { [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value) | ConvertFrom-Json -NoEnumerate | ForEach-Object { $_ } })
    if (-not $m.Success) { "$k : no result" } elseif ($hits.Count -eq 0) { "$k : ok" }
    else { "$k : $($hits.Count) overlap(s)"; $hits | ForEach-Object { "    '$($_[0])' / '$($_[1])' at $($_[2]) ($($_[3]) px)" } }
    continue
  }
  if ($w -eq 0) { # size taken from the page itself (the routed Level 0 poster sizes itself)
    $svgTag = (& $chrome --headless=new --disable-gpu --dump-dom $u 2>$null | Select-String '<svg id="s"[^>]*>').Matches[0].Value
    $w = [int]([regex]::Match($svgTag,'width="(\d+)"').Groups[1].Value); $h = [int]([regex]::Match($svgTag,'height="(\d+)"').Groups[1].Value)
  }
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 "--window-size=$w,$h" "--screenshot=$out.png" $u 2>$null | Out-Null
  if (-not $NoPdf) { & $chrome --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=$out.pdf" $u 2>$null | Out-Null }
  "$k -> slides\$folder\$name"
}
