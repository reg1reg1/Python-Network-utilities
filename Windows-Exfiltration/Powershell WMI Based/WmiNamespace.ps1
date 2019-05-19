#Script has been taken from Mattifestation

<#
Anyone interested in Powershell and WMI exploits should definitely follow him and check him out
https://github.com/mattifestation
#>


# Yes I know I should do this with the CIM cmdlets too...
function Get-WmiNamespace {
<#
.SYNOPSIS

Returns a list of WMI namespaces present within the specified namespace.

.PARAMETER Namespace

Specifies the WMI repository namespace in which to list sub-namespaces. Get-WmiNamespace defaults to the ROOT namespace.

.PARAMETER Recurse

Specifies that namespaces should be recursed upon starting from the specified root namespace.

.EXAMPLE

Get-WmiNamespace

.EXAMPLE

Get-WmiNamespace -Recurce

.EXAMPLE

Get-WmiNamespace -Namespace ROOT\CIMV2

.EXAMPLE

Get-WmiNamespace -Namespace ROOT\CIMV2 -Recurse

.OUTPUTS

System.String

Get-WmiNamespace returns fully-qualified names.
#>

    [OutputType([String])]
    Param (
        [String]
        [ValidateNotNullOrEmpty()]
        $Namespace = 'ROOT',

        [Switch]
        $Recurse
    )

    $BoundParamsCopy = $PSBoundParameters
    $null = $BoundParamsCopy.Remove('Namespace')

    # Exclude locale specific namespaces
    Get-WmiObject -Class __NAMESPACE -Namespace $Namespace -Filter 'NOT Name LIKE "ms_4%"' |
    ForEach-Object {
        $FullyQualifiedNamespace = '{0}\{1}' -f $_.__NAMESPACE, $_.Name
        $FullyQualifiedNamespace

        if ($Recurse) {
            Get-WmiNamespace -Namespace $FullyQualifiedNamespace @BoundParamsCopy
        }
    }
}