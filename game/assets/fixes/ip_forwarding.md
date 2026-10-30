# IP Forwarding

While you're spoofing, traffic between the two hosts passes through your computer. **IP forwarding** passes that traffic on to where it was going. Without it, the two hosts simply lose their connection.

## Windows

Run this in PowerShell **as Administrator**, then restart the computer:

```
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name IPEnableRouter -Value 1 -Type DWord
```

## Linux

```
sudo sysctl -w net.ipv4.ip_forward=1
```

## macOS / other systems

The game doesn't know how to turn forwarding on for this system. On macOS: `sudo sysctl -w net.inet.ip.forwarding=1`.

If turning it **off** failed, run the same command with `0` (Linux/macOS) to put the setting back.
