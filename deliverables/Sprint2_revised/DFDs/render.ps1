# Renders each diagram in dfd_source_v3.html to PNG with headless Chrome.
param([string[]]$Only)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$dir = $PSScriptRoot
$src = "file:///" + (Join-Path $dir 'dfd_source_v3.html').Replace('\','/')
$set = [ordered]@{
  context = @('QuickPhone_DFD_0_Context', 2600, 1870)
  level0  = @('QuickPhone_DFD_1_Level0', 3300, 2570)
  l1_1    = @('QuickPhone_DFD_2_Level1_P1_CheckIn', 2400, 1880)
  l1_2    = @('QuickPhone_DFD_3_Level1_P2_Diagnose', 2400, 1910)
  l1_3    = @('QuickPhone_DFD_4_Level1_P3_Repair', 2600, 1800)
  l1_4    = @('QuickPhone_DFD_5_Level1_P4_Notify', 2400, 1910)
  l1_5    = @('QuickPhone_DFD_6_Level1_P5_Release', 2400, 1740)
  l1_6    = @('QuickPhone_DFD_7_Level1_P6_Replenish', 2500, 2090)
  l1_8    = @('QuickPhone_DFD_8_Level1_P8_Maintain', 2400, 1540)
}
foreach ($k in $set.Keys) {
  if ($Only -and $k -notin $Only) { continue }
  $name, $w, $h = $set[$k]
  $out = Join-Path $dir "$name.png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 "--window-size=$w,$h" "--screenshot=$out" "$src`?d=$k" 2>$null | Out-Null
  "$k -> $name.png"
}
