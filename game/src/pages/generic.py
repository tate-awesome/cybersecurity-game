from ..app_core import Context

# Better Widgets
from .. import widgets
# Widgets
from ..widgets import popup
from ..pages.page import Page

# Network
from ..network.network_controller import HardwareAttacker as HardwareNetwork

class GenericPage(Page):
    '''
    Page constructor for attacker/attackerv0. Inherits CTkFrame
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        self.load_page("attacker_lab.json")

        net = context.refresh_net(HardwareNetwork)

        menu_bar = widgets.MenuBar(self, context, "attacker")
        menu_bar.page_buttons()

        trifold = widgets.Panes(self, context, "horizontal", 3, [4, 3, 2], True)

    # Forms
        hacking_side = widgets.Panes(trifold.pane(0), context, "vertical", 2, [2.3, 2], False)
        widgets.panel("network_action_panel", hacking_side.pane(0), context)
        widgets.panel("modbus_table_panel", hacking_side.pane(1), context)

    # Console
        console = widgets.Panes(trifold.pane(1), context, "vertical", 3, [3, 3, 3], False)
        widgets.panel("packet_panel", console.pane(0), context)
        widgets.panel("network_graph_panel", console.pane(1), context)
        widgets.panel("status_panel", console.pane(2), context)


    # Displays
        model = self.context.states.get("model_type")
        if model == "submarine":
            display = widgets.Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
            widgets.panel("submarine_panel", display.pane(0), context)
            widgets.panel("modbus_chart_panel", display.pane(1), context)
        elif model == "hvac":
            display = widgets.Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
            widgets.panel("hvac_panel", display.pane(0), context)
            widgets.panel("modbus_chart_panel", display.pane(1), context)
        else:
            widgets.panel("modbus_chart_panel", trifold.pane(2), context)

        # display.bottom.configure(fg_color=context.style.color("panel"))
        # values = ValuesTable(style, top, context)