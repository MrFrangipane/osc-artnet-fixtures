import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int


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

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        if self.mood.on_octo == 0:
            return [0] * 6

        #
        # hue
        hue = self.mood.hue

        if self.mood.palette == 1 and self.group_place % 2:
            hue += 0.5

        if self.mood.palette == 2 and self.group_place not in [0, self.group_size - 1]:
            hue += 0.33

        elif self.mood.palette == 4:
            hue += self.group_position * 0.5 - 0.25

        value = math.pow(self.mood.master_dimmer * self.mood.recallable_dimmer, 2.2)

        #
        # Animation
        pattern = patterns.octostrip[self.mood.pattern]
        
        value *= pattern.read_pattern(
            time_scale=[0.25, 0.5, 1.0, 2.0, 4.0][self.mood.bpm_scale],
            group_position=self.group_position,
            beat_counter=self.mood.beat_counter,
            parameter=self.mood.pattern_parameter,
            playmode=self.mood.pattern_playmode
        )
        
        value *= group_dimmer
        saturation = 1.0 - self.mood.on_white

        # Map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        mapping = self.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        if self.mood.on_strobe:
            mapping.strobe = 200

        return list(vars(mapping).values())
