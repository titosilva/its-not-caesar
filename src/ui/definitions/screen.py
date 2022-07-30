from abc import ABC, abstractmethod
from typing import List
from ui.definitions.device import Device

from ui.definitions.renderable import Renderable


class Screen(ABC):
    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        pass
    