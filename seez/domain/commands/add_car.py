from haps import Inject

from seez.domain.dto import AddCarDTO
from seez.domain.exceptions import ModelDoesNotExist, SubModelDoesNotExist
from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import (
    CarRepository,
    MakeRepository,
    ModelRepository,
    SubModelRepository,
)


class AddCar(BaseCommand):
    car_repository: CarRepository = Inject()
    make_repository: MakeRepository = Inject()
    model_repository: ModelRepository = Inject()
    submodel_repository: SubModelRepository = Inject()

    add_car_dto: AddCarDTO

    @transactional
    def handle(self) -> None:
        make = self.make_repository.get_by_name(self.add_car_dto.make)
        try:
            submodel = self.submodel_repository.get_by_name_model_and_make(
                name=self.add_car_dto.submodel,
                model=self.add_car_dto.model,
                make=self.add_car_dto.make,
            )
        except SubModelDoesNotExist:
            submodel = None

        if submodel is None:
            submodel = self._create_new_submodel(make)

        car = Car.create_new(
            year=self.add_car_dto.year,
            mileage=self.add_car_dto.mileage,
            submodel_pk=submodel.pk,
            price=self.add_car_dto.price,
            exterior_color=self.add_car_dto.exterior_color,
            body_type=self.add_car_dto.body_type,
            transmission=self.add_car_dto.transmission,
            fuel_type=self.add_car_dto.fuel_type,
        )
        self.car_repository.add(car)

    def _create_new_submodel(self, make: Make) -> SubModel:
        try:
            model = self.model_repository.get_by_name_and_make(
                name=self.add_car_dto.model, make=self.add_car_dto.make
            )
        except ModelDoesNotExist:
            model = None

        if model is None:
            model = Model.create_new(name=self.add_car_dto.model, make_pk=make.pk)
            self.model_repository.add(model)

        submodel = SubModel.create_new(name=self.add_car_dto.submodel, model_pk=model.pk)
        self.submodel_repository.add(submodel)
        return submodel
