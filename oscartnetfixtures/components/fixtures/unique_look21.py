from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo


class UniqueLook21(BaseFixture):

    @dataclass
    class Mapping:
        pump: int = 0
        fan: int = 0

    def __init__(self, address=None):
        super().__init__(address)

    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo):
        self.apply_pattern_while_playing(group_info)

        if mood.on_smoke == 0:
            self._mapping = self.Mapping()
