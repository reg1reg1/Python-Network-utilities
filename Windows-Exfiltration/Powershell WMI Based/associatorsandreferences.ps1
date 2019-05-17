#_RELPATH property of an Instance can be used as a key to list relationships

#"Associators of" can be used to get assosciations of al
Get-WmiObject -Class Win32_NetworkAdapter -Filter "DeviceId=2"
Get-WmiObject -Query "Associators of {Win32_NetworkAdapter.DeviceId=11}"
Get-WmiObject -Query "Associators of {Win32_Process}" -Filter "DeviceId=12"
Get-WmiObject -Query ""

#This query will list the class definitions of associated classes
Get-WmiObject -Query "Associators of {Win32_NetworkAdapter.DeviceId=2} Where ClassDefsOnly"



#Observe what the relpath property contains for the class
Get-WmiObject -Class Win32_Process | fl __RELPAT*
#The RELPATH value will be the one which will be used to query the associators of
#Invalid handle causes the query to throw an error
Get-WmiObject -Query "Associators of {Win32_process.Handle=2345}"

#Equivalent CIM query, (always prefer CIM over WMI)
Get-CimAssociatedInstance -InputObject (Get-CimInstance -ClassName Win32_NetworkAdapter -Filter "DeviceId=12")

#This is to list the associated classes with the current instance
Get-WmiObject -Query "Associators of {Win32_Process.Handle=9368} Where ClassDefsOnly"

Get-WmiObject -Class Win32_process -Filter 'Handle=9368'
#It will show all the associated classes , but let us use a different filter and a different
#syntax

#Retrieve instance of a single associated class, just add a where class
Get-WmiObject -Query "Associators of {Win32_Process.Handle=9368} Where ClassDefsOnly and AssocClass=Win32_ProtocolBinding"
