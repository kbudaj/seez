import csv
from typing import List

from dateutil import parser
from haps import Inject

from seez.domain.models import Make
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import CarRepository, MakeRepository


class ImportDataComand(BaseCommand):
    car_repository: CarRepository = Inject()
    make_repository: MakeRepository = Inject()

    path: str = "/app/data/"

    @transactional
    def handle(self) -> None:
        self.makes = {}
        makes_to_create = list(self.makes.values())
        self.make_repository.add_batch(makes_to_create)

    def _parse_makes(self) -> List[Make]:
        with open(self.path + "makes.csv", newline="") as f:
            read = csv.DictReader(f)
            for line in read:
                self._parse_line(line)

    def _line_to_make(self, line, makes) -> Make:
        pk = line["id"]
        name = line["name"]
        active = True if line["active"].lower() == "f" else False
        created_at = parser.parse(line["created_at"])
        updated_at = parser.parse(line["updated_at"])
        make = Make(
            pk=Make.next_pk(),
            name=name,
            active=active,
            created_at=created_at,
            updated_at=updated_at,
        )
        self.makes[pk] = make
