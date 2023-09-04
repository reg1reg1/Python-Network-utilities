function RemovePathCustom
{
[CmdletBinding(SupportsShouldProcess= $True)]
param([Parameter()] $Global:FilePath)
Write-Verbose "Deleting $FilePath"
if ($PSCmdlet.ShouldProcess("$FilePath", "Deleting File Forever and ever and ever"))
{
Remove-Item $FilePath
wmic qfe list
}
}

function TestThePath
{
Test-Path $Filepath

}