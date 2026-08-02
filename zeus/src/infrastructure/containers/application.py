from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container

from infrastructure.containers.domain import DomainContainer
from infrastructure.containers.infrastructure import InfrastructureContainer


class ApplicationContainer(DeclarativeContainer):
    config = Configuration(strict=True)

    infra: InfrastructureContainer = Container(
        InfrastructureContainer,
        config=config,
    )
    domain: DomainContainer = Container(
        DomainContainer,
        deps=infra,
    )
