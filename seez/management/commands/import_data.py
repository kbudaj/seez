import csv
from typing import Any, Dict, Optional

from dateutil import parser
from haps import Inject
from tqdm import tqdm

from seez.domain.models import Car, Make, Model, SubModel
from seez.infrastructure.session import transactional
from seez.management.commands import ManagementCommand
from seez.ports.repositories import (
    CarRepository,
    MakeRepository,
    ModelRepository,
    SubModelRepository,
)


class Command(ManagementCommand):
    car_repository: CarRepository = Inject()
    make_repository: MakeRepository = Inject()
    model_repository: ModelRepository = Inject()
    submodel_repository: SubModelRepository = Inject()

    path: str = "/app/data/"

    @transactional
    def handle(self) -> None:
        self.makes: Dict[str, Make] = {}
        self.models: Dict[str, Model] = {}
        self.submodels: Dict[str, SubModel] = {}
        self.cars: Dict[str, Car] = {}

        self._parse_makes()
        self._parse_models()
        self._parse_submodels()
        self._parse_cars()

    def _parse_makes(self) -> None:
        with open(self.path + "makes.csv", newline="") as f:
            read = csv.DictReader(f)
            self.stdout.write("Importing Makes")
            for line in tqdm(read):
                self._parse_make_line(line)

        makes_to_create = list(self.makes.values())
        self.make_repository.add_batch(makes_to_create)

    def _parse_make_line(self, line: Dict[str, Any]) -> None:
        id = line["id"]
        name = line["name"]
        active = True if line["active"].lower() == "t" else False
        created_at = parser.parse(line["created_at"])
        updated_at = parser.parse(line["updated_at"])
        make = Make(
            pk=Make.next_pk(),
            name=name,
            active=active,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.makes[id] = make

    def _parse_models(self) -> None:
        with open(self.path + "models.csv", newline="") as f:
            read = csv.DictReader(f)
            self.stdout.write("Importing Models")
            for line in tqdm(read):
                self._parse_model_line(line)

        models_to_create = list(self.models.values())
        self.model_repository.add_batch(models_to_create)

    def _parse_model_line(self, line: Dict[str, Any]) -> None:
        id = line["id"]
        name = line["name"]
        active = True if line["active"].lower() == "t" else False
        make_id = line["make_id"]
        created_at = line["created_at"]
        updated_at = line["updated_at"]
        model = Model(
            pk=Model.next_pk(),
            name=name,
            active=active,
            make_pk=self.makes[make_id].pk,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.models[id] = model

    def _parse_submodels(self) -> None:
        with open(self.path + "submodels.csv", newline="") as f:
            read = csv.DictReader(f)
            self.stdout.write("Importing SubModels")
            for line in tqdm(read):
                self._parse_submodel_line(line)

        submodels_to_create = list(self.submodels.values())
        self.submodel_repository.add_batch(submodels_to_create)

    def _parse_submodel_line(self, line: Dict[str, Any]) -> None:
        id = line["id"]
        name = line["name"]
        active = True if line["active"].lower() == "t" else False
        model_id = line["model_id"]
        created_at = line["created_at"]
        updated_at = line["updated_at"]
        submodel = SubModel(
            pk=SubModel.next_pk(),
            name=name,
            active=active,
            model_pk=self.models[model_id].pk,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.submodels[id] = submodel

    def _parse_cars(self) -> None:
        with open(self.path + "cars.csv", newline="") as f:
            read = csv.DictReader(f)
            self.stdout.write("Importing SubModels")
            for line in tqdm(read):
                self._parse_cars_line(line)

        cars_to_create = list(self.cars.values())
        self.car_repository.add_batch(cars_to_create)

    def _parse_cars_line(self, line: Dict[str, Any]) -> None:
        id = line["id"]
        active = True if line["active"].lower() == "t" else False
        year = line["year"]
        mileage_str = line["mileage"]

        mileage: Optional[int] = None
        try:
            mileage = int(mileage_str)
        except ValueError:
            mileage = None

        price_str = line["price"]
        price: Optional[int] = None
        try:
            price = int(price_str)
        except ValueError:
            price = None
        exterior_color = line["exterior_color"]
        created_at = line["created_at"]
        updated_at = line["updated_at"]
        submodel_id = line["submodel_id"]
        body_type_str = line["body_type"]
        body_type = self._str_to_body_type(body_type_str)

        transmission_str = line["transmission"]
        transmission = self._str_to_transmission(transmission_str)

        fuel_type_str = line["fuel_type"]
        fuel_type = self._str_to_fuel_type(fuel_type_str)

        car = Car(
            pk=Car.next_pk(),
            active=active,
            year=year,
            mileage=mileage,
            price=price,
            exterior_color=exterior_color,
            created_at=created_at,
            updated_at=updated_at,
            submodel_pk=self.submodels[submodel_id].pk,
            body_type=body_type,
            transmission=transmission,
            fuel_type=fuel_type,
        )
        self.cars[id] = car

    def _str_to_body_type(self, s: str) -> Car.BodyType:
        m = {
            "coupe": Car.BodyType.COUPE,
            "sedan": Car.BodyType.SEDAN,
            "suv": Car.BodyType.SUV,
            "hatchback": Car.BodyType.HATCHBACK,
            "convertible": Car.BodyType.CONVERTIBLE,
            "van": Car.BodyType.VAN,
            "sports": Car.BodyType.SPORTS,
            "truck": Car.BodyType.TRUCK,
            "wagon": Car.BodyType.WAGON,
            "luxury": Car.BodyType.LUXURY,
        }
        s = s.lower()
        body_type = m.get(s)
        return body_type

    def _str_to_transmission(self, s: str) -> Car.Transmission:
        m = {
            "automatic": Car.Transmission.AUTOMATIC,
            "manual": Car.Transmission.MANUAL,
        }
        s = s.lower()
        transmission = m.get(s)
        return transmission

    def _str_to_fuel_type(self, s: str) -> Car.FuelType:
        m = {
            "petrol": Car.FuelType.PETROL,
            "hybrid": Car.FuelType.HYBRID,
            "diesel": Car.FuelType.DIESEL,
            "electricity": Car.FuelType.ELECTRICITY,
        }
        s = s.lower()
        fuel_type = m.get(s)
        return fuel_type
