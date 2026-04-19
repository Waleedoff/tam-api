from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value

class BacklogType(str, BaseEnum):
    BUG = 'BUG'
    FEAT = 'feature'
    ENC = 'ENC'