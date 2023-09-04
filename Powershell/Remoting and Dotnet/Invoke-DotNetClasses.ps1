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

    }
"@

#Note that once this has been added, the session will persist it even after the script has exited, and will throw an error. So close the powershell session and rerun the script.
Add-Type -TypeDefinition $DotNetCSharp
#[Syscommands]::startTaskMgr()


#[Syscommands]::nsCheck("google.com")


#Alternatively
#Methods must be non-static as we are accessing the method via a instance of the class
$obj = New-Object Syscommands
$obj.regeditStart()

