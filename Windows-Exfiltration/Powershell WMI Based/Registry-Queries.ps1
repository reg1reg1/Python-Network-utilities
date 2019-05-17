#https://support.microsoft.com/en-us/help/256986/windows-registry-information-for-advanced-users
#https://docs.microsoft.com/en-us/previous-versions/windows/desktop/regprov/enumkey-method-in-class-stdregprov

#Registry keys
HKEY_CURRENT_USER : 2147483649
HKLM : 2147483650
HKROOT : 2147483652
HKU USER: 2147483651
HKU Current Config: 2147483653


#For reference open the registry and see where each stuff is easy for ease of querying







#-----------------------Registry Modifiers, query registry----------------------------
#Below is an alternate way of doing this

#This iwll list the different keys(it is in root default namespace)
$x = Get-WmiObject -Namespace root\default -Class StdRegProv -List

$x.Methods
#Registry values
#Show C
#https://docs.microsoft.com/en-us/previous-versions/windows/desktop/regprov/stdregprov
#What can we do to the registry? Expand the property methods to find out.


#StdRegProv is the key class, let us look at all the methods available
Get-WmiObject -Namespace root\default -Class StdRegProv -List | select -ExpandProperty Methods
#OR
(Get-WmiObject -Namespace root\default -Class StdRegProv -List).Methods

#Let us exlpore the keys
#First we will use EnumKey function which was shown under methods.
#Using the Enumkey to search the software namespace
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"software\") | Select -ExpandProperty -sNames
#Let us explore Microsoft
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"software\microsoft") | Select -ExpandProperty -sNames

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"software\Microsoft") | Select -ExpandProperty sNames


#The registry key value is retrieved (each visied url is sotred as url 1 , url2 etc on the system)
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483649,"software\microsoft\internet explorer\typedurls","url1")

Get-WmiObject -class Win32_TSGeneralSetting -Namespace root\cimv2\TerminalServices -Filter TerminalName='RDP-tcp'

#HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name Enumkey @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer") |  Select -ExpandProperty sNames

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name GetStringValue @(2147483650,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU","a")

Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483649,"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU") | Select -ExpandProperty sNames



#HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache
#Contains the cache information for the commands which were run
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483649,"Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache") | Select -ExpandProperty sNames
#HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache
Invoke-WmiMethod -Namespace root\default -Class StdRegProv -Name EnumValues @(2147483649,"Software\Classes\Local Settings\Software\Microsoft\Windows\ShellNoRoam\MuiCache") | Select -ExpandProperty sNames