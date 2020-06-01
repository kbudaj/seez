from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCommand(ABC):
    def __init__(self, **kwargs: Any) -> None:
        for field in kwargs:
            setattr(self, field, kwargs[field])

    @abstractmethod
    def handle(self) -> Optional[Any]:
        pass
