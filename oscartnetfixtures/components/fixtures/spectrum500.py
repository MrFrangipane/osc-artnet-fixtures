from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.python_extensions.math import map_to_int, p_cos
from oscartnetdaemon.python_extensions.colors import hsl_to_rgbw
from oscartnetdaemon.core.osc.two_bright_par import HSL  # fixme ?


class AlgamSpectrum500RGB(BaseFixture):
    desaturate_threshold = 0.75

    @dataclass
    class Mapping:
        on_off: int = 0  # 1-200=34ch  201-254=6ch 255=pattern_a off
        mode: int = 0  # auto, one scene
        pattern_library: int = 0
        figure_: int = 9  # NOT SIZE ?!  26 ?
        zoom_effect: int = 0
        speed_: int = 0
        horizontal_movement: int = 203
        vertical_movement: int = 0
        horizontal_zoom: int = 0
        vertical_zoom: int = 24
        color_mode: int = 8  # 0: original, 1+ : colors
        color: int = 58  # 2=original  10=red  18=yellow 26=green 34=cyan 42=blue 50=pink 58=white
        dot_line: int = 0  # 0=? 66=dots 130=lines
        progressive_draw: int = 0
        ch_15: int = 0
        ch_16: int = 0
        ch_17: int = 0
        pattern_b_on: int = 30
        ch_19: int = 0
        ch_20: int = 0
        ch_21: int = 0
        ch_22: int = 0
        ch_23: int = 0
        ch_24: int = 0
        ch_25: int = 0
        ch_26: int = 0
        ch_27: int = 0
        ch_28: int = 0
        ch_29: int = 0
        ch_30: int = 0
        ch_31: int = 0
        ch_32: int = 0
        ch_33: int = 0
        ch_34: int = 0

    def map_to_channels(self, group_dimmer: float) -> list[int]:

        mapping = self.Mapping()
        mapping.speed_ = map_to_int(self.mood.bpm_scale, 13, 128)

        if self.mood.blinking > .6:
            mapping.on_off = 1

        if self.mood.blinking > .8:
            mapping.on_off = int((self.mood.beat_counter * 4) % 1 > .5)

        return list(vars(mapping).values())
