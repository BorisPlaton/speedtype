from textual.widget import Widget


class BaseWidget(Widget):
    def __init__(
        self,
        *args,
        name: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._name = name

    def hide(self) -> None:
        self.styles.display = "none"

    def show(self) -> None:
        self.styles.display = "block"

    @property
    def name(self) -> str | None:
        return self._name
