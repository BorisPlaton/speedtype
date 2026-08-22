from typing import Annotated

from fastapi import APIRouter, Depends

from domain.use_cases.get_text_config import GetTextConfig
from domain.use_cases.get_text_words import GetTextWords
from inbound.http.contracts.text_config import GetTextConfigResponseContract
from inbound.http.contracts.text_words import GetTextWordsRequestContract, GetTextWordsResponseContract
from inbound.http.dependencies import get_domain_container
from infrastructure.containers.domain import DomainContainer


router = APIRouter(prefix="/text")


@router.post("/words", response_model_exclude_none=True)
async def get_text_text(
    container: Annotated[DomainContainer, Depends(get_domain_container)],
    words_properties: GetTextWordsRequestContract,
) -> GetTextWordsResponseContract:
    get_text_words_use_case: GetTextWords = container.get_text_words()
    text_words = await get_text_words_use_case.execute(
        language=words_properties.language,
        words_length=words_properties.words_length,
        special_symbol_types=words_properties.special_symbol_types,
    )
    return GetTextWordsResponseContract.from_use_case(data=text_words)


@router.get("/config")
async def get_text_config(
    container: Annotated[DomainContainer, Depends(get_domain_container)],
) -> GetTextConfigResponseContract:
    get_text_config_use_case: GetTextConfig = container.get_text_config()
    text_config = await get_text_config_use_case.execute()
    return GetTextConfigResponseContract.from_use_case(data=text_config)
