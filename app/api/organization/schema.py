from pydantic import BaseModel

from app.api.organization.enums import SubscriptionPan

class CreateOrganizationRequest(BaseModel):
    name: str 
    industry: str 
    subscription_plan: SubscriptionPan
    is_active: bool 