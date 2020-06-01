from seez.infrastructure.exceptions import DoesNotExistError


class CarDoesNotExist(DoesNotExistError):
    description = "Car does not exist"


class ModelDoesNotExist(DoesNotExistError):
    description = "Model does not exist"


class SubModelDoesNotExist(DoesNotExistError):
    description = "SubModel does not exist"


class MakeDoesNotExist(DoesNotExistError):
    description = "Make does not exist"
