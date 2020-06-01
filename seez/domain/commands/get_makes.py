from haps import Inject

from seez.domain.dto import MakeListDTO
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import MakeRepository


class GetAllMakes(BaseCommand):
    make_repository: MakeRepository = Inject()

    @transactional
    def handle(self) -> MakeListDTO:
        makes = self.make_repository.get_all_active()
        return MakeListDTO.from_model(makes)
