from enum import StrEnum

from rich.repr import Result
from textual import events, on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive

from speedtype.domain.text.service import TextService
from speedtype.domain.text.value_objects import TextConfig
from speedtype.ui.constants.classes import CSSClass
from speedtype.ui.widgets.menu_island.island import MenuIsland
from speedtype.ui.widgets.menu_island.text import MenuIslandText
from speedtype.ui.widgets.section_menu_island import (
    MultipleSectionMenuIsland,
    SectionConfiguration,
    SectionMenuIsland,
    SectionOption,
)


type SelectedTextConfig = dict[TextConfiguration.Configuration, list[str]]


class TextConfiguration(MenuIsland):
    text_config: reactive[TextConfig] = reactive(None, init=False, recompose=True)
    text_config: TextConfig

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

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._text_service = TextService()
        self._text_config: SelectedTextConfig = {}
        self._customization_sections_name = "config_menu"
        self._customization_sections = SectionMenuIsland(
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

    def compose(self) -> ComposeResult:
        yield self._customization_sections

        yield MenuIslandText(label="┃")

        yield SectionMenuIsland(
            options=tuple(
                SectionOption(
                    label=option.display_text,
                    value=str(option.seconds),
                    css_class=CSSClass.SELECTED if option.is_default else None,
                ) for option in self.text_config.time_limits
            ),
            name=self.Configuration.TIME,
            persistent=True,
            is_vertical=False,
        )
        yield SectionMenuIsland(
            options=tuple(
                SectionOption(
                    label=option.title,
                    value=option.code,
                    css_class=CSSClass.SELECTED if option.is_default else None,
                ) for option in self.text_config.languages
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
                            value=option.code,
                            css_class=CSSClass.SELECTED if option.is_default else None,
                        ) for option in self.text_config.words_configs.word_lengths.options,
                    ),
                    name="words_length",
                ),
                SectionConfiguration(
                    options=tuple(
                        SectionOption(
                            label=option.title,
                            value=option.code,
                            css_class=CSSClass.SELECTED if option.is_default else None,
                        ) for option in self.text_config.words_configs.special_symbols.options,
                    ),
                    name="additional_symbols",
                    is_multiple_options=True,
                ),
            ),
        )

        for section in self._text_config_sections.values():
            yield section

    @on(events.Mount)
    async def _load_text_config(self) -> None:
        self.text_config = await self._text_service.get_text_config()

    @on(SectionMenuIsland.OptionSelected)
    def _option_selected(
        self,
        event: SectionMenuIsland.OptionSelected,
    ) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config.setdefault(event.section_name, []).append(event.value)
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return

        selected_section_name = event.value
        self._text_config_sections[selected_section_name].show()

        for section_name, section in self._text_config_sections.items():
            if selected_section_name == section_name:
                section.show()
            else:
                section.hide()

    @on(SectionMenuIsland.OptionRemoved)
    def _option_removed(
        self,
        event: SectionMenuIsland.OptionRemoved,
    ) -> None:
        if event.section_name != self._customization_sections_name:
            self._text_config.setdefault(event.section_name, []).remove(event.value)
            self.post_message(self.ConfigUpdated(selected_text_config=self._text_config))
            return
