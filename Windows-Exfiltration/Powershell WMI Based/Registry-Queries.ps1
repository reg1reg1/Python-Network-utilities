#Learn more about registry, how it functions, purpose it serves
#https://support.microsoft.com/en-us/help/256986/windows-registry-information-for-advanced-users
#https://docs.microsoft.com/en-us/previous-versions/windows/desktop/regprov/enumkey-method-in-class-stdregprov


#-----------------------Registry Modifiers, query registry----------------------------
#Below is an alternate way of doing this

#This iwll list the different keys(it is in root default namespace)
$x = Get-WmiObject -Namespace root\default -Class StdRegProv -List

$x.Methods
#Registry values
#Show C
#https://docs.microsoft.com/en-us/previous-versions/windows/desktop/regprov/stdregprov
#What can we do to the registry? Expand the property methods to find out.
Get-WmiObject -Namespace root\default -Class StdRegProv -List | select -ExpandProperty Methods
#OR
(Get-WmiObject -Namespace root\default -Class StdRegProv -List).Methods


Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"software\microsoft\internet explorer")


#The registry key value is retrieved (each visied url is sotred as url 1 , url2 etc on the system)
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483649,"software\microsoft\internet explorer\typedurls","url1")

Get-WmiObject -class Win32_TSGeneralSetting -Namespace root\cimv2\TerminalServices -Filter TerminalName='RDP-tcp'

#HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer") |  Select -ExpandProperty sNames

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483650,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU","a")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483650,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU") | Select -ExpandProperty sNames