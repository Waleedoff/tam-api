from enum import Enum



class BaseEnum(Enum):
    def __str__(self):
        return self.value

class AnnouncementStatus(str, BaseEnum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"



class VoteType(str, Enum):
    HELPFUL = "HELPFUL"
    UNHELPFUL = "UNHELPFUL"