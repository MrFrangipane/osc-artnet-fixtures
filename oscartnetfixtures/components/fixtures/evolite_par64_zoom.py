from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetfixtures.python_extensions.math import map_to_int


class EvolitePar64Zoom(BaseFixture):

    @dataclass
    class Mapping:
        dimmer: int = 0
        strobe: int = 0
        zoom: int = 0

    def __init__(self, address=None):
        super().__init__(address)

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        self.apply_pattern_while_playing(group_info)

        self._mapping.dimmer = map_to_int(
            mood.master_dimmer * mood.recallable_dimmer * dimmer_value * (float(self._mapping.dimmer) / 255.0)
        )
