App

    GUI:

        Navigation:

            common.py

Notated below is the structure that works and is good.
The one's that aren't noted here are WIP or copied from previous versions

    gui/

        drawing/

        navigation/

            widgets/

    network/

        mod_table.py
        modbus_util.py
        network_controller.py
        packet_buffer.py

        hardware/

            arp_spoofing.py
            net_filter_queue.py
            nmap.py
            sniffing.py

        local/

        virtual/



        Hardware:

            (module) Hacking.py                 access point for all hacking?

            (module) Preprocessing.py           packet preprocessing helper module
            (module) Buffer.py                  safely holds data in a sliding window for GUI access
            (module) ARP_Spoofing.py            arp module
            (module) Net_Filter_Queue.py        nfq module
            
            (module) NMap.py                    nmap module
            (module) Sniffing.py                sniffing module

            (scripts) Testing.py

            NEXT: figure out duplicate ACK to stop interrupting communication