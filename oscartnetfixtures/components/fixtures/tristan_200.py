import logging
import time
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.components.pattern_store.api import PatternStoreAPI

from oscartnetfixtures.python_extensions.math import map_to_int

_logger = logging.getLogger(__name__)


class Tristan200(BaseFixture):
    @dataclass
    class Mapping:
        pan: int = 0
        pan_fine: int = 0
        tilt: int = 0
        tilt_fine: int = 0
        moving_speed: int = 0
        color: int = 0
        gobo1: int = 0
        gobo1_rotation: int = 0
        gobo2: int = 0
        prism: int = 0
        prism_rotation: int = 0
        frost: int = 0
        focus: int = 0
        focus_fine: int = 0
        shutter: int = 0
        dimmer: int = 0
        dimmer_fine: int = 0
        reset: int = 0

    def __init__(self, address=None):
        super().__init__(address)
        self._mapping = Tristan200.Mapping()

        self._dim_factor = 1.0
        self._elapsed = 0
        self._previous_color = 0
        self._symmetry = 0
        self._wheels_blackout_timestamp = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        self._elapsed += 0.1
        self._symmetry = (self.group_position * 2.0) - 1.0

        self._mapping = self.Mapping()

        pattern_step = PatternStoreAPI.get_step_while_playing(fixture_type=self.__class__.__name__, group_place=self.group_place)
        for parameter, value in pattern_step.items():
            setattr(self._mapping, parameter, value)

        self._color_wheel()
        self._beam()
        self._strobe_and_white()

        self._mapping.dimmer = map_to_int(
            self.mood.master_dimmer * self.mood.recallable_dimmer * self._dim_factor * group_dimmer
        )
        self._poll_for_wheels_blackout()

        if self.mood.on_lyre == 0:
            self._mapping.dimmer = 0

        return list(vars(self._mapping).values())

    def _beam(self):
        if self.mood.texture > .66:
            self._mapping.focus = 255
            self._mapping.gobo2 = 11
            self._dim_factor = 1.0

        elif self.mood.texture > .33:
            self._mapping.focus = 255
            self._mapping.gobo1 = 28
            self._mapping.prism = 26
            self._mapping.frost = 34
            self._mapping.prism_rotation = 179 + int(self.group_position * 27)
            self._dim_factor = 0.6

        else:
            self._mapping.prism = 26
            self._mapping.frost = 144
            self._dim_factor = 0.4

    def _strobe_and_white(self):
        """
        Call after color wheel
        """
        if self.mood.on_white:
            self._mapping.color = 64  # open

        if self.mood.on_strobe:
            self._mapping.shutter = 124  # 100 ou 124

    def _color_wheel(self):
        """
        Call before strobe_and_white()
        """
        mapping = [
            [0.0, .03, 66],  # red
            [.03, .05, 67],  # red/orange
            [.05, .07, 68],  # orange
            [.07, .10, 69],  # orange/yellow
            [.10, .14, 70],  # yellow
            [.14, .22, 71],  # yellow/green
            [.22, .37, 72],  # green
            [.37, .55, 78],  # blue
            [.55, .71, 74],  # cyan
            # [.71, .75, 76],  # magenta
            [.71, .98, 80],  # pink
            # 73
            # 75
            # 77
            # 79
            [.98, 1.0, 66]   # red
        ]

        hue = self.mood.hue
        if self.mood.palette == 1 and self.group_place == 1:
            hue += 0.5
            hue = hue % 1.0

        if self.mood.palette == 3:
            hue += 0.5
            hue = hue % 1.0

        for min_, max_, value in mapping:
            if min_ <= hue <= max_:
                self._mapping.color = value
                return

        self._mapping.color = 128  # fast wheel rotation to warn operator something's wrong

    def _poll_for_wheels_blackout(self):
        """
        Blacks out for a short period of time while wheels are turning
        Call right before returning mapped channels
        """
        distance = abs(self._previous_color - self._mapping.color)
        if distance > 0:
            self._previous_color = self._mapping.color
            if distance > 1:
                self._wheels_blackout_timestamp = time.time()

        if time.time() - self._wheels_blackout_timestamp < 0.2:
            self._mapping.dimmer = 0
