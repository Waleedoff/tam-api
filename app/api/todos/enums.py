from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value




class Status(str, BaseEnum):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

class Priority(str, BaseEnum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'
