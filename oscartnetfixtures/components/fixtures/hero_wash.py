import logging
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw

from oscartnetfixtures.python_extensions.math import map_to_int

_logger = logging.getLogger(__name__)


class HeroWash(BaseFixture):

    @dataclass
    class Mapping:
        pan: int = 0
        pan_fine: int = 0
        tilt: int = 0
        tilt_fine: int = 0
        moving_speed: int = 0
        zoom: int = 0
        dimmer: int = 0
        strobe: int = 0
        red_1: int = 0
        green_1: int = 0
        blue_1: int = 0
        white_1: int = 0
        red_2: int = 0
        green_2: int = 0
        blue_2: int = 0
        white_2: int = 0
        red_3: int = 0
        green_3: int = 0
        blue_3: int = 0
        white_3: int = 0
        color_temperature: int = 0
        colr_macro: int = 0
        segment_pattern: int = 0
        segment_pattern_transition_speed: int = 0
        zoom_auto_patter: int = 0
        pan_tilt_auto_pattern: int = 0

    def __init__(self, address=None):
        super().__init__(address)
        self._mapping.dimmer = 255
        self._lightness = 0.5
        self._symmetry = 0

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        self.apply_pattern_while_playing(group_info)

        self._symmetry = (group_info.position * 2.0) - 1.0
        self._strobe_and_white(mood, group_info)
        self._color(mood, group_info)
        self._mapping.dimmer = map_to_int(
            mood.master_dimmer * mood.recallable_dimmer * dimmer_value * (float(self._mapping.dimmer) / 255.0)
        )

        if mood.on_wash == 0:
            self._mapping.dimmer = 0

    def _strobe_and_white(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call after color wheel
        """
        if mood.on_strobe:
            self._mapping.strobe = 235

        self._lightness = 1.0 if mood.on_white else 0.5

    def _color(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call before color_and_white
        """
        hue = mood.hue
        if mood.palette == 1 and group_info.place == 1:
            hue += 0.5
            hue = hue % 1.0

        if mood.palette == 3:
            hue += 0.5
            hue = hue % 1.0

        r, g, b, w = hsl_to_rgbw(hue, 1.0, self._lightness)

        self._mapping.red_1 = int(r * self._mapping.red_1)
        self._mapping.green_1 = int(g * self._mapping.green_1)
        self._mapping.blue_1 = int(b * self._mapping.blue_1)
        self._mapping.white_1 = int(w * self._mapping.white_1)

        self._mapping.red_2 = int(r * self._mapping.red_2)
        self._mapping.green_2 = int(g * self._mapping.green_2)
        self._mapping.blue_2 = int(b * self._mapping.blue_2)
        self._mapping.white_2 = int(w * self._mapping.white_2)

        self._mapping.red_3 = int(r * self._mapping.red_3)
        self._mapping.green_3 = int(g * self._mapping.green_3)
        self._mapping.blue_3 = int(b * self._mapping.blue_3)
        self._mapping.white_3 = int(w * self._mapping.white_3)
