$DotNetCSharp = @"
    public class Syscommands
    {
        public static void startTaskMgr ()
        {
            System.Diagnostics.Process.Start("taskmgr.exe");
        }
        public static void netuser (string cmd)
        {
            string clistr = "/k net.exe "+cmd;
            System.Diagnostics.Process.Start("cmd.exe", clistr);
        }
        public static void nsCheck (string domainname)
        {
            System.Diagnostics.Process.Start("nslookup.exe",domainname);

        }
        public void regeditStart()
        {
            System.Diagnostics.Process.Start("regedit.exe");
        }
        public static void Main()
        {
            System.Diagnostics.Process.Start("chrome.exe");
        }

    }
"@


#outputting to a DLL file with output type library, these require our typedefinitions to have an entry point or main() function
Add-Type -TypeDefinition $DotNetCSharp -OutputType Library -OutputAssembly InvokeDotNetClasses.DLL

Add-Type -TypeDefinition $DotNetCSharp -OutputType ConsoleApplication -OutputAssembly InvokeDotNetClasses.exe


#The .exe will open chrome browser on clicking it


#To access the DLL file, we can use the passthru parameter
$var2 = Add-Type -Path .\InvokeDotNetClasses.dll -PassThru
#We can then enumerate members using the var2 variable. We basically can then access all the functions via this DLL file we just outputted to

$var2 | Get-Member -Static 

# This would not show us the non-static regedit member 
#Use the Getmethods function instead if you want access to all the methods.
$var2.GetMethods() | Where-Object {$_.Name -match "regedit"}

#the ability to load dlls and use functions within powershell using dotnet, makes it very powerful tool