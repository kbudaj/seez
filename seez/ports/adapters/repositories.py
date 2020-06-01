from typing import List

from haps import Inject, egg

from seez.aliases import CarPk, MakePk, ModelPk, SubModelPk
from seez.domain.exceptions import (
    CarDoesNotExist,
    MakeDoesNotExist,
    ModelDoesNotExist,
    SubModelDoesNotExist,
)
from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.session import Session
from seez.ports.repositories import (
    CarRepository,
    MakeRepository,
    ModelRepository,
    SubModelRepository,
    does_not_exist_error,
)


@egg
class SqlAlchemyCarRepository(CarRepository):
    session: Session = Inject()

    @does_not_exist_error(CarDoesNotExist)
    def get_by_pk(self, pk: CarPk) -> Car:
        return self.session.query(Car).filter(Car.pk == pk).one()

    def get_all(self) -> List[Car]:
        return list(self.session.query(Car).all())

    def add(self, car: Car) -> None:
        self.session.add(car)
        self.session.flush()

    def add_batch(self, cars: List[Car]) -> None:
        self.session.bulk_save_objects(cars)


@egg
class SqlAlchemyMakeRepository(MakeRepository):
    session: Session = Inject()

    @does_not_exist_error(MakeDoesNotExist)
    def get_by_pk(self, pk: MakePk) -> Make:
        return self.session.query(Make).filter(Make.pk == pk).one()

    def get_all(self) -> List[Make]:
        return list(self.session.query(Make).all())

    def add(self, make: Make) -> None:
        self.session.add(make)
        self.session.flush()

    def add_batch(self, makes: List[Make]) -> None:
        self.session.bulk_save_objects(makes)


@egg
class SqlAlchemyModelRepository(ModelRepository):
    session: Session = Inject()

    @does_not_exist_error(ModelDoesNotExist)
    def get_by_pk(self, pk: ModelPk) -> Model:
        return self.session.query(Model).filter(Model.pk == pk).one()

    def get_all(self) -> List[Model]:
        return list(self.session.query(Model).all())

    def add(self, model: Model) -> None:
        self.session.add(model)
        self.session.flush()

    def add_batch(self, models: List[Model]) -> None:
        self.session.bulk_save_objects(models)


@egg
class SqlAlchemySubModelRepository(SubModelRepository):
    session: Session = Inject()

    @does_not_exist_error(SubModelDoesNotExist)
    def get_by_pk(self, pk: SubModelPk) -> SubModel:
        return self.session.query(SubModel).filter(SubModel.pk == pk).one()

    def get_all(self) -> List[SubModel]:
        return list(self.session.query(SubModel).all())

    def add(self, submodel: SubModel) -> None:
        self.session.add(submodel)
        self.session.flush()

    def add_batch(self, submodels: List[SubModel]) -> None:
        self.session.bulk_save_objects(submodels)
