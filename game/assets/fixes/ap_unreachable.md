# Can't Reach the Access Point

The game polls the lab's access point (AP) over HTTP for its data, and the request failed or stopped getting answers.

## Check

- **Are you on the AP's network?** The AP only answers devices connected to its own Wi-Fi. Use the **WiFi Switch** form, or join that network by hand.
- **Is the AP powered on?** After power returns, give it a few seconds to boot.
- **Is the address right?** The AP's URL comes from the workspace's AP settings. Open it in a browser (**Open AP Config** in the menu bar). If the page doesn't load there either, the problem is the network, not the game.
- **Is something blocking it?** Firewalls and VPNs can block local HTTP requests.

Once the AP answers again, the poller reconnects by itself.
