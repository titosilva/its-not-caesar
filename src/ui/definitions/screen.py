from abc import ABC, abstractmethod
from typing import List
from ui.definitions.device import Device

from ui.definitions.renderable import Renderable


class Screen(ABC):
    @abstractmethod
    def get_content(self) -> Renderable:
        raise NotImplementedError()

    @abstractmethod
    def get_rendered_content(self) -> List[str]:
        raise NotImplementedError()
