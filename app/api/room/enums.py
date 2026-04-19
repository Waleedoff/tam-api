from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return self.value



class ProjectStatus(str, BaseEnum):
    DRAFT = 'DRAFT'
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    ACHIEVED = 'ARCHIEVED'
    

class PublishingStatus(str, BaseEnum):
    PUBLISHED = 'PUBLISHED'
    DRAFT = 'DRAFT'
    DELETED = 'DELETED'


class Methdology(str, BaseEnum):
    KANBAN = 'KANBAN'
    SCRUM = 'SCRUM'
    HYBIRD = 'HYBIRD'


class Visibility(str, BaseEnum):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    INTERNAL = 'INTERNAL'


class RoomMemberRole(str, Enum):
    ADMIN  = "admin"
    PO     = "po"       # Product Owner
    MEMBER = "member"
    VIEWER = "viewer"

class RoomMemberStatus(str, Enum):
    INVITED = "invited"
    ACTIVE  = "active"
    LEFT    = "left"
    
class WorkItemType(str, Enum):
    STORY = 'STORY'
    BUG = 'BUG'
    SPIK = 'SPIK'

class UserStoryStatus(str, Enum):
    STARTED = 'STARTED'
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    READY = 'READY'
    DONE = 'DONE'

class SprintStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    PLANNED = 'PLANNED'
    COMPLETED = 'COMPLETED'
