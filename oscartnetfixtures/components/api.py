import importlib
import logging
import sys
from typing import Type

from oscartnetdaemon.core.fixture.base import BaseFixture

from oscartnetfixtures.components import patterns

from oscartnetfixtures.components.fixtures import hero_wash
from oscartnetfixtures.components.fixtures import octostrip_bar
from oscartnetfixtures.components.fixtures import rgb_pixel
from oscartnetfixtures.components.fixtures import spectrum500
from oscartnetfixtures.components.fixtures import tristan_200
from oscartnetfixtures.components.fixtures import two_bright_par


_logger = logging.getLogger(__name__)


class OSCArtnetFixturesAPI:

    @staticmethod
    def reload_definitions():
        _logger.info("Reloading fixtures and patterns definitions")

        importlib.reload(patterns)

        importlib.reload(hero_wash)
        importlib.reload(octostrip_bar)
        importlib.reload(rgb_pixel)
        importlib.reload(spectrum500)
        importlib.reload(tristan_200)
        importlib.reload(two_bright_par)

    @staticmethod
    def get_fixture(name) -> Type[BaseFixture]:
        classes = {cls.__name__: cls for cls in [
            hero_wash.HeroWash,
            octostrip_bar.OctostripBar,
            rgb_pixel.RGBPixel,
            spectrum500.AlgamSpectrum500RGB,
            tristan_200.Tristan200,
            two_bright_par.TwoBrightPar
        ]}
        return classes.get(name, None)
