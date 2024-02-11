from dataclasses import dataclass
import colorsys

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood

from oscartnetfixtures.python_extensions.math import map_to_int


class OctostripBar(BaseFixture):
    @dataclass
    class Mapping:
        rainbow: int = 0
        red: int = 0
        green: int = 0
        blue: int = 0
        strobe: int = 0  # 1-20 Hz
        chase: int = 0  # sound active 241-255

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        offset = ((group_position * 2) - 1) * mood.animation * 0.5
        hue = (mood.palette + offset) % 1.0
        red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        mapping = OctostripBar.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        return list(vars(mapping).values())
