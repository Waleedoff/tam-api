from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value




class PublishingStatus(str, BaseEnum):
    PUBLISHED = 'PUBLISHED'
    DRAFT = 'DRAFT'
    DELETED = 'DELETED'
