import colorsys
import math
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

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

    def map_to_channels(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo) -> list[int]:
        if mood.on_octo == 0:
            return [0] * 6

        #
        # hue
        hue = mood.hue

        if mood.palette == 1 and group_info.place % 2:
            hue += 0.5

        if mood.palette == 2 and group_info.place not in [0, group_info.size - 1]:
            hue += 0.33

        elif mood.palette == 4:
            hue += group_info.position * 0.5 - 0.25

        value = math.pow(dimmer_value * mood.master_dimmer * mood.recallable_dimmer, 2.2)
        saturation = 1.0 - mood.on_white

        # Map
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        mapping = self.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        if mood.on_strobe:
            mapping.strobe = 200

        return list(vars(mapping).values())
