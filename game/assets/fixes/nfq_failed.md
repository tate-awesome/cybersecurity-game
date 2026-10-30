# NFQ Error

The NFQ hook intercepts packets through a Linux *netfilter queue*, and something went wrong with the queue.

## Check

- **Root.** iptables and the queue need root, so start the game with `sudo`.
- **The netfilterqueue package.** Run `pip install netfilterqueue`. It builds against `libnetfilter-queue-dev` (`sudo apt install libnetfilter-queue-dev`).
- **Leftover rules.** If NFQ didn't stop cleanly, its iptables rules may still be active, and traffic may stall. Remove them with:

```
sudo iptables -t mangle -F
```

Then start the NFQ hook again.
