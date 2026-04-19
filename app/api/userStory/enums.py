from enum import Enum



class BaseEnum(Enum):
    def __str__(self):
        return self.value



class UserStoryStatus(str, BaseEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"



class ActorType(str, BaseEnum):
    USER = "USER"
    ADMIN = "ADMIN"
    GUEST = "GUEST"
    OTHER = "OTHER"
    
    
class PipelineStage(str, BaseEnum):
    IDEA = 'IDEA'
    READY = 'READY'
    NEXT = 'NEXT'
    ACHIEVED = 'ACHIEVED'