$DotNetCSharp = @"
    public class Syscommands
    {
        public static void startTaskMgr ()
        {
            System.Diagnostics.Process.Start("taskmgr.exe");
        }
        public void netuser (string cmd)
        {
            string clistr = "/k net.exe "+cmd;
            System.Diagnostics.Process.Start("cmd.exe", clistr);
        }
        public static void nsCheck (string domainname)
        {
            System.Diagnostics.Process.Start("nslookup.exe",domainname);

        }

    }
"@


Add-Type -TypeDefinition $DotNetCSharp
[Syscommands]::startTaskMgr()


[Syscommands]::nsCheck("google.com")


#Alternatively

$var1 = New-Object Syscommands
$var1.netuser("user")