import colorsys
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.python_extensions.math import map_to_int


class RGBPixel(BaseFixture):

    @dataclass
    class Mapping:
        red: int = 0
        green: int = 0
        blue: int = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:
        #
        # Hue
        hue = self.mood.hue

        if self.mood.palette == 1 and self.group_place == 1:  # FIXME we implicitly know there are two pixels
            hue += 0.5

        if self.mood.palette == 2 and self.group_place == 1:  # FIXME we implicitly know there are two pixels
            hue += 0.33

        elif self.mood.palette == 4:
            hue += self.group_position * 0.5 - 0.25

        # Map
        if self.mood.on_white:
            lightness = 1.0
        else:
            lightness = 0.5

        r, g, b = colorsys.hls_to_rgb(hue, lightness, 1.0)
        return [
            map_to_int(r),
            map_to_int(g),
            map_to_int(b)
        ]
