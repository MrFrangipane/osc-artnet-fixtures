import time
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetfixtures.components.color import Color

from oscartnetfixtures.python_extensions.math import map_to_int


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

        self._elapsed = 0
        self._previous_color = 0
        self._symmetry = 0
        self._wheels_blackout_timestamp = 0

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        self.apply_pattern_while_playing(group_info)

        self._elapsed += 0.1
        self._symmetry = (group_info.position * 2.0) - 1.0
        self._color_wheel(mood, group_info)
        self._strobe_and_white(mood, group_info)
        self._mapping.dimmer = map_to_int(
            mood.master_dimmer * mood.recallable_dimmer * dimmer_value * (float(self._mapping.dimmer) / 255.0)
        )

        """
        if mood.beam_shape == 0:
            self._mapping.gobo2 = 11
            self._mapping.focus = 255
            self._mapping.prism = 0
            self._mapping.frost = 0

        elif mood.beam_shape == 1:
            self._mapping.gobo2 = 0
            self._mapping.focus = 0
            self._mapping.prism = 0
            self._mapping.frost = 40

        elif mood.beam_shape == 2:
            self._mapping.gobo2 = 0
            self._mapping.focus = 0
            self._mapping.prism = 21
            self._mapping.frost = 40
        """

        if mood.on_lyre == 0:
            self._mapping.dimmer = 0

        self._poll_for_wheels_blackout()

    def _strobe_and_white(self, mood: Mood, group_info: ShowItemGroupInfo):
        """
        Call after color wheel
        """
        if mood.on_white or mood.colorize_lyre < 0.5:
            self._mapping.color = 64  # open

        if mood.on_strobe:
            self._mapping.shutter = 124  # 100 ou 124

    def _color_wheel(self, mood: Mood, group_info: ShowItemGroupInfo):
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

        hue = Color.get_hue_from_palette(mood, group_info)

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
