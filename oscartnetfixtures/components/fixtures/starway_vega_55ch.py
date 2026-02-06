from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetdaemon.python_extensions.colors import colorize, hsl_to_rgbw
from oscartnetfixtures.components.color import Color

from oscartnetfixtures.python_extensions.math import map_to_int


class StarwayVega55ch(BaseFixture):

    @dataclass
    class Mapping:
        dimmer: int = 0

        ring_ext_1_r: int = 0
        ring_ext_1_g: int = 0
        ring_ext_1_b: int = 0
        ring_ext_2_r: int = 0
        ring_ext_2_g: int = 0
        ring_ext_2_b: int = 0
        ring_ext_3_r: int = 0
        ring_ext_3_g: int = 0
        ring_ext_3_b: int = 0
        ring_ext_4_r: int = 0
        ring_ext_4_g: int = 0
        ring_ext_4_b: int = 0
        ring_ext_5_r: int = 0
        ring_ext_5_g: int = 0
        ring_ext_5_b: int = 0
        ring_ext_6_r: int = 0
        ring_ext_6_g: int = 0
        ring_ext_6_b: int = 0
        ring_ext_7_r: int = 0
        ring_ext_7_g: int = 0
        ring_ext_7_b: int = 0
        ring_ext_8_r: int = 0
        ring_ext_8_g: int = 0
        ring_ext_8_b: int = 0
        ring_ext_strobe: int = 0

        ring_int_1_r: int = 0
        ring_int_1_g: int = 0
        ring_int_1_b: int = 0
        ring_int_2_r: int = 0
        ring_int_2_g: int = 0
        ring_int_2_b: int = 0
        ring_int_3_r: int = 0
        ring_int_3_g: int = 0
        ring_int_3_b: int = 0
        ring_int_4_r: int = 0
        ring_int_4_g: int = 0
        ring_int_4_b: int = 0
        ring_int_5_r: int = 0
        ring_int_5_g: int = 0
        ring_int_5_b: int = 0
        ring_int_6_r: int = 0
        ring_int_6_g: int = 0
        ring_int_6_b: int = 0
        ring_int_7_r: int = 0
        ring_int_7_g: int = 0
        ring_int_7_b: int = 0
        ring_int_8_r: int = 0
        ring_int_8_g: int = 0
        ring_int_8_b: int = 0
        ring_int_strobe: int = 0

        center_warm_white: int = 0
        center_amber: int = 0

        backlight_warm_white: int = 0

        center_strobe : int = 0

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
            self._mapping.ring_ext_strobe = 150
            self._mapping.ring_int_strobe = 150
            self._mapping.center_strobe = 150

        self._lightness = 1.0 if mood.on_white else 0.5

    def _color(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call before _strobe_and_white
        """
        hue = Color.get_hue_from_palette(mood, group_info)
        r, g, b, w = hsl_to_rgbw(hue, 1.0, self._lightness)

        self._mapping.ring_ext_1_r = map_to_int(r, max_=self._mapping.ring_ext_1_r)
        self._mapping.ring_ext_1_g = map_to_int(g, max_=self._mapping.ring_ext_1_g)
        self._mapping.ring_ext_1_b = map_to_int(b, max_=self._mapping.ring_ext_1_b)
        self._mapping.ring_ext_2_r = map_to_int(r, max_=self._mapping.ring_ext_2_r)
        self._mapping.ring_ext_2_g = map_to_int(g, max_=self._mapping.ring_ext_2_g)
        self._mapping.ring_ext_2_b = map_to_int(b, max_=self._mapping.ring_ext_2_b)
        self._mapping.ring_ext_3_r = map_to_int(r, max_=self._mapping.ring_ext_3_r)
        self._mapping.ring_ext_3_g = map_to_int(g, max_=self._mapping.ring_ext_3_g)
        self._mapping.ring_ext_3_b = map_to_int(b, max_=self._mapping.ring_ext_3_b)
        self._mapping.ring_ext_4_r = map_to_int(r, max_=self._mapping.ring_ext_4_r)
        self._mapping.ring_ext_4_g = map_to_int(g, max_=self._mapping.ring_ext_4_g)
        self._mapping.ring_ext_4_b = map_to_int(b, max_=self._mapping.ring_ext_4_b)
        self._mapping.ring_ext_5_r = map_to_int(r, max_=self._mapping.ring_ext_5_r)
        self._mapping.ring_ext_5_g = map_to_int(g, max_=self._mapping.ring_ext_5_g)
        self._mapping.ring_ext_5_b = map_to_int(b, max_=self._mapping.ring_ext_5_b)
        self._mapping.ring_ext_6_r = map_to_int(r, max_=self._mapping.ring_ext_6_r)
        self._mapping.ring_ext_6_g = map_to_int(g, max_=self._mapping.ring_ext_6_g)
        self._mapping.ring_ext_6_b = map_to_int(b, max_=self._mapping.ring_ext_6_b)
        self._mapping.ring_ext_7_r = map_to_int(r, max_=self._mapping.ring_ext_7_r)
        self._mapping.ring_ext_7_g = map_to_int(g, max_=self._mapping.ring_ext_7_g)
        self._mapping.ring_ext_7_b = map_to_int(b, max_=self._mapping.ring_ext_7_b)
        self._mapping.ring_ext_8_r = map_to_int(r, max_=self._mapping.ring_ext_8_r)
        self._mapping.ring_ext_8_g = map_to_int(g, max_=self._mapping.ring_ext_8_g)
        self._mapping.ring_ext_8_b = map_to_int(b, max_=self._mapping.ring_ext_8_b)

        self._mapping.ring_int_1_r = map_to_int(r, max_=self._mapping.ring_int_1_r)
        self._mapping.ring_int_1_g = map_to_int(g, max_=self._mapping.ring_int_1_g)
        self._mapping.ring_int_1_b = map_to_int(b, max_=self._mapping.ring_int_1_b)
        self._mapping.ring_int_2_r = map_to_int(r, max_=self._mapping.ring_int_2_r)
        self._mapping.ring_int_2_g = map_to_int(g, max_=self._mapping.ring_int_2_g)
        self._mapping.ring_int_2_b = map_to_int(b, max_=self._mapping.ring_int_2_b)
        self._mapping.ring_int_3_r = map_to_int(r, max_=self._mapping.ring_int_3_r)
        self._mapping.ring_int_3_g = map_to_int(g, max_=self._mapping.ring_int_3_g)
        self._mapping.ring_int_3_b = map_to_int(b, max_=self._mapping.ring_int_3_b)
        self._mapping.ring_int_4_r = map_to_int(r, max_=self._mapping.ring_int_4_r)
        self._mapping.ring_int_4_g = map_to_int(g, max_=self._mapping.ring_int_4_g)
        self._mapping.ring_int_4_b = map_to_int(b, max_=self._mapping.ring_int_4_b)
        self._mapping.ring_int_5_r = map_to_int(r, max_=self._mapping.ring_int_5_r)
        self._mapping.ring_int_5_g = map_to_int(g, max_=self._mapping.ring_int_5_g)
        self._mapping.ring_int_5_b = map_to_int(b, max_=self._mapping.ring_int_5_b)
        self._mapping.ring_int_6_r = map_to_int(r, max_=self._mapping.ring_int_6_r)
        self._mapping.ring_int_6_g = map_to_int(g, max_=self._mapping.ring_int_6_g)
        self._mapping.ring_int_6_b = map_to_int(b, max_=self._mapping.ring_int_6_b)
        self._mapping.ring_int_7_r = map_to_int(r, max_=self._mapping.ring_int_7_r)
        self._mapping.ring_int_7_g = map_to_int(g, max_=self._mapping.ring_int_7_g)
        self._mapping.ring_int_7_b = map_to_int(b, max_=self._mapping.ring_int_7_b)
        self._mapping.ring_int_8_r = map_to_int(r, max_=self._mapping.ring_int_8_r)
        self._mapping.ring_int_8_g = map_to_int(g, max_=self._mapping.ring_int_8_g)
        self._mapping.ring_int_8_b = map_to_int(b, max_=self._mapping.ring_int_8_b)
