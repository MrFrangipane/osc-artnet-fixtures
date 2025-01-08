import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw


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

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        if mood.on_par == 0:
            self._mapping = self.Mapping()
            return

        self.apply_pattern_while_playing(group_info)
        self._color(mood, dimmer_value, group_info)

        # TODO : strobe

    def _color(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        hue = mood.hue
        if mood.palette == 1 and group_info.place % 2:
            hue += 0.5

        if mood.palette == 2 and group_info.place not in [0, group_info.size - 1]:
            hue += 0.33

        elif mood.palette == 4:
            hue += group_info.position * 0.5 - 0.25

        lightness = math.pow(dimmer_value * mood.master_dimmer * mood.recallable_dimmer, 2.2)

        saturation = 1.0
        if mood.on_white:
            saturation = 0

        # Map
        r, g, b, w = hsl_to_rgbw(hue, saturation, lightness * 0.5)
        self._mapping.red = int(self._mapping.red * r)
        self._mapping.green = int(self._mapping.green * g)
        self._mapping.blue = int(self._mapping.blue * b)
        self._mapping.white = int(self._mapping.white * w)
