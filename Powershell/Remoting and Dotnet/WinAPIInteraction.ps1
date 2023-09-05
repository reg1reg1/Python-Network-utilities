#Interacting With Windows API

$ApiCode = @"
[DllImport("Kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
public static extern bool CreateSymbolicLink(string lpSymlinkFileName, string lpTargetFileName, int dwFlags);
"@


$Symlink = Add-Type -MemberDefinition $ApiCode -Name Symlink -NameSpace CreateSymlink -Passthru
$Symlink::CreateSymbolicLink("C:\Users\yuvra\Downloads\lnk","C:\Users",1)




