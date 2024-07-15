import logging
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int, p_cos


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
        self._elapsed = 0
        self._symmetry = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        if self.mood.on_octo == 0:
            return [0] * 26

        self._dim_factor = 1.0
        self._elapsed += 0.1
        self._symmetry = (self.group_position * 2.0) - 1.0

        self._mapping = self.Mapping()
        self._blinking()
        self._color()
        self._beam()
        self._animation()

        self._mapping.dimmer = map_to_int(
            self.mood.master_dimmer * self.mood.recallable_dimmer * self._dim_factor * group_dimmer
        )
        return list(vars(self._mapping).values())

    def _beam(self):
        self._mapping.zoom = map_to_int(self.mood.texture)

    def _animation(self):
        time_scale = [1.0, 1.0, 1.0, 2.0, 2.0][self.mood.bpm_scale]

        pan, dim = self.read_pattern(
            table=patterns.tristan200_pan[self.mood.pattern],
            time_scale=time_scale
        )
        self._dim_factor *= dim

        tilt, dim = self.read_pattern(
            table=patterns.tristan200_tilt[self.mood.pattern],
            time_scale=time_scale
        )
        self._dim_factor *= dim

        self._mapping.pan = map_to_int(pan, 87,172)
        self._mapping.tilt = map_to_int(tilt, 0,72)

    def _blinking(self):
        """
        Call after color wheel
        """
        if self.mood.blinking > 0.65:
            self._mapping.strobe = 235

        if self.mood.blinking > 0.80:
            self._lightness = 0.5 + (self.mood.blinking - 0.8) * 2.5
            self._mapping.strobe = 245

    def _color(self):
        """
        Call before blinking
        """
        hue = self.mood.hue
        if self.mood.palette == 3:
            hue += 0.5
            hue = hue % 1.0

        r, g, b, w = hsl_to_rgbw(hue, 1.0, self._lightness)

        self._mapping.red_1 = int(r * 255)
        self._mapping.green_1 = int(g * 255)
        self._mapping.blue_1 = int(b * 255)
        self._mapping.white_1 = int(w * 255)

        self._mapping.red_2 = int(r * 255)
        self._mapping.green_2 = int(g * 255)
        self._mapping.blue_2 = int(b * 255)
        self._mapping.white_2 = int(w * 255)

        self._mapping.red_3 = int(r * 255)
        self._mapping.green_3 = int(g * 255)
        self._mapping.blue_3 = int(b * 255)
        self._mapping.white_3 = int(w * 255)
