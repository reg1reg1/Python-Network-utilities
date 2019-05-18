$users = @{}
$process = Get-Process

Get-WmiObject Win32_SessionProcess | ForEach-Object {

    $userid = (($_.Antecedent -split “=”)[-1] -replace '"'  -replace “}”,“”).Trim()
    if($users.ContainsKey($userid))
    {
        #Get username from cache
        $username = $users[$userid]
    } 
    else 
    {
        $username = (Get-WmiObject -Query "ASSOCIATORS OF {Win32_LogonSession.LogonId='$userid'} WHERE ResultClass=Win32_UserAccount").Name
        #Cache username
        $users[$userid] = $username
    }

    $procid = (($_.Dependent -split “=”)[-1] -replace '"'  -replace “}”,“”).Trim()
    $proc =  $process | Where-Object { $_.Id -eq $procid }

    New-Object psobject -Property @{
        UserName = $username
        ProcessName = $proc.Name
        "WorkingSet(MB)" = $proc.WorkingSet / 1MB
    }
}