from dataclasses import dataclass

from domain.constraints.not_empty_string import NotEmptyStringConstraint
from domain.value_objects.base import ConfigEntry


@dataclass(kw_only=True, slots=True, frozen=True)
class SpecialSymbol(ConfigEntry[str]):
    title: str

    @classmethod
    def new(
        cls,
        *,
        title: str,
        code: str,
        is_default: bool,
    ) -> SpecialSymbol:
        NotEmptyStringConstraint(
            value=title,
            name="Special Symbol title",
        ).check()
        NotEmptyStringConstraint(
            value=code,
            name="Special Symbol code",
        ).check()
        return SpecialSymbol(
            title=title,
            value=code,
            is_default=is_default,
        )

    def get_display_text(self) -> str:
        return self.title
