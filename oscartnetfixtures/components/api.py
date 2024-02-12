import importlib
import logging
import sys
from typing import Type

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns
from oscartnetfixtures.components.fixtures import octostrip_bar
from oscartnetfixtures.components.fixtures import tristan_200
from oscartnetfixtures.components.fixtures import two_bright_par

_logger = logging.getLogger(__name__)


class OSCArtnetFixturesAPI:

    @staticmethod
    def reload_definitions():
        _logger.info("Reloading fixtures and patterns definitions")
        importlib.reload(patterns)
        importlib.reload(octostrip_bar)
        importlib.reload(tristan_200)
        importlib.reload(two_bright_par)

    @staticmethod
    def get_fixture(name) -> Type[BaseFixture]:
        return {
            'OctostripBar': octostrip_bar.OctostripBar,
            'Tristan200': tristan_200.Tristan200,
            'TwoBrightPar': two_bright_par.TwoBrightPar
        }.get(name, None)
