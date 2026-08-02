from enum import StrEnum
from typing import NamedTuple

from dependency_injector.wiring import Provide, inject
from funcy import select
from rich.repr import Result
from textual import events, on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive

from speedtype.outbound.zeus.client import ZeusClient
from speedtype.outbound.zeus.contracts.fetch_text_config import TextConfigResponseContract
from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.widgets.menu_island.island import MenuIsland
from speedtype.ui.widgets.menu_island.text import MenuIslandText
from speedtype.ui.widgets.section_menu_island import (
    MultipleSectionMenuIsland,
    SectionConfiguration,
    SectionMenuIsland,
    SectionOption,
)


type SelectedTextConfig = dict[str, list[TextConfigOption]]


class TextConfigOption(NamedTuple):
    label: str
    value: str | None = None


class TextConfiguration(MenuIsland):
    text_config: reactive[TextConfigResponseContract] = reactive(None, init=False, recompose=True)
    text_config: TextConfigResponseContract

    class Configuration(StrEnum):
        TIME = "TIME"
        LANGUAGE = "LANGUAGE"
        DIFFICULTY = "DIFFICULTY"

    class ConfigUpdated(Message):
        def __init__(
            self,
            selected_text_config: SelectedTextConfig,
        ) -> None:
            self.selected_text_config = selected_text_config
            super().__init__()

        def __rich_repr__(self) -> Result:
            yield "selected_text_config", self.selected_text_config

    @inject
    def __init__(
        self,
        *args,
        zeus_client: ZeusClient = Provide["zeus_client"],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._zeus_client = zeus_client
        self._text_config: SelectedTextConfig = {}
        self._customization_sections_name = "config_menu"

    def compose(self) -> ComposeResult:
        if not self.text_config:
            return

        yield SectionMenuIsland(
            options=(
                SectionOption(
                    label=self.Configuration.TIME,
                    value=self.Configuration.TIME,
                    css_class=CSSClass.SELECTED,
                ),
                SectionOption(
                    label=self.Configuration.LANGUAGE,
                    value=self.Configuration.LANGUAGE,
                ),
                SectionOption(
                    label=self.Configuration.DIFFICULTY,
                    value=self.Configuration.DIFFICULTY,
                ),
            ),
            name=self._customization_sections_name,
            persistent=True,
            is_vertical=False,
        )

        yield MenuIslandText(label="┃")

        yield SectionMenuIsland(
            options=tuple(
                SectionOption(
                    label=option.title,
                    value=str(option.value),
                    css_class=CSSClass.SELECTED if option.is_default else None,
                )
                for option in self.text_config.time_limits.options
            ),
            name=self.Configuration.TIME,
            persistent=True,
            is_vertical=False,
        )
        yield SectionMenuIsland(
            options=tuple(
                SectionOption(
                    label=option.title,
                    value=option.value,
                    css_class=CSSClass.SELECTED if option.is_default else None,
                )
                for option in self.text_config.text_languages.options
            ),
            name=self.Configuration.LANGUAGE,
            persistent=True,
            is_vertical=True,
        )
        yield MultipleSectionMenuIsland(
            section_configs=(
                SectionConfiguration(
                    options=tuple(
                        SectionOption(
                            label=option.title,
                            value=option.value,
                            css_class=CSSClass.SELECTED if option.is_default else None,
                        )
                        for option in self.text_config.words_length.options
                    ),
                    name=self.Configuration.DIFFICULTY,
                ),
                SectionConfiguration(
                    options=tuple(
                        SectionOption(
                            label=option.title,
                            value=option.value,
                            css_class=CSSClass.SELECTED if option.is_default else None,
                        )
                        for option in self.text_config.special_symbols.options
                    ),
                    is_multiple_options=True,
                    name=self.Configuration.DIFFICULTY,
                ),
            ),
        )

    @on(events.Mount)
    async def _load_text_config(self) -> None:
        self.text_config = await self._zeus_client.get_text_config()

    @on(SectionMenuIsland.OptionSelected)
    def _option_selected(
        self,
        event: SectionMenuIsland.OptionSelected,
    ) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config.setdefault(event.section_name, []).append(
                TextConfigOption(value=event.value, label=event.label),
            )
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return

        for section in self.query(SectionMenuIsland):
            if section.name == event.value:
                section.show()
            elif section.name != self._customization_sections_name:
                section.hide()

    @on(SectionMenuIsland.OptionRemoved)
    def _option_removed(
        self,
        event: SectionMenuIsland.OptionRemoved,
    ) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config[event.section_name] = select(
                lambda option: option.value != event.value,
                self._text_config.setdefault(event.section_name, []),
            )
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return
