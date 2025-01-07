import logging
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw

from oscartnetfixtures.python_extensions.math import map_to_int, p_cos


_logger = logging.getLogger(__name__)


class HeroWash(BaseFixture):

    MAX_RGBW = 128

    @dataclass
    class Mapping:
        pan: int = 0
        pan_fine: int = 0
        tilt: int = 0
        tilt_fine: int = 0
        moving_speed: int = 0
        zoom: int = 0
        dimmer: int = 255
        strobe: int = 255
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
        self._mapping: HeroWash.Mapping = HeroWash.Mapping()
        self._mapping.dimmer = 255

        self._lightness = 0.5

        self._dim_factor = 1.0
        self._symmetry = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        self._dim_factor = 1.0
        self._symmetry = (self.group_position * 2.0) - 1.0

        self._mapping = self.Mapping()

        # pattern_step = PatternStoreAPI.get_step(fixture_type=self.__class__.__name__, group_place=self.group_place)
        # for parameter, value in pattern_step.items():
        #     setattr(self._mapping, parameter, value)

        self._strobe_and_white()
        self._color()
        self._beam()

        if self.mood.pattern not in [2, 3]:
            self._mapping.dimmer = map_to_int(
                self.mood.master_dimmer * self.mood.recallable_dimmer * (1.0 - self._dim_factor) * group_dimmer
            )

        if self.mood.on_wash == 0:
            self._mapping.dimmer = 0

        return list(vars(self._mapping).values())

    def _beam(self):
        self._mapping.zoom = map_to_int(self.mood.texture)

    def _strobe_and_white(self):
        """
        Call after color wheel
        """
        if self.mood.on_strobe:
            self._mapping.strobe = 235

        self._lightness = 1.0 if self.mood.on_white else 0.5

    def _color(self):
        """
        Call before color_and_white
        """
        hue = self.mood.hue
        if self.mood.palette == 1 and self.group_place == 1:
            hue += 0.5
            hue = hue % 1.0

        if self.mood.palette == 3:
            hue += 0.5
            hue = hue % 1.0

        r, g, b, w = hsl_to_rgbw(hue, 1.0, self._lightness)

        self._mapping.red_1 = int(r * self.MAX_RGBW)
        self._mapping.green_1 = int(g * self.MAX_RGBW)
        self._mapping.blue_1 = int(b * self.MAX_RGBW)
        self._mapping.white_1 = int(w * self.MAX_RGBW)

        self._mapping.red_2 = int(r * self.MAX_RGBW)
        self._mapping.green_2 = int(g * self.MAX_RGBW)
        self._mapping.blue_2 = int(b * self.MAX_RGBW)
        self._mapping.white_2 = int(w * self.MAX_RGBW)

        self._mapping.red_3 = int(r * self.MAX_RGBW)
        self._mapping.green_3 = int(g * self.MAX_RGBW)
        self._mapping.blue_3 = int(b * self.MAX_RGBW)
        self._mapping.white_3 = int(w * self.MAX_RGBW)
