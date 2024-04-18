import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int


class OctostripBar(BaseFixture):
    desaturate_threshold = 0.5

    @dataclass
    class Mapping:
        rainbow: int = 0
        red: int = 0
        green: int = 0
        blue: int = 0
        strobe: int = 0  # 1-20 Hz
        chase: int = 0  # sound active 241-255

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        # Color
        hue = self.mood.palette

        if self.mood.blinking > self.desaturate_threshold:
            saturation = 1.0 - (self.mood.blinking - self.desaturate_threshold) / (1 - self.desaturate_threshold)
        else:
            saturation = 1.0

        value = math.pow(self.mood.master_dimmer * self.mood.recallable_dimmer, 2.2)

        # Animation
        value *= self.read_pattern(
            table=patterns.octostrip[self.mood.pattern],
            time_scale=[0.25, 0.5, 1.0, 2.0, 4.0][self.mood.bpm_scale]
        )
        value *= group_dimmer

        strobe = 0
        if self.mood.blinking > 0.7:
            strobe = (self.mood.blinking - 0.5) * 2.0

        # Map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        mapping = self.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)
        if strobe:
            mapping.strobe = map_to_int(strobe, 128, 255)

        return list(vars(mapping).values())
