from enum import StrEnum

from dependency_injector.wiring import Provide, inject
from rich.repr import Result
from textual import events, on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive

from speedtype.outbound.zeus.client import ZeusClient
from speedtype.outbound.zeus.contracts.get_text_config import TextConfigResponseContract
from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.types.text_config import SelectedTextConfig, TextConfigName, TextConfigOption
from speedtype.ui.widgets.menu_island.island import MenuIsland
from speedtype.ui.widgets.menu_island.text import MenuIslandText
from speedtype.ui.widgets.section_menu_island import (
    MultipleSectionMenuIsland,
    SectionConfiguration,
    SectionMenuIsland,
    SectionOption,
)


class TextConfiguration(MenuIsland):
    text_config: reactive[TextConfigResponseContract] = reactive(None, init=False, recompose=True)
    text_config: TextConfigResponseContract

    class SectionName(StrEnum):
        TIME = "TIME"
        LANGUAGE = "LANGUAGE"
        WORDS_CONFIG = "WORDS CONFIG"
        SECTIONS_PANE = "sections_pane"

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
        self._text_config = SelectedTextConfig.new()

    def compose(self) -> ComposeResult:
        if not self.text_config:
            return

        yield SectionMenuIsland(
            options=(
                SectionOption(
                    label=self.SectionName.TIME,
                    value=TextConfigName.TIME,
                    css_class=CSSClass.SELECTED,
                ),
                SectionOption(
                    label=self.SectionName.LANGUAGE,
                    value=TextConfigName.LANGUAGE,
                ),
                SectionOption(
                    label=self.SectionName.WORDS_CONFIG,
                    value=(TextConfigName.WORDS_LENGTH, TextConfigName.SPECIAL_SYMBOLS),
                ),
            ),
            name=self.SectionName.SECTIONS_PANE,
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
            name=TextConfigName.TIME,
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
            name=TextConfigName.LANGUAGE,
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
                    name=TextConfigName.WORDS_LENGTH,
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
                    name=TextConfigName.SPECIAL_SYMBOLS,
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
        if event.section_name != self.SectionName.SECTIONS_PANE:
            self._text_config.update_config_option(
                config_name=event.section_name,
                option=TextConfigOption(value=str(event.value), label=event.label),
            )
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return

        for section in self.query(SectionMenuIsland):
            if section.name in event.value:
                section.show()
            elif section.name != self.SectionName.SECTIONS_PANE:
                section.hide()

    @on(SectionMenuIsland.OptionRemoved)
    def _option_removed(
        self,
        event: SectionMenuIsland.OptionRemoved,
    ) -> None:
        if event.section_name != self.SectionName.SECTIONS_PANE:
            self._text_config.remove_config_option_by_value(
                config_name=event.section_name,
                value=str(event.value),
            )
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return
