import os.path

from oscartnetfixtures.core.components import Components


class Launcher:

    def __init__(self):
        Components().configuration.resources_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources"
        )

    def exec(self):
        pass
