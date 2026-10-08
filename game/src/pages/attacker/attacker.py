from ...app_core import Context

# Better Widgets
from ...widgets import (
    MenuBar, Panes, HackingPanel, ModbusPanel, PacketConsole,
    NetworkDiagram, StatusConsole, SniffedSubmarineMap, VariableMonitor, SniffedHVACHouse,
)
# Widgets
from ...pages.page import Page

class AttackerV0(Page):
    '''
    Page constructor for attacker/attackerv0.
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        menu_bar = MenuBar(self, context, "attacker")
        menu_bar.page_buttons()

        trifold = Panes(self, context, "horizontal", 3, [4, 3, 2], True)

    # # Forms
        hacking_side = Panes(trifold.pane(0), context, "vertical", 2, [2.3, 2], False)
        HackingPanel(hacking_side.pane(0), context)
        ModbusPanel(hacking_side.pane(1), context)

    # Console
        console = Panes(trifold.pane(1), context, "vertical", 3, [3, 3, 3], False)
        PacketConsole(console.pane(0), context)
        NetworkDiagram(console.pane(1), context)
        StatusConsole(console.pane(2), context)


    # Displays
        model = self.context.states.get("modbus_model_selected")
        if model == "sniffed_submarine_map":
            display = Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
            SniffedSubmarineMap(display.pane(0), context)
            VariableMonitor(display.pane(1), context)
        elif model == "sniffed_hvac_house":
            display = Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
            SniffedHVACHouse(display.pane(0), context)
            VariableMonitor(display.pane(1), context)
        else:
            ...
            VariableMonitor(trifold.pane(2), context)

        # display.bottom.configure(fg_color=context.style.color("panel"))
        # values = ValuesTable(style, top, context)