<#
Gathering information from the box using WMI which is an effective stealthy tool
How to maximise leverage cmd presence via WMI

#>
#Listing classes to look for useful stuff
Get-WmiObject -Class *Win32_IP* -List

#Listing useful information about route tables
Get-WmiObject -Class Win32_IP4RouteTable | Select-Object -Property Description,Mask

#Let's have a look at the local accounts,domains, trusted domains etc 
#Users for not just the current box , but the current domain, and domains which have bidirectional trust with our current domain
Get-WmiObject -Class Win32_UserAccount

#Local domain, trusted domains, and trusted forest is also revealed
Get-WmiObject -Class Win32_Group

#We have escalated privileges
#Use win32_shadow copy of the C drive of domain controller. Keys to the kingdom? Copying C drive of the domain controller
#Needs admin privileges on the box
#Can be used to extract system secrets
Get-WmiObject -Class win32_shadowcopy

#Lookup basic commands in case you forget syntax of wmql
Get-WmiObject -Class Win32_ShadowCopy -List | Select -ExpandProperty Methods | where Name -eq Create


<#
Using Admin jump boxes as jump points
These are saved session informations 
#>









