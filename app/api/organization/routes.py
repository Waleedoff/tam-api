
from fastapi import APIRouter

from app.api.organization.schema import CreateOrganizationRequest
from app.api.organization.service.create_organization import create_organization_
from app.api.organization.service.get_all_departments import get_all_departments_
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import  Session
router =  APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/organization"
tags = ["organization"]



@router.post('/')
def create_organization(body: CreateOrganizationRequest, session: Session = db_session):
    return create_organization_(body=body, session=session)

@router.get('/departments')
def get_all_departments(session: Session = db_session):
    return get_all_departments_(session=session)