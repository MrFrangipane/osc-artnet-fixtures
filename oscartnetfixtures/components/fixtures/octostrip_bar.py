import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetdaemon.python_extensions.colors import colorize
from oscartnetfixtures.components.color import Color


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

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        if mood.on_octo == 0:
            self._mapping = self.Mapping()
            return

        self.apply_pattern_while_playing(group_info)
        self._color(mood, dimmer_value, group_info)

        if mood.on_strobe:
            self._mapping.strobe = 251

    def _color(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):

        hue = Color.get_hue_from_palette(mood, group_info)
        value = math.pow(dimmer_value * mood.master_dimmer * mood.recallable_dimmer, 2.2)
        saturation = 1.0 - mood.on_white

        # Map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        self._mapping.red = colorize(self._mapping.red, mood.colorize_octo, red)
        self._mapping.green = colorize(self._mapping.green, mood.colorize_octo, green)
        self._mapping.blue = colorize(self._mapping.blue, mood.colorize_octo, blue)
