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