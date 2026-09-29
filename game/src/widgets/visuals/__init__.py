'''
Procedural visuals - animated, theme-colored graphics for demo pages and
title-page backgrounds. Each Visual subclass is registered here by its KEY;
VisualBackground plays one by key. Order here is dropdown order and the
order the "cycle" option rotates through.
'''

from .base import Visual, VisualPalette
from .network_mesh import NetworkMesh
from .kernel import Kernel
from .telemetry import Telemetry
from .kalman import Kalman

VISUALS: dict[str, type[Visual]] = {
    NetworkMesh.KEY: NetworkMesh,
    Kernel.KEY: Kernel,
    Telemetry.KEY: Telemetry,
    Kalman.KEY: Kalman,
}

from .background import VisualBackground  # noqa: E402  (needs VISUALS defined first)
