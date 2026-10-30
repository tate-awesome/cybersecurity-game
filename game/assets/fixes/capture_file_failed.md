# Capture File Error

Reading or writing a capture file (PCAP or JSON) failed.

## Check

- **Is it the right kind of file?** **Load PCAP** opens `.pcap`/`.pcapng` files. The JSON loaders open `.json` and `.mcap` captures that the game saved.
- **Is the file damaged?** A capture that was cut off mid-write (for example, when the game was closed during a stream) may not load. Try another copy.
- **Permissions.** Saving needs a folder you can write to. If the game ran as Administrator, files it made earlier may belong to the administrator account. Save somewhere new, such as your Documents folder.
- **Disk space.** Long streams can fill a nearly full disk.
