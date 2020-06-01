from dataclasses import dataclass
from uuid import uuid4

from seez.aliases import CarPk

from seez.infrastructure.models import AggregateRoot


@dataclass(unsafe_hash=False, eq=False)
class Car(AggregateRoot):
    pk: CarPk
    title: str

    @classmethod
    def next_pk(cls) -> CarPk:
        return CarPk(uuid4())

    @classmethod
    def create_new(cls, title: str) -> "Car":
        return cls(pk=cls.next_pk(), title=title)
