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
from .wave_grid import WaveGrid
from .vector_field import VectorField
from .constellation import Constellation
from .dense_mesh import DenseMesh
from .proximity import Proximity

VISUALS: dict[str, type[Visual]] = {
    NetworkMesh.KEY: NetworkMesh,
    Kernel.KEY: Kernel,
    Telemetry.KEY: Telemetry,
    Kalman.KEY: Kalman,
    WaveGrid.KEY: WaveGrid,
    VectorField.KEY: VectorField,
    Constellation.KEY: Constellation,
    DenseMesh.KEY: DenseMesh,
    Proximity.KEY: Proximity,
}

from .background import VisualBackground
