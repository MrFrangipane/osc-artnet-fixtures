from dataclasses import dataclass

from oscartnetfixtures.core.configuration import Configuration
from oscartnetfixtures.python_extensions.singleton_metaclass import SingletonMetaclass


@dataclass
class Components(metaclass=SingletonMetaclass):
    configuration = Configuration()
