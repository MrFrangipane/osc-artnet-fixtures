import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetdaemon.python_extensions.colors import colorize, hsl_to_rgbw
from oscartnetfixtures.components.color import Color


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
        hue = Color.get_hue_from_palette(mood, group_info)
        lightness = math.pow(dimmer_value * mood.master_dimmer * mood.recallable_dimmer, 2.2)

        saturation = 1.0
        if mood.on_white:
            saturation = 0

        # Map
        r, g, b, w = hsl_to_rgbw(hue, saturation, lightness * 0.5)
        self._mapping.red = colorize(self._mapping.red, mood.colorize_par, r)
        self._mapping.green = colorize(self._mapping.green, mood.colorize_par, g)
        self._mapping.blue = colorize(self._mapping.blue, mood.colorize_par, b)
        self._mapping.white = colorize(self._mapping.white, mood.colorize_par, w)
        self._mapping.amber = colorize(self._mapping.amber * dimmer_value, mood.colorize_par, 0)
        self._mapping.uv = colorize(self._mapping.uv * dimmer_value, mood.colorize_par, 0)
