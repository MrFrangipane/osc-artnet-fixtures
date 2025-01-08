import importlib
import logging
from typing import Type

from oscartnetdaemon.core.fixture.base import BaseFixture


_logger = logging.getLogger(__name__)


# FIXME : solve circular dependency between FixtureAPI (showStore) and Fixture (PatternAPI),
#  make this dynamic and text-based ?
class OSCArtnetFixturesAPI:
    hero_wash = None
    octostrip_bar = None
    tristan_200 = None
    two_bright_par = None

    @staticmethod
    def reload_definitions():
        _logger.info("Reloading fixtures and patterns definitions")

        from oscartnetfixtures.components.fixtures import hero_wash
        from oscartnetfixtures.components.fixtures import octostrip_bar
        from oscartnetfixtures.components.fixtures import tristan_200
        from oscartnetfixtures.components.fixtures import two_bright_par

        importlib.reload(hero_wash)
        importlib.reload(octostrip_bar)
        importlib.reload(tristan_200)
        importlib.reload(two_bright_par)

        OSCArtnetFixturesAPI.hero_wash = hero_wash
        OSCArtnetFixturesAPI.octostrip_bar = octostrip_bar
        OSCArtnetFixturesAPI.tristan_200 = tristan_200
        OSCArtnetFixturesAPI.two_bright_par = two_bright_par

    @staticmethod
    def get_fixture(name) -> Type[BaseFixture]:
        classes = {cls.__name__: cls for cls in [
            OSCArtnetFixturesAPI.hero_wash.HeroWash,
            OSCArtnetFixturesAPI.octostrip_bar.OctostripBar,
            OSCArtnetFixturesAPI.tristan_200.Tristan200,
            OSCArtnetFixturesAPI.two_bright_par.TwoBrightPar
        ]}
        return classes.get(name, None)
