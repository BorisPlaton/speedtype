from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Container, Provider, Singleton

from infrastructure.containers.domain import DomainContainer
from infrastructure.containers.infrastructure import InfrastructureContainer
from infrastructure.secret_manager.base import SecretManager
from infrastructure.secret_manager.factory import secret_manager_factory
from infrastructure.settings import GCPConfig, Settings


class SettingsContainer(DeclarativeContainer):
    gcp_config: Provider[GCPConfig] = Singleton(GCPConfig)
    secret_manager: Provider[SecretManager] = Singleton(
        secret_manager_factory,
        gcp_config=gcp_config,
    )
    config: Provider[Settings] = Singleton(
        Settings.new,
        secret_manager=secret_manager,
    )


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
