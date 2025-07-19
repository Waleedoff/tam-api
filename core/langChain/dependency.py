



# from app.api.auth.schema import UserResponse
# from app.api.auth.services.authSetup import get_current_active_user
# from app.common.enums import Department, Role


# def can_use_ai_agent_dependency(
#     current_user: UserResponse = get_current_active_user
# ):
#     if current_user.role == Role.SPECIALIST:
#         return
#     if current_user.role == Role.SPECIALIST and current_user.department in [Department.BUSINESS, Department.HR, Department.FINAINC]:
#         return
#     raise Exception(
#         status_code=403,
#         detail="❌ لا تملك صلاحية استخدام هذه الميزة.",
#     )