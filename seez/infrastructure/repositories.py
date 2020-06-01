from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from seez.aliases import T, TEntity


class ReadOnlyRepository(ABC, Generic[T, TEntity]):
    """Generic Read Only Repository"""

    @abstractmethod
    def get_by_pk(self, pk: T) -> Optional[TEntity]:
        pass

    @abstractmethod
    def get_all(self) -> List[TEntity]:
        pass


class Repository(ReadOnlyRepository[T, TEntity]):
    """Generic Repository Interface"""

    @abstractmethod
    def add(self, entity: TEntity) -> None:
        pass
