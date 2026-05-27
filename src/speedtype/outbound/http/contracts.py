from pydantic import BaseModel, ConfigDict, alias_generators


class BaseResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
        frozen=True,
    )
