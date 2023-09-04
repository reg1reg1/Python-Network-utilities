function Write-Motivation
{
[CmdletBinding(SupportsShouldProcess= $True)]
param([Parameter()] $Global:FilePath)
Write-Verbose "Deleting $FilePath"
if ($PSCmdlet.ShouldProcess("$FilePath", "Deleting File Forever and ever and ever"))
{
Remove-Item $FilePath
}
}

function TestThePath
{
Test-Path $Filepath

}
function HideFromUser
{
	Write-Output "Hide this function from user"
}

Export-ModuleMember -Function "*-*"