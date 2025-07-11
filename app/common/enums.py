from collections.abc import Collection
from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value

    @classmethod
    def list(cls):
        return [attr.value for attr in cls]
        # return list(map(lambda c: c.value, cls))

    @classmethod
    def set(cls):
        return {attr.value for attr in cls}
        # return list(map(lambda c: c.value, cls))

    @classmethod
    def validate_item(cls, item):
        return item in cls.list()

    @classmethod
    def validate_items(cls, items: Collection):
        return cls.set() & set(items) == len(items)

class LoggingLevel(str, BaseEnum):
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class EmailTemplate(str, BaseEnum):
    COMPLETED_TASK = "completed_task.html"
