import asyncio
import random
from collections.abc import Coroutine

from dependency_injector.wiring import Provide, inject
from textual import events, on, work
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.worker import Worker

from speedtype.outbound.zeus.client import ZeusClient
from speedtype.ui.types.text_config import SelectedTextConfig
from speedtype.ui.widgets.base import BaseWidget
from speedtype.ui.widgets.typing_area.text_input import TextInput


LINE_WIDTH = 140


class TypingArea(BaseWidget):
    DEFAULT_CSS = f"""
    TypingArea {{
        width: 100%;
        height: 100%;
        align: center middle;

        .wrapper {{
            align: center middle;
            width: auto;
            padding: 1 0;

            border: hkey $surface;
            border-title-align: left;
            border-title-color: $primary;
            border-title-style: bold;
            border-title-background: $surface;

            border-subtitle-align: right;
            border-subtitle-color: $primary;
            border-subtitle-style: bold;
            border-subtitle-background: $surface;

            .text {{
                width: {LINE_WIDTH};
                height: 100%;
            }}
        }}
    }}
    """
    text_config: var[SelectedTextConfig] = var(None, init=False)
    text: var[str] = var("", init=False)
    text_config: SelectedTextConfig

    @inject
    def __init__(
        self,
        *args,
        zeus_client: ZeusClient = Provide["zeus_client"],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._zeus_client = zeus_client
        self._timer: Worker[Coroutine[None, None, None]] | None = None

    def compose(self) -> ComposeResult:
        with (
            Container(classes="wrapper"),
            Container(classes="text"),
        ):
            yield TextInput(line_length=LINE_WIDTH).data_bind(TypingArea.text)

    def watch_text_config(self) -> None:
        config_values = []
        selected_time = 0

        if self.text_config.time:
            selected_time = self.text_config.input_time_seconds

        if self.text_config.langauge:
            config_values.append(self.text_config.langauge.label)

        if self.text_config.words_length:
            config_values.append(self.text_config.words_length.label)

        if self.text_config.special_symbols:
            config_values.extend(symbol.label for symbol in self.text_config.special_symbols)

        self.query_one(TextInput).input_time = selected_time
        self._update_timer(seconds=selected_time)

        if self.query_one(Container).border_subtitle != (config_string := f" {', '.join(config_values)} "):
            self.query_one(Container).border_subtitle = config_string
            self.regenerate_text()

    def stop(self) -> None:
        self.query_one(TextInput).stop(is_finished=False)

    def _update_timer(
        self,
        *,
        seconds: str | int,
    ) -> None:
        self.query_one(Container).border_title = f" {seconds} SEC "

    async def _load_input_text(self) -> str:
        special_symbol_types = [symbol.value for symbol in self.text_config.special_symbols or []]
        text_data = await self._zeus_client.get_text_words(
            language=self.text_config.langauge.value,
            words_length=self.text_config.words_length.value,
            special_symbol_types=special_symbol_types or None,
        )

        random.shuffle(text_data.words)

        if not text_data.special_symbols:
            return " ".join(text_data.words)

        for i, _word in enumerate(text_data.words):
            if random.random() > 0.75:
                text_data.words[i] += random.choice(text_data.special_symbols)

        return " ".join(text_data.words)

    @on(events.Mount)
    def _load_initial_text(self) -> None:
        self.regenerate_text()

    @on(TextInput.TypingStarted)
    def _typing_started(self) -> None:
        self._timer = self._start_timer()

    @on(TextInput.TypingFinished)
    @on(TextInput.TypingStopped)
    def _reset_typing_area(self) -> None:
        self._timer.cancel()
        self._update_timer(seconds=self.text_config.input_time_seconds)
        self.regenerate_text()

    @work(exclusive=True, group="regenerate_text")
    async def regenerate_text(self) -> None:
        if self.text_config and self.text_config.langauge and self.text_config.words_length:
            self.text = await self._load_input_text()

    @work(exclusive=True, group="timer")
    async def _start_timer(self) -> None:
        remaining_seconds = self.text_config.input_time_seconds

        while remaining_seconds > 0:
            await asyncio.sleep(1)
            remaining_seconds -= 1
            self._update_timer(seconds=remaining_seconds)
