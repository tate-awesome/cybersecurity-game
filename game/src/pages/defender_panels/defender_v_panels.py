from ...app_core import Context

# Widgets
from ...widgets import (
    MenuBar, Panes, HackingPanel, DefenderModbusPanel, PacketConsole,
    NetworkDiagram, StatusConsole, ModbusModel, DefenderStripchartPanel,
)
from ..page import Page


class DefenderVPanels(Page):
    '''
    Hardcoded testing page for the panels-based defender rebuild. Same
    trifold layout as AttackerV0/DefenderV0:

      - network_action_panel (HackingPanel) reused as-is, extended with the
        AP Connection/Encryption/AP Tunnel/Kalman Filter forms
      - modbus_table_panel replaced by defender_modbus_panel
        (DefenderModbusPanel): mode label, live client/server readout,
        filter sliders
      - packet_panel/network_graph_panel/status_panel reused as-is
      - modbus_model_panel reused as-is, extended with defender_hvac/
        defender_submarine models that auto-switch with the AP's mode
      - modbus_chart_panel replaced by defender_stripchart_panel
        (DefenderStripchartPanel)

    Unlike AttackerV0/DefenderV0, this page does load its own config.json's
    "settings" (the way WorkspacePage does) - it needs network_action_
    visibility/modbus_model_visibility entries _admin.json alone doesn't
    carry (ap_connect, defender_hvac, ...), so it can't just rely on
    whatever context.states already happens to hold at startup.
    '''

    def __init__(self, context: Context):
        super().__init__(context)

        key = context.router.current_page
        context.pages.prepare_page_config(key)

        menu_bar = MenuBar(self, context, "defender_panels")
        menu_bar.page_buttons()

        trifold = Panes(self, context, "horizontal", 3, [4, 3, 2], True)

    # Forms
        left_side = Panes(trifold.pane(0), context, "vertical", 2, [2.3, 2], False)
        HackingPanel(left_side.pane(0), context)
        DefenderModbusPanel(left_side.pane(1), context)

    # Console
        console = Panes(trifold.pane(1), context, "vertical", 3, [3, 3, 3], False)
        PacketConsole(console.pane(0), context)
        NetworkDiagram(console.pane(1), context)
        StatusConsole(console.pane(2), context)

    # Displays
        display = Panes(trifold.pane(2), context, "vertical", 2, [2, 2], False)
        ModbusModel(display.pane(0), context)
        DefenderStripchartPanel(display.pane(1), context)
