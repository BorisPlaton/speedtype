from abc import ABC

from domain.entities.time_limits import TimeLimits
from domain.repository.config import ConfigRepository


class TimeLimitsRepository(ConfigRepository[TimeLimits], ABC):
    pass
