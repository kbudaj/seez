from haps import Inject

from seez.domain.dto import SubModelListDTO
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import SubModelRepository


class GetAllSubModels(BaseCommand):
    submodel_repository: SubModelRepository = Inject()

    @transactional
    def handle(self) -> SubModelListDTO:
        submodels = self.submodel_repository.get_all_active()
        return SubModelListDTO.from_model(submodels)
