
#----Namespaces commands---
#Printing Name property of each Namespace
T#The "Namespace" class contains information about namespaces, and is within the root namespace
Get-WmiObject -Namespace Root -Class "__Namespace" | Select-Object -Property Name
#List all namsespaces within the root Namespace
Get-WmiObject -Namespace root -Class "__Namespace" 
Get-CimInstance -Namespace root -Class "__Namespace"
Get-WmiObject -Namespace "root" -class "__Namespace" | Select Name
#Recursive look for namespace (Default namespace argument is set to root)
#Run the powershell in admin mode
function Get-Recursive-Namespace {
    param($Namespace='root')
    Get-WmiObject -Namespace $Namespace -Class "__Namespace" | ForEach-Object{
        ($ns = '{0}\{1}' -f $_.__Namespace,$_.Name)
        Get-Recursive-Namespace $ns
    }    
}
#Get-Recursive-Namespace root or without arguments 


#Playing around with classes (All the classes with bios in their Name)
Get-WmiObject -Class *bios* -List
Get-WmiObject -Class *Win32_Net* -List
#Count the no of classes in the default namespace , measure is the keyword
Get-WmiObject -Class * -List | measure

#Many classes are of good importance like Win32_process and win32


#Lists the objects in win32 which is only 1
Get-WmiObject -Class win32_process -List
Get-WmiObject -Class win32_process -Filter "Name='explorer.exe'" | Select ProcessId
Get-WmiObject -Class win32_process -Filter "Name='explorer.exe'" | Select-Object ProcessId
Get-WmiObject -Class win32_process -Filter "Name='explorer.exe'" | Select-Object ProcessId

#Using Query
Get-WmiObject -Query "select ProcessId from Win32_process where Name='explorer.exe'"

#Using class to remove objects
Get-WmiObject -Query "Select * from Win32_process where Name='Calculator.exe'" | Remove-WmiObject
Get-WmiObject -Class win32_process -Filter "Name='Calculator.exe'" | Remove-WmiObject
Get-CimInstance -ClassName win32_process -Filter 



#Selecting Methods from the Win32 process, Understanding Methods
#First step is to find the arguments that a method uses 
#A lot of crucial scripts below (wrt syntax structure)

Get-WmiObject -List | Select Methods
Get-WmiObject -List | Where-Object {$_.Methods}
Get-CimClass -MethodName Create
Get-WmiObject -class win32_process -List | Select-Object -ExpandProperty Methods 
Get-WmiObject -class win32_process -List | Select-Object -ExpandProperty Methods | where name -eq "create" 
Get-WmiObject -class win32_process -List | Select-Object -ExpandProperty Methods | where name -eq "create" | -ExpandProperty Parameters
Get-CimClass -ClassName win32_process 
#Invoking Methods, now that we know their arguments
Invoke-WmiMethod -class win32_process -Name Create -ArgumentList calc.exe



#Selects the method attribute of the displayed object(See the output of above and below queries in sequence)
Get-WmiObject -Class win32_process -List | Select-Object -Property Methods
Get-WmiObject -Class win32_process -List | Select Methods
Get-WmiObject -Class win32_process -List | Get-Member -memberType Methods
Get-WmiObject -Class win32_process -List | Where-Object {$_.Methods} #another way
#Expand on the methods, want to see more expand on the methods object
Get-WmiObject -class win32_process -List | Select-Object -ExpandProperty Methods



#See what columns are present within a certain class
Get-WmiObject -Class "Win32_process" -List | Format-List -Property *










#--------------------------Query other Namespaces to display useful information----------------
#It is important to understand which information lies in what namespace
#Get all logged on accounts and display the username column
Get-WmiObject -Class win32_computerSystem | Select-Object username

Get-WmiObject -Namespace "root/cimv2" -List

#Load antivirus product The namespace SecurityCenter2 and SecurityCenter both are useful
Get-WmiObject -namespace root/SecurityCenter2 -Class AntiVirusProduct -List
Get-WmiObject -Namespace root/SecurityCenter -List 

#Visualize EventLogs:
#lets see what properties are present in the LogEVENT
Get-WmiObject -class Win32_NTLogEvent -List | Format-List -Property *
#Expands on each member of the class
Get-WmiObject Win32_NTLogEvent | Get-Member -memberType Properties




$Logs = Get-WmiObject -class Win32_NTLogEvent -Filter "(logfile=’Application’) AND (type=’error’)" 
$Logs | Format-Table EventCode, EventType, Message -auto

$Logs = Get-WmiObject -query `
"SELECT * FROM Win32_NTLogEvent WHERE (logfile=’Application’) AND (type=’error’)" 
$Logs | Format-Table EventCode, EventType, Message -auto



Get-WmiObject -Namespace root/cimv2 -List 


Get-WmiObject -Namespace Root\cimv2\Security -List | 



Invoke-WmiMethod -Namespace rootdefault -Class StdRegProv -Name 
