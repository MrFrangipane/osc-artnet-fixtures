from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo

from logging import getLogger

_logger = getLogger(__name__)


class Color:

    @staticmethod
    def get_hue_from_palette(mood: Mood, group_info: ShowItemGroupInfo):
        hue = mood.hue

        # FIXME hacky, set a groupinfo index parameter in show
        group_index = {
            1: 1,
            2: 2,
            3: 4,
            4: 5,
            6: 7
        }[group_info.index]


        if mood.palette == 1 and group_info.place % 2 == 0:
            hue += 0.5

        elif mood.palette == 2 and group_info.place % 2 == 0:
            hue += 0.33

        elif mood.palette == 3 and group_index % 2 == 0:
            hue += 0.5

        elif mood.palette == 4:
            hue += (group_info.position * 0.5 - 0.25) % 1.0

        return hue % 1.0
