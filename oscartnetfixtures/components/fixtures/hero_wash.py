from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetdaemon.python_extensions.colors import colorize, hsl_to_rgbw
from oscartnetfixtures.components.color import Color

from oscartnetfixtures.python_extensions.math import map_to_int


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

        """
        self._mapping.zoom = {
            0: 255,
            1: 100,
            2: 0
        }[mood.beam_shape]
        """

    def _strobe_and_white(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call after color wheel
        """
        if mood.on_strobe:
            self._mapping.strobe = 235

        self._lightness = 1.0 if mood.on_white else 0.5

    def _color(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call before _strobe_and_white
        """
        hue = Color.get_hue_from_palette(mood, group_info)
        r, g, b, w = hsl_to_rgbw(hue, 1.0, self._lightness)

        self._mapping.red_1 = colorize(self._mapping.red_1, mood.colorize_wash, r)
        self._mapping.green_1 = colorize(self._mapping.green_1, mood.colorize_wash, g)
        self._mapping.blue_1 = colorize(self._mapping.blue_1, mood.colorize_wash, b)
        self._mapping.white_1 = colorize(self._mapping.white_1, mood.colorize_wash, w)

        self._mapping.red_2 = colorize(self._mapping.red_2, mood.colorize_wash, r)
        self._mapping.green_2 = colorize(self._mapping.green_2, mood.colorize_wash, g)
        self._mapping.blue_2 = colorize(self._mapping.blue_2, mood.colorize_wash, b)
        self._mapping.white_2 = colorize(self._mapping.white_2, mood.colorize_wash, w)

        self._mapping.red_3 = colorize(self._mapping.red_3, mood.colorize_wash, r)
        self._mapping.green_3 = colorize(self._mapping.green_3, mood.colorize_wash, g)
        self._mapping.blue_3 = colorize(self._mapping.blue_3, mood.colorize_wash, b)
        self._mapping.white_3 = colorize(self._mapping.white_3, mood.colorize_wash, w)
