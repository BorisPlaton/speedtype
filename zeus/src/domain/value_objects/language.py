from dataclasses import dataclass

from domain.constraints.not_empty import NotEmptyStringConstraint
from domain.value_objects.base import ConfigEntry


@dataclass(kw_only=True, slots=True, frozen=True)
class Language(ConfigEntry[str]):
    title: str

    @classmethod
    def new(
        cls,
        *,
        title: str,
        code: str,
        is_default: bool,
    ) -> Language:
        NotEmptyStringConstraint(
            value=title,
            name="Language title",
        ).check()
        NotEmptyStringConstraint(
            value=code,
            name="Language code",
        ).check()
        return Language(
            title=title,
            value=code,
            is_default=is_default,
        )

    def get_display_text(self) -> str:
        return self.title
