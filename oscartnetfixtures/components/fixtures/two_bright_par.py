import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood

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

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        # color
        offset = 0  # ((group_position * 2) - 1) * mood.animation * 0.5
        hue = (mood.palette + offset) % 1.0
        saturation = 1.0 - (mood.blinking - self.desaturate_threshold) / self.desaturate_threshold \
            if mood.blinking > self.desaturate_threshold else 1.0
        value = math.pow(mood.master_dimmer * mood.recallable_dimmer, 2.2)
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)

        # animation
        pass

        # map
        mapping = TwoBrightPar.Mapping()
        mapping.red = map_to_int(red * mood.blinking * .5)
        mapping.green = map_to_int(green * mood.blinking * .5)
        mapping.blue = map_to_int(blue * mood.blinking * .5)

        return list(vars(mapping).values())
