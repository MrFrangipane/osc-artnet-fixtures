import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int


class OctostripBar(BaseFixture):
    desaturate_threshold = 0.75

    @dataclass
    class Mapping:
        rainbow: int = 0
        red: int = 0
        green: int = 0
        blue: int = 0
        strobe: int = 0  # 1-20 Hz
        chase: int = 0  # sound active 241-255

    def map_to_channels(self) -> list[int]:
        # color
        offset = 0  # ((group_position * 2) - 1) * mood.animation * 0.5
        hue = (self.mood.palette + offset) % 1.0
        saturation = 1.0 - (self.mood.blinking - self.desaturate_threshold) / self.desaturate_threshold \
            if self.mood.blinking > self.desaturate_threshold else 1.0
        value = math.pow(self.mood.master_dimmer * self.mood.recallable_dimmer, 2.2)

        # animation
        value *= self.read_pattern(patterns.octostrip[self.mood.pattern])

        # map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        mapping = OctostripBar.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        return list(vars(mapping).values())
