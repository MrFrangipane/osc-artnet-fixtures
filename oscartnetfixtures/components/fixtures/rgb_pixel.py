import colorsys
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from oscartnetfixtures.python_extensions.math import map_to_int


class RGBPixel(BaseFixture):

    @dataclass
    class Mapping:
        red: int = 0
        green: int = 0
        blue: int = 0

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo) -> list[int]:
        #
        # Hue
        hue = mood.hue

        if mood.palette == 1 and group_info.place == 1:  # FIXME we implicitly know there are two pixels
            hue += 0.5

        if mood.palette == 2 and group_info.place == 1:  # FIXME we implicitly know there are two pixels
            hue += 0.33

        elif mood.palette == 4:
            hue += group_info.position * 0.5 - 0.25

        # Map
        if mood.on_white:
            lightness = 1.0
        else:
            lightness = 0.5

        r, g, b = colorsys.hls_to_rgb(hue, lightness, 1.0)
        return [
            map_to_int(r),
            map_to_int(g),
            map_to_int(b)
        ]
