from haps import Inject

from seez.domain.dto import ModelListDTO
from seez.infrastructure.command import BaseCommand
from seez.infrastructure.session import transactional
from seez.ports.repositories import ModelRepository


class GetAllModels(BaseCommand):
    model_repository: ModelRepository = Inject()

    @transactional
    def handle(self) -> ModelListDTO:
        models = self.model_repository.get_all_active()
        return ModelListDTO.from_model(models)
