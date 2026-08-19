from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core import Context

NODE_RADIUS = 6

class NetworkDiagramCanvas(Canvas):
    '''
    Canvas that displays hosts as nodes and packet flow as arrows between them.
    Live mode flashes arrows for recent traffic; paused mode shows the MAC/IP
    path of the single packet selected in the packet console.
    '''

    def __init__(self, master: CTkFrame, context: Context):
        super().__init__(master, context, ((-1.3, -1.3), (1.3, 1.3)))
        self.network = context.net.buffer.network
        self.packets = context.net.buffer.packets

        def draw_host(mac, point):
            cx, cy = self.camera.world_to_canvas([point])[0]
            self.create_oval(
                cx - NODE_RADIUS, cy - NODE_RADIUS, cx + NODE_RADIUS, cy + NODE_RADIUS,
                fill=context.style.color("accent"), outline=""
            )
            self.create_text(
                cx, cy - NODE_RADIUS - 8, text=mac,
                fill=context.style.color("field_text"), font=("Consolas", 9)
            )

        def frame_callback():
            self.delete("all")
            self.draw.background(context.style.color("field"))

            positions = self.network.get_host_positions()
            for mac, point in positions.items():
                draw_host(mac, point)

            mode = context.states.get("packet_console_state", "mode")

            if mode == "paused":
                mpkt = self.packets.get_selected()
                if mpkt is None:
                    return

                mac_src, mac_dst = mpkt.get("mac_src"), mpkt.get("mac_dst")
                if mac_src in positions and mac_dst in positions and mac_src != mac_dst:
                    self.draw.visible_arrow([positions[mac_src], positions[mac_dst]], context.style.color("accent"))

                    ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                    if ip_src != "-" and ip_dst != "-":
                        self.draw.visible_arrow([positions[mac_src], positions[mac_dst]], context.style.color("scrollbar_hover"))
            else:
                for mpkt, macs in self.network.get_arrows_this_tick().items():
                    src, dst = macs
                    if src in positions and dst in positions and src != dst:
                        self.draw.visible_arrow([positions[src], positions[dst]], context.style.color("accent"))

        self.set_frame_callback(frame_callback)
        self.start_animation()
