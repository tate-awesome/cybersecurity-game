from .core.canvas import Canvas
from customtkinter import CTkFrame
from ...app_core import Context
import math

NODE_RADIUS = 6
ARROW_OFFSET = 0.15

def offset_perpendicular(p1, p2, amount):
    '''
    Nudges both points sideways, perpendicular to the p1->p2 direction,
    so two arrows sharing the same endpoints render as visibly separate lines.
    '''
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return p1, p2
    nx, ny = -dy / length, dx / length
    return (p1[0] + nx * amount, p1[1] + ny * amount), (p2[0] + nx * amount, p2[1] + ny * amount)

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
                    p1, p2 = positions[mac_src], positions[mac_dst]

                    ip_src, ip_dst = mpkt.get("ip_src"), mpkt.get("ip_dst")
                    has_ip = ip_src != "-" and ip_dst != "-"

                    # if has_ip:
                    #     mac_p1, mac_p2 = offset_perpendicular(p1, p2, -ARROW_OFFSET)
                    #     ip_p1, ip_p2 = offset_perpendicular(p1, p2, ARROW_OFFSET)
                    #     self.draw.visible_arrow([mac_p1, mac_p2], context.style.color("accent"))
                    #     self.draw.visible_arrow([ip_p1, ip_p2], context.style.color("scrollbar_hover"))
                    # else:
                    self.draw.visible_arrow([p1, p2], context.style.color("accent"))
            else:
                for mpkt, macs in self.network.get_arrows_this_tick().items():
                    src, dst = macs
                    if src in positions and dst in positions and src != dst:
                        self.draw.visible_arrow([positions[src], positions[dst]], context.style.color("accent"))

        self.set_frame_callback(frame_callback)
        self.start_animation()
