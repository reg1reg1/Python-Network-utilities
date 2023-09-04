$Classes = [AppDomain]::CurrentDomain.GetAssemblies() | ForEach-Object {$_.GetTypes()} | Where-Object {$_.Name -eq "Process"}


#Get-Member won't return static members by default and need to be explicitly asked
$Classes | Get-Member -MemberType Method -Static



Add-Type -AssemblyName System.Windows.Forms		
#We can't use Get-Member on System.Windows.Forms


# A way to do it is filter on the basetype 
[Appdomain]::CurrentDomain.GetAssemblies() | ForEach-Object {$_.GetTypes()} | Where-Object {$_.BaseType -match "System.Windows.Forms"}



# If you have a definite class object like SendKeys in the forms , then we can fetch the members