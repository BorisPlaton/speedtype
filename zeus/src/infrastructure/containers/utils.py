from infrastructure.containers.application import ApplicationContainer, SettingsContainer


def create_container() -> ApplicationContainer:
    settings_container = SettingsContainer()
    app_container = ApplicationContainer()
    app_container.config.from_pydantic(settings_container.config(), required=True)
    return app_container
