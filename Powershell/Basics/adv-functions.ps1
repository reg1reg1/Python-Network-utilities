

function fooBar {

    param (
    [Parameter (Mandatory =$True)]
    $n1,
    [Parameter ()]
     $n2
     )
     Write-Output "$n1"
     Write-Output "$n2"

}

 function fooBar-1 {

    param (
    [Parameter (Mandatory =$True, Position=2)]
    $n1,
    [Parameter (Position=1)]
     $n2
     )
     Write-Output "$n1"
     Write-Output "$n2"

}
 


function fooBar-2 {

    param ([Parameter (Mandatory =$True, ValueFromPipeline=$True)] $n1, [Parameter (ValueFromPipeline=$True)] $n2)
     Write-Output "$n1"
     Write-Output "$n2"
}

function fooBar-3 {

    param ([Parameter (Mandatory =$True, ValueFromPipeline=$True, ParameterSetName="Set1")] $n1, [Parameter (ValueFromPipeline=$True, ParameterSetName="Set2")] $n2)
     Write-Output "$n1"
     Write-Output "$n2"
     Write-Verbose "Hello"
}
 
 
