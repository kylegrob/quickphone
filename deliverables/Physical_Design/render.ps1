# Renders each physical diagram to PNG with headless Chrome.
param([string[]]$Only)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir = $PSScriptRoot
$dfd = "file:///" + (Join-Path $dir 'physical_dfd_source.html').Replace('\','/')
$erd = "file:///" + (Join-Path $dir 'physical_erd_source.html').Replace('\','/')
$set = [ordered]@{
  context = @('QuickPhone_PDFD_0_Context', 2600, 1990, $dfd)
  level0  = @('QuickPhone_PDFD_1_Level0', 3550, 3050, $dfd)
  l1_1    = @('QuickPhone_PDFD_2_Level1_P1_CheckIn', 2400, 1930, $dfd)
  l1_2    = @('QuickPhone_PDFD_3_Level1_P2_Diagnose', 2400, 1930, $dfd)
  l1_3    = @('QuickPhone_PDFD_4_Level1_P3_Repair', 2650, 1790, $dfd)
  l1_4    = @('QuickPhone_PDFD_5_Level1_P4_Notify', 2700, 1930, $dfd)
  l1_5    = @('QuickPhone_PDFD_6_Level1_P5_Release', 2500, 1760, $dfd)
  l1_6    = @('QuickPhone_PDFD_7_Level1_P6_Replenish', 2500, 2110, $dfd)
  l1_8    = @('QuickPhone_PDFD_8_Level1_P8_Maintain', 2400, 1900, $dfd)
  l1_9    = @('QuickPhone_PDFD_9_Level1_P9_SystemServices', 2400, 1840, $dfd)
  erd     = @('QuickPhone_Physical_ERD', 4240, 1960, $erd)
}
foreach ($k in $set.Keys) {
  if ($Only -and $k -notin $Only) { continue }
  $name, $w, $h, $src = $set[$k]
  $out = Join-Path $dir "$name.png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 "--window-size=$w,$h" "--screenshot=$out" "$src`?d=$k" 2>$null | Out-Null
  "$k -> $name.png"
}
