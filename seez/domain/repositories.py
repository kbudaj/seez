from abc import abstractmethod
from typing import List, Optional

from haps import base

from seez.infrastructure.repositories import Repository

from seez.domain.models import Car, CarPk


@base
class CarRepository(Repository[CarPk, Car]):
    @abstractmethod
    def get_by_pk(self, pk: CarPk) -> Optional[Car]:
        pass

    @abstractmethod
    def get_all(self) -> List[Car]:
        pass

    @abstractmethod
    def add(self, car: Car) -> None:
        pass
