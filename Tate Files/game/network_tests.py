from src.network import network_controller

class tests:

    def hardware_test():
        net = network_controller.HardwareNetwork()
        try:
            net.start_arp()
            net.start_nfq()

            input("Press Enter to print all positions received")

            print(net.buffer.get_all_positions("in"))
        finally:
            net.stop_arp()
            net.stop_nfq()

if __name__ == "__main__":
    tests.hardware_test()
