import logging
import time

from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood

from oscartnetfixtures.python_extensions.math import map_to_int, p_cos

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
        self.elapsed = 0

        self._mapping = Tristan200.Mapping()
        self._previous_color = 0
        self._previous_gobo1 = 0
        self._wheels_blackout_timestamp = 0

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        self.elapsed += mood.animation / 10.0
        sym = (group_position * 2.0) - 1.0

        self._mapping = Tristan200.Mapping()
        self._mapping.color = self._color_wheel(mood)

        if mood.texture > .66:
            self._mapping.focus = 255
            self._mapping.gobo2 = 11
            dim_factor = 1.0

        elif mood.texture > .33:
            self._mapping.focus = 255
            self._mapping.gobo1 = 28
            self._mapping.prism = 26
            self._mapping.frost = 34
            self._mapping.prism_rotation = 179 + int(group_position * 27)
            dim_factor = 0.6

        else:
            self._mapping.prism = 26
            self._mapping.frost = 144
            dim_factor = 0.4

        if mood.blinking > .7:
            self._mapping.shutter = 121

        elif mood.blinking < .3:
            dim_factor *= p_cos(mood.beat_counter * 6.28)

        pan = p_cos(mood.beat_counter + 1.57 * sym) * .3
        if .6 > mood.animation > .3:
            pan = 0.18  # roughly 45, centered

        self._mapping.pan = map_to_int(pan)
        self._mapping.tilt = 40
        self._mapping.dimmer = map_to_int(mood.master_dimmer * mood.recallable_dimmer * dim_factor * 0.5)

        self._poll_for_wheels_blackout()
        return list(vars(self._mapping).values())

    def _color_wheel(self, mood:Mood) -> int:
        if mood.blinking > 0.75:
            return 64  # open

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

        for min_, max_, value in mapping:
            if min_ <= mood.palette <= max_:
                distance = abs(self._previous_color - value)
                if distance > 0:
                    self._previous_color = value
                    if distance > 1:
                        self._start_wheels_blackout()

                return value

        return 128  # fast wheel rotation to debug

    def _start_wheels_blackout(self):
        """
        Blacks out for a short period of time while wheels are turning
        Call whenever you change a parameter associated with a wheel
        """
        self._wheels_blackout_timestamp = time.time()

    def _poll_for_wheels_blackout(self):
        """
        Blacks out for a short period of time while wheels are turning
        Call right before returning mapped channels
        """
        if time.time() - self._wheels_blackout_timestamp < 0.2:
            self._mapping.dimmer = 0

