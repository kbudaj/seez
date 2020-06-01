from typing import Any, Optional


class BaseError(Exception):
    description: Any
    code: Optional[str] = None

    def __init__(self, description: Any = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args)
        self.description = description or self.description
        self.code = kwargs.get("code", None) or self.code

    def __str__(self) -> Any:
        return self.description

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if self.code is not None:
            return self.code == other.code
        else:
            return bool(self.description == other.description)


class SeezError(BaseError):
    description = "Base Exception"


class DoesNotExistError(SeezError):
    description = "Does Not Exist"
