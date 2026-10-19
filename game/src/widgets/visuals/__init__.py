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


def background_choices(context) -> dict[str, str]:
    '''
    What the background pickers offer, key -> shown name: No Background,
    every visual not hidden from them (see Style.background_hidden - chosen
    on the visuals demo page), then Cycle All when there's more than one.
    '''
    from ...app_core.context.style import NO_BACKGROUND
    hidden = context.style.background_hidden
    keys = [key for key in VISUALS if key not in hidden]
    if len(keys) > 1 and "cycle" not in hidden:
        keys.append("cycle")
    return {key: context.labels.get(f"visual_names_{key}") for key in [NO_BACKGROUND, *keys]}

from .background import VisualBackground
