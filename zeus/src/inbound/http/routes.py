from typing import Annotated

from fastapi import APIRouter, Depends, Request

from domain.use_cases.get_text_config import GetTextConfig
from inbound.http.contracts.text_config import TextConfigResponseContract
from inbound.http.dependencies import get_domain_container
from infrastructure.containers.domain import DomainContainer


router = APIRouter(prefix="/text")


@router.get("/")
async def get_input_text(request: Request) -> None:
    pass


@router.get("/config")
async def get_text_config(
    container: Annotated[DomainContainer, Depends(get_domain_container)],
) -> TextConfigResponseContract:
    get_text_config_use_case: GetTextConfig = container.get_text_config()
    text_config = await get_text_config_use_case.execute()
    return TextConfigResponseContract.from_use_case(data=text_config)
