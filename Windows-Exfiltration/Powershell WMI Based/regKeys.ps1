$HKEY_CURRENT_USER =2147483649
$computer ='.'
$reg = [WMIClass]"ROOT\DEFAULT:StdRegProv"
$Key = "Console"
$Value = "HistoryBufferSize"
$results = $reg.GetDWORDValue($HKEY_CURRENT_USER, $Key, $value)
"Current History Buffer Size: {0}" -f $results.uValue