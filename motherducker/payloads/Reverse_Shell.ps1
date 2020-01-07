$url = "http://127.0.0.1:8000/payloads/any_rest_api"
$Body = @{
    uuid = (Get-WmiObject -Class Win32_ComputerSystemProduct).UUID
    name = $env:computername
    description = $env:UserName
    ip = $env:HostIP
    status = "True"
}
Invoke-RestMethod -Method 'Post' -Uri $url -Body $body