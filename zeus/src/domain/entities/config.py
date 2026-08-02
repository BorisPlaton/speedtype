from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from funcy import first

from domain.constraints.display_unique import DisplayUniqueConstraint
from domain.constraints.one_default import NotMoreThanOneDefaultConstraint
from domain.exceptions.config import DefaultOptionAlreadyExists, OptionWithValueDoesntExist
from domain.value_objects.base import ConfigEntry


@dataclass(kw_only=True, slots=True)
class Config[Option: ConfigEntry[object]](ABC):
    is_required: ClassVar[bool]
    name: ClassVar[str]
    options: list[Option]

    @classmethod
    def new(
        cls,
        *,
        options: list[Option],
    ) -> Config:
        NotMoreThanOneDefaultConstraint(
            items=options,
            exact_one=cls.is_required,
            name=cls.name,
        ).check()
        DisplayUniqueConstraint(items=options).check()
        return cls(options=options)

    def add_option(
        self,
        *,
        option: Option,
    ) -> None:
        default_option = self.default_option

        if option.is_default and self.default_option:
            raise DefaultOptionAlreadyExists(
                name=self.name,
                default_value=default_option.value,
            )

        DisplayUniqueConstraint(items=self.options).check()

        self.options.append(option)

    def set_default_option(
        self,
        *,
        option_value: object,
    ) -> None:
        new_default: Option | None = first(
            filter(lambda option: option.value == option_value, (option for option in self.options))
        )

        if not new_default:
            raise OptionWithValueDoesntExist(
                name=self.name,
                value=option_value,
            )

        new_default.is_default = True
        self.default_option.is_default = False

    @property
    def default_option(self) -> Option | None:
        return first(filter(lambda option: option.is_default, (option for option in self.options)))
