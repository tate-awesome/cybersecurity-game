from ....app_core import Context
from ...canvases.network_diagram import NetworkDiagramCanvas
from ..panel import Panel
from ...frame_widgets.important_buttons import ClearNetworkHosts, EditNetworkHosts, ToggleNetworkGraphRingView

class Builder(Panel):
    '''The graph of hosts seen on the network and the traffic between them (see NetworkDiagramCanvas).'''
    KEY = "hosts_panel"
    # The settings keys (see _packages/_default.json) this panel reads or writes -
    # the workspace editor lists it under each of them
    # packet_console's "mode" switches the graph between live arrows and paused labels
    SETTINGS = (
        "packet_console",
        "network_hosts",
        "network_graph_view",
    )
    def __init__(self, master, context: Context):
        super().__init__(master, context, self.KEY)

        self.diagram = NetworkDiagramCanvas(self, context)

        self.menu_bar.add_important(EditNetworkHosts)
        self.menu_bar.add_important(ClearNetworkHosts)
        self.menu_bar.add_important(ToggleNetworkGraphRingView)
        self.menu_bar.minimize_button(self.diagram)
