from speedtype.infrastructure.containers import ApplicationContainer
from speedtype.infrastructure.settings import SpeedTypeSettings
from speedtype.ui.app import SpeedType


def main() -> None:
    container = ApplicationContainer()
    container.config.from_pydantic(SpeedTypeSettings())
    container.wire(
        modules=[
            "speedtype.ui.widgets.text_configuration",
            "speedtype.ui.widgets.typing_area.area",
        ]
    )
    SpeedType().run()


if __name__ == "__main__":
    main()
