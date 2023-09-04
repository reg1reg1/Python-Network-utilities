function CheckPatch
{
$cutoff = (Get-Date).AddDays(-90)

$filter = "LastLogonDate -gt '$cutoff'"

$computerNames = Get-ADComputer -Filter $filter -Properties OperatingSystem,Description,LastLogonDate |
    Select Name,OperatingSystem,Description,LastLogonDate | Foreach-Object {$_.Name}
foreach ($i in $computerNames)
{
 
 try {
    $value =   Get-HotFix -ComputerName $i | Where-Object -Property HotfixID -EQ "KB2871997"
    if ($value)
        {
            Write-Output "Hotfix found on $i"
        }
        #$ErrorActionPreference = "Stop"; #Make all errors terminating
     else
     {
        Write-Output "Hotfix not installed for $i"
     }
    } 
 catch{
        Write-Host "RPC server unavailable for Workstation $i";
        Write-Host $Error[0].Exception;
    }
}
} 