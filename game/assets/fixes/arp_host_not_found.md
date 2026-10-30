# Host Not Found

To ARP spoof, the game first asks the network for the MAC address of each IP you entered, and nothing answered for one of them.

## Check

- **Are the IP addresses right?** Run **NMap** and open its report to see which hosts are up, then copy the addresses from there.
- **Are you on the same network?** ARP only works inside one local network. Both IPs have to be on the subnet you're connected to.
- **Are the devices on and awake?** A device that's asleep or turned off won't answer.

The spoof keeps asking, so once the host answers it carries on without a restart.
