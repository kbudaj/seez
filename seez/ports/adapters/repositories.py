from typing import Any, Dict, List, Optional, cast

from haps import Inject, egg
from sqlalchemy import desc, func
from sqlalchemy.sql.operators import is_
from sqlalchemy_filters import apply_filters, apply_pagination

from seez.aliases import (
    CarPk,
    MakeName,
    MakePk,
    ModelName,
    ModelPk,
    SubModelName,
    SubModelPk,
)
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

    def get_active_paged(
        self,
        page_number: int = 1,
        page_size: int = 20,
        price_min: Optional[int] = None,
        price_max: Optional[int] = None,
        mileage_min: Optional[int] = None,
        mileage_max: Optional[int] = None,
    ) -> List[Car]:
        active_cars_q = (
            self.session.query(Car)
            .filter(is_(Car.active, True))
            .order_by(desc(Car.updated_at))
        )

        filter_spec = self._prepare_filters(
            price_min, price_max, mileage_min, mileage_max
        )
        filtered_q = apply_filters(active_cars_q, filter_spec, do_auto_join=False)

        query, pagination = apply_pagination(
            filtered_q, page_number=page_number, page_size=page_size
        )
        return cast(List[Car], query.all())

    def _prepare_filters(
        self,
        price_min: Optional[int],
        price_max: Optional[int],
        mileage_min: Optional[int],
        mileage_max: Optional[int],
    ) -> List[Dict[Any, Any]]:
        filter_spec = []
        if price_min is not None:
            filter_spec.append({"field": "price", "op": ">=", "value": price_min})
        if price_max is not None:
            filter_spec.append({"field": "price", "op": "<=", "value": price_max})
        if mileage_min is not None:
            filter_spec.append({"field": "mileage", "op": ">=", "value": mileage_min})
        if mileage_max is not None:
            filter_spec.append({"field": "mileage", "op": "<=", "value": mileage_max})
        return filter_spec

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

    def get_all_active(self) -> List[Make]:
        return list(self.session.query(Make).filter(is_(Make.active, True)).all())

    @does_not_exist_error(MakeDoesNotExist)
    def get_by_name(self, name: MakeName) -> Make:
        return (
            self.session.query(Make)
            .filter(func.lower(Make.name) == func.lower(name))
            .one()
        )

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

    def get_all_active(self) -> List[Model]:
        return list(self.session.query(Model).filter(is_(Model.active, True)).all())

    def get_by_name_and_make(self, name: ModelName, make: MakeName) -> Model:
        return (
            self.session.query(Model)
            .join(Make, Model.make_pk == Make.pk)
            .filter(func.lower(Model.name) == func.lower(name))
            .filter(func.lower(Make.name) == func.lower(make))
            .first()
        )

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

    def get_all_active(self) -> List[SubModel]:
        return list(self.session.query(SubModel).filter(is_(SubModel.active, True)).all())

    def get_by_name_model_and_make(
        self, name: SubModelName, make: MakeName, model: ModelName
    ) -> SubModel:
        return (
            self.session.query(SubModel)
            .join(Model, SubModel.model_pk == Model.pk)
            .join(Make, Model.make_pk == Make.pk)
            .filter(func.lower(SubModel.name) == func.lower(name))
            .filter(func.lower(Model.name) == func.lower(model))
            .filter(func.lower(Make.name) == func.lower(make))
            .first()
        )

    def add(self, submodel: SubModel) -> None:
        self.session.add(submodel)
        self.session.flush()

    def add_batch(self, submodels: List[SubModel]) -> None:
        self.session.bulk_save_objects(submodels)
