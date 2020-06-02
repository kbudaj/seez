from typing import Optional

from haps import Inject

from seez.domain.dto import CarListDTO
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import CarRepository


class GetCarsPaged(BaseCommand):
    car_repository: CarRepository = Inject()

    page_number: int = 1
    page_size: int = 1

    price_min: Optional[int] = None
    price_max: Optional[int] = None
    mileage_min: Optional[int] = None
    mileage_max: Optional[int] = None

    @transactional
    def handle(self) -> CarListDTO:
        cars = self.car_repository.get_active_paged(
            page_number=self.page_number,
            page_size=self.page_size,
            price_min=self.price_min,
            price_max=self.price_max,
            mileage_min=self.mileage_min,
            mileage_max=self.mileage_max,
        )
        return CarListDTO.from_model(cars)
