from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value


class SubscriptionPan(str, BaseEnum):
    STARTUP = 'STARTUP'
    GROWTH = 'GROWTH'
    ENTRPRISE = 'ENTRPRISE'
