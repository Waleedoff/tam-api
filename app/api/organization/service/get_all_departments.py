from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.auth.models import User
from app.common.enums import Department

def get_all_departments_(session: Session):
    get_departments = [d.value for d in Department]
    
    stmt = select(User).where(User.organization_id == "xyz")
    members = session.execute(stmt).scalars().all()
    
    # Group users by department
    department_data = []
    for dep in get_departments:
        department_members = [
            {
                "username": member.username,
                "email": member.email,
                "role": member.role
            }
            for member in members
            if member.department == dep
        ]
        department_data.append({
            "department": dep,
            "members": department_members
        })

    return department_data
