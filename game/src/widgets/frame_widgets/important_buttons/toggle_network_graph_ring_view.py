from ._base_button import ToggleButton


class ToggleNetworkGraphRingView(ToggleButton):
    '''Switches the network graph between its table and its ring of hosts (the network_graph_view setting).'''
    LABEL = "menu_bar_buttons_network_graph_ring_view"
    ACTIVE_LABEL = "menu_bar_buttons_network_graph_table_view"
    TOOLTIP = "menu_bar_tooltips_network_graph_view"

    def is_active(self) -> bool:
        return self.context.states.get("network_graph_view") == "ring"

    def start(self):
        self.context.states.set("network_graph_view", value="ring")

    def stop(self):
        self.context.states.set("network_graph_view", value="table")
