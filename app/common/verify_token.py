from jose import JWTError, jwt
from app.config import config
from app.api.auth.schema import UserResponse
from datetime import datetime

def verify_token(token: str) -> UserResponse:

        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.ALGORITHM)
        user_id: str = payload.get("id")
        


        role: str = payload.get("role")
        department: str = payload.get("department")
        if user_id is None :
            return None
 
        return UserResponse(
            id=user_id,
            role=role,
            department=department,
        )

   
