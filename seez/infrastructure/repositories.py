from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ReadOnlyRepository(ABC):
    """Generic Read Only Repository"""

    @abstractmethod
    def get_by_pk(self, pk: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        pass


class Repository(ReadOnlyRepository):
    """Generic Repository Interface"""

    @abstractmethod
    def add(self, entity: Any) -> None:
        pass
