# Renders every QuickPhone Sprint 3 model diagram with headless Chrome:
# a 2x-resolution PNG (for documents) and a vector PDF (zoom to any size) per diagram.
param([string[]]$Only, [switch]$NoPdf)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir = $PSScriptRoot
function Url($file, $q) { "file:///" + (Join-Path $dir $file).Replace('\','/') + "?$q" }
# key = @(output folder, file name, width, height, source file, query)
$set = [ordered]@{
  erd_log  = @('logical',  'QuickPhone_Logical_ERD',  4240, 1980, 'erd_source.html', 'v=log')
  erd_phys = @('physical', 'QuickPhone_Physical_ERD', 4240, 1980, 'erd_source.html', 'v=phys')
  erd_log_a = @('logical', 'QuickPhone_Logical_ERD_detail_1', 1350, 1330, 'erd_source.html', 'v=log&crop=0,1350')
  erd_log_b = @('logical', 'QuickPhone_Logical_ERD_detail_2', 1400, 1330, 'erd_source.html', 'v=log&crop=1380,2780')
  erd_log_c = @('logical', 'QuickPhone_Logical_ERD_detail_3', 1440, 1330, 'erd_source.html', 'v=log&crop=2780,4220')
}
if (Test-Path (Join-Path $dir 'dfd_list.ps1')) { . (Join-Path $dir 'dfd_list.ps1') }
foreach ($k in $set.Keys) {
  if ($Only -and $k -notin $Only) { continue }
  $folder, $name, $w, $h, $src, $q = $set[$k]
  $out = Join-Path (Join-Path $dir $folder) $name
  $u = Url $src $q
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 "--window-size=$w,$h" "--screenshot=$out.png" $u 2>$null | Out-Null
  if (-not $NoPdf) {
    & $chrome --headless=new --disable-gpu --no-pdf-header-footer "--print-to-pdf=$out.pdf" $u 2>$null | Out-Null
  }
  "$k -> $folder\$name"
}
