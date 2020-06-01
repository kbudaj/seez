from abc import ABC
from typing import Any


class Entity(ABC):
    pk: Any

    def __eq__(self, other: Any) -> bool:
        return isinstance(self, other.__class__) and self.pk == other.pk

    def __hash__(self) -> int:
        return hash(self.pk)


class AggregateRoot(Entity):
    @classmethod
    def next_pk(cls) -> Any:
        raise NotImplementedError
