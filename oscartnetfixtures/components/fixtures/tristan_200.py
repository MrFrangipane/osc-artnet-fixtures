import logging

from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood

from oscartnetfixtures.python_extensions.math import map_to_int, p_cos

_logger = logging.getLogger(__name__)


class Tristan200(BaseFixture):
    @dataclass
    class Mapping:
        pan: int = 0
        pan_fine: int = 0
        tilt: int = 0
        tilt_fine: int = 0
        moving_speed: int = 0
        color: int = 0
        gobo1: int = 0
        gobo1_rotation: int = 0
        gobo2: int = 0
        prism: int = 0
        prism_rotation: int = 0
        frost: int = 0
        focus: int = 0
        focus_fine: int = 0
        shutter: int = 0
        dimmer: int = 0
        dimmer_fine: int = 0
        reset: int = 0

    def __init__(self, address=None):
        super().__init__(address)
        self.elapsed = 0

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        self.elapsed += mood.animation / 10.0
        sym = (group_position * 2.0) - 1.0

        mapping = Tristan200.Mapping()
        mapping.color = map_to_int(mood.palette, 66, 80)

        if mood.texture > .66:
            mapping.focus = 255
            mapping.gobo2 = 11
            dim_factor = 1.0

        elif mood.texture > .33:
            mapping.focus = 255
            mapping.gobo1 = 28
            mapping.prism = 26
            mapping.frost = 34
            mapping.prism_rotation = 179 + int(group_position * 27)
            dim_factor = 0.6

        else:
            mapping.prism = 26
            mapping.frost = 144
            dim_factor = 0.4

        if mood.blinking > .7:
            mapping.shutter = 121

        elif mood.blinking < .3:
            dim_factor *= p_cos(mood.beat_counter * 6.28)

        pan = p_cos(mood.beat_counter + 1.57 * sym) * .3
        if .6 > mood.animation > .3:
            pan = 0.18  # roughly 45, centered

        mapping.pan = map_to_int(pan)
        mapping.tilt = 40
        mapping.dimmer = map_to_int(mood.master_dimmer * mood.recallable_dimmer * dim_factor * 0.5)

        return list(vars(mapping).values())
