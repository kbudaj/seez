from typing import Any, Dict

from haps.scopes import Scope
from scopectx import Context, NotInContextException

TRANSACTIONAL_SCOPE = "__transactional"
THREAD_SCOPE = "__thread"


class TransactionalScope(Scope):
    scope = Context()

    def get_object(self, class_: Any) -> Any:
        try:
            return self.scope[class_]
        except KeyError:
            obj = class_()
            self.scope[class_] = obj
            return obj


class TestTransactionalScope(Scope):
    scope = Context()
    objects: Dict[Any, Any] = {}

    def get_object(self, class_: Any) -> Any:
        try:
            return self.scope[class_]
        except KeyError:
            obj = class_()
            self.scope[class_] = obj
            return obj
        except NotInContextException:
            if class_ not in self.objects:
                self.objects[class_] = class_()

            return self.objects[class_]

    @classmethod
    def reset(cls) -> None:
        cls.objects = {}
