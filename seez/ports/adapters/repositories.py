from typing import List, Optional
from uuid import UUID

from haps import Inject, egg

from seez.infrastructure.session import Session

from seez.domain.models import Car
from seez.domain.repositories import CarRepository


@egg
class SqlAlchemyCarRepository(CarRepository):
    session: Session = Inject()

    def get_by_pk(self, pk: UUID) -> Optional[Car]:
        return self.session.query(Car).filter(Car.pk == pk).one()

    def get_all(self) -> List[Car]:
        return list(self.session.query(Car).all())

    def add(self, car: Car) -> None:
        self.session.add(car)
        self.session.flush()
