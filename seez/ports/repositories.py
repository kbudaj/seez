from abc import abstractmethod
from typing import List, Optional

from haps import base

from seez.domain.models import Car, CarPk
from seez.infrastructure.repositories import Repository


@base
class CarRepository(Repository):
    @abstractmethod
    def get_by_pk(self, pk: CarPk) -> Optional[Car]:
        pass

    @abstractmethod
    def get_all(self) -> List[Car]:
        pass

    @abstractmethod
    def add(self, car: Car) -> None:
        pass
