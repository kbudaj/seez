from haps import Inject

from seez.domain.models import Car, Make
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import CarRepository, MakeRepository


class GetCarCommand(BaseCommand):
    # pk: CarPk
    car_repository: CarRepository = Inject()
    make_repository: MakeRepository = Inject()

    @transactional
    def handle(self) -> Car:
        make = Make.create_new("abuse")
        self.make_repository.add(make)
        return self.make_repository.get_by_pk(pk=make.pk)
        # return self.car_repository.get_by_pk(pk=self.pk)
