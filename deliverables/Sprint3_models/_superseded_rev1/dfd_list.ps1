# DFD entries for render.ps1: each diagram renders in the logical and the physical view.
$dfds = [ordered]@{
  context = @('0_Context', 2600, 1940, 1940)
  level0  = @('1_Level0', 3550, 3560, 3560)
  l1_1    = @('2_Level1_P1_ScheduleAppointment', 2400, 1510, 1510)
  l1_2    = @('3_Level1_P2_RegisterRepairJob', 2400, 1900, 1900)
  l1_3    = @('4_Level1_P3_RecordDiagnosis', 2400, 1900, 1900)
  l1_4    = @('5_Level1_P4_RecordRepairWork', 2650, 1760, 1760)
  l1_5    = @('6_Level1_P5_SendCompletionNotice', 2700, 1900, 1900)
  l1_6    = @('7_Level1_P6_RecordDeviceRelease', 2500, 1760, 1760)
  l1_7    = @('8_Level1_P7_ProcessPurchaseOrders', 2500, 2110, 2110)
  l1_9    = @('9_Level1_P9_MaintainShopRecords', 2400, 1560, 2610)
}
foreach ($k in $dfds.Keys) {
  $f, $w, $hl, $hp = $dfds[$k]
  $set["${k}_log"]  = @('logical',  "QuickPhone_DFD_$f",  $w, $hl, 'dfd_source.html', "v=log&d=$k")
  $set["${k}_phys"] = @('physical', "QuickPhone_PDFD_$f", $w, $hp, 'dfd_source.html', "v=phys&d=$k")
}
