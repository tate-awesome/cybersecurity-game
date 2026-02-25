fixed menu bar
    page name
    
    themes
    settings
    help
    quit
    stop network activity

scrollable left panel
    nmap widget
    arp widget
    sniff widget
    nfq widget

tabbed center panel
    terminal for nmap, arp, sniff, nfq
    canvases for world map, data over time, compass, rudder, speed, network visualizer

tabbed right panel
    widgets for modifying values
    widgets for advanced hacking

Bottom:
    Net tab: master, slave, you, packet dings, pps metrics

Map additions:
    Rudder, speed, x, y, t metrics
    

Nmap
arp
sniff: show all, learn to filter, learn conversion
dos
mitm (nfq) with mod values: show modbus


right side

console with level of detail options
pkt show, summary, pretty print


net visual
show connections, pps

path gaps & inferences when there's a break in communication

new menu bar:

[back arrow] [refresh] Title   - 100% + [gear] [help] [light/dark moon] [theme palette] [fullscreen box] [exit X]
< ⟳ Title         - 100% +  ⚙️  ❔ 🎨  ▢  ❌


I need to make a console to print all of my text-based hacking outputs. I think each hack should own its own tab, so the user can look at different outputs freely.

I might have to rework the buffer to be able to handle different packets from different sources.
Also .putting metapacket objects because they're better.
Creating different strings of positions based on timing - to catch breaks as they come in.
Putting a lot of things in the buffer - results from every hack. (better agnostic interface for other game versions)

I NEED to stop breaking communications with nfq. So annoying.
Sometimes with only ARP hack, the chip dies

Gotta add a "GUI save" class for the context to hold it's too messy in there


Tabview -> tab -> console -> update loop (100ms) pulls everything from buffer to display (print for now)
Hack widget -> hack.start -> handler -> hack.put -> buffer["hack"].packet OR NMAP result OR ARP lines

Map -> get_trails -> buffer.all_trails[list[list[tuple[float,float]]]] -> for each trail in trails drawline(trail)
Also Hack widget -> hack.start -> handler -> var_buffer.put(x, y, t, s, r) -> if(last_time > 50): new trail, if(last_time > 50): break_variable_seismograph, if(t): last_t = t, if (x,y): last_xy = x, y,