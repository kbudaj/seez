from haps import Container
from haps.scopes import Scope
from haps.scopes.thread import ThreadScope

from seez.infrastructure.scopes import (
    THREAD_SCOPE,
    TRANSACTIONAL_SCOPE,
    TransactionalScope,
)


def configure_haps(transactional_scope: Scope = TransactionalScope) -> None:
    Container.autodiscover(
        ["seez.ports",]
    )
    Container().register_scope(TRANSACTIONAL_SCOPE, transactional_scope)
    Container().register_scope(THREAD_SCOPE, ThreadScope)
