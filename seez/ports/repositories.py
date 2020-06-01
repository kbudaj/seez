from abc import abstractmethod
from typing import Any, Dict, List, Optional, Type

from haps import base
from sqlalchemy.orm.exc import NoResultFound

from seez.aliases import CarPk, MakePk, ModelPk, SubModelPk
from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.exceptions import DoesNotExistError
from seez.infrastructure.repositories import Repository


def does_not_exist_error(exc: Optional[Type[Exception]] = None) -> Any:
    """
    Decorator for repositories' `get_` methods.
    Raises given exception when object was not found
    """

    def decorator(fn: Any) -> Any:
        def wrapped(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
            try:
                return fn(*args, **kwargs)
            except NoResultFound:
                if exc is not None:
                    raise exc
                else:
                    raise DoesNotExistError

        return wrapped

    return decorator


@base
class CarRepository(Repository):
    @abstractmethod
    def get_by_pk(self, pk: CarPk) -> Car:
        pass

    @abstractmethod
    def get_all(self) -> List[Car]:
        pass

    @abstractmethod
    def get_active_paged(self, page_number: int) -> List[Car]:
        pass

    @abstractmethod
    def add(self, car: Car) -> None:
        pass

    @abstractmethod
    def add_batch(self, cars: List[Car]) -> None:
        pass


@base
class MakeRepository(Repository):
    @abstractmethod
    def get_by_pk(self, pk: MakePk) -> Make:
        pass

    @abstractmethod
    def get_all(self) -> List[Make]:
        pass

    @abstractmethod
    def get_all_active(self) -> List[Make]:
        pass

    @abstractmethod
    def add(self, make: Make) -> None:
        pass

    @abstractmethod
    def add_batch(self, makes: List[Make]) -> None:
        pass


@base
class ModelRepository(Repository):
    @abstractmethod
    def get_by_pk(self, pk: ModelPk) -> Model:
        pass

    @abstractmethod
    def get_all(self) -> List[Model]:
        pass

    @abstractmethod
    def get_all_active(self) -> List[Model]:
        pass

    @abstractmethod
    def add(self, model: Model) -> None:
        pass

    @abstractmethod
    def add_batch(self, models: List[Model]) -> None:
        pass


@base
class SubModelRepository(Repository):
    @abstractmethod
    def get_by_pk(self, pk: SubModelPk) -> SubModel:
        pass

    @abstractmethod
    def get_all(self) -> List[SubModel]:
        pass

    @abstractmethod
    def get_all_active(self) -> List[SubModel]:
        pass

    @abstractmethod
    def add(self, submodel: SubModel) -> None:
        pass

    @abstractmethod
    def add_batch(self, submodels: List[SubModel]) -> None:
        pass
