from sqlalchemy.orm import Session
from app.api.organization.models import Organization
from app.api.organization.schema import CreateOrganizationRequest

def create_organization_(body: CreateOrganizationRequest, session: Session):
    
    new_org = Organization(**body.model_dump(), created_by="admin", id="xyz")
    session.add(new_org)
