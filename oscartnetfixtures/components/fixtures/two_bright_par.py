import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetfixtures.python_extensions.math import map_to_int, p_cos
from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw
from oscartnetdaemon.core.osc.two_bright_par import HSL  # fixme ?


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

    def map_from_hsl(self, hsl: HSL) -> list[int]:
        r, g, b, w = hsl_to_rgbw(hsl.h, hsl.s, hsl.l)
        mapping = self.Mapping()
        mapping.red = int(r * 255)
        mapping.green = int(g * 255)
        mapping.blue = int(b * 255)
        mapping.white = int(w * 255)

        return list(vars(mapping).values())

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo) -> list[int]:
        if mood.on_par == 0:
            return [0] * 6

        #
        # Hue
        hue = mood.hue

        if mood.palette == 1 and group_info.place in [0, group_info.size - 1]:
            hue += 0.5

        if mood.palette == 2 and group_info.place not in [0, group_info.size - 1]:
            hue += 0.33

        elif mood.palette == 4:
            hue += group_info.position * 0.5 - 0.25

        #
        # Saturation
        lightness = math.pow(mood.master_dimmer * mood.recallable_dimmer * dimmer_value * 0.5, 2.2)
        if mood.on_white:
            lightness = 1.0

        # Animation
        # value *= self.read_pattern(patterns.octostrip[self.mood.pattern])

        # Map
        return self.map_from_hsl(
            HSL(hue, 1.0, lightness)
        )
