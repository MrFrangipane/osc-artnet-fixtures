import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int, p_cos


class TwoBrightPar(BaseFixture):
    desaturate_threshold = 0.75

    @dataclass
    class Mapping:
        red: int = 0
        green: int = 0
        blue: int = 0
        white: int = 0
        amber: int = 0
        uv: int = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        # Color
        hue = self.mood.palette

        if self.mood.blinking > self.desaturate_threshold:
            saturation = 1.2 - (self.mood.blinking - self.desaturate_threshold) / (1 - self.desaturate_threshold)
        else:
            saturation = 1.0

        value = math.pow(self.mood.master_dimmer * self.mood.recallable_dimmer, 2.2) * saturation
        value *= group_dimmer

        # Animation
        # value *= self.read_pattern(patterns.octostrip[self.mood.pattern])

        # Map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        mapping = self.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        return list(vars(mapping).values())
