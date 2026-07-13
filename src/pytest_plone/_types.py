from OFS.Application import Application
from OFS.SimpleItem import Item
from plone.app.vocabularies import PermissiveVocabulary
from plone.app.vocabularies import SlicableVocabulary
from plone.dexterity.content import DexterityContent
from plone.dexterity.fti import DexterityFTI
from Products.CMFPlone.Portal import PloneSite
from typing import Any
from typing import Protocol
from typing import TypeAlias
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import TreeVocabulary


Context: TypeAlias = DexterityContent | Item

PloneVocabulary: TypeAlias = (
    SimpleVocabulary | TreeVocabulary | PermissiveVocabulary | SlicableVocabulary
)


class ProfileVersionGetter(Protocol):
    def __call__(self, profile: str) -> str: ...


class FTIGetter(Protocol):
    def __call__(self, name: str) -> DexterityFTI: ...


class BehaviorsGetter(Protocol):
    def __call__(self, name: str) -> list[str]: ...


class VocabularyGetter(Protocol):
    def __call__(self, name: str, context: Context) -> PloneVocabulary: ...


class ProfilesApplier(Protocol):
    def __call__(self, portal: PloneSite, profiles: list[str]) -> None: ...


class ContentCreator(Protocol):
    def __call__(
        self, container: DexterityContent | Item, content: list[dict]
    ) -> None: ...


class RolesGranter(Protocol):
    def __call__(self, context: DexterityContent | Item, roles: list[str]) -> None: ...


class RequestFactory(Protocol):
    def __call__(
        self,
        *,
        role: str = ...,
        basic_auth: tuple[str, str] | None = ...,
        api: bool = ...,
    ) -> Any: ...


class SiteCreator(Protocol):
    def __call__(self, app: Application, answers: dict) -> PloneSite: ...
