from fastapi import Request

from infrastructure.containers.domain import DomainContainer


def get_domain_container(request: Request) -> DomainContainer:
    return request.app.extra["container"].domain
