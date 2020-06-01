from haps import Inject

from seez.domain.dto import CarListDTO
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import CarRepository


class GetCarsPaged(BaseCommand):
    car_repository: CarRepository = Inject()

    page_number: int = 1
    page_size: int = 1

    @transactional
    def handle(self) -> CarListDTO:
        cars = self.car_repository.get_active_paged(
            page_number=self.page_number, page_size=self.page_size
        )
        return CarListDTO.from_model(cars)
