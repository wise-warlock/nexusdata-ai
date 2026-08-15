from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    BUILDER = "builder"
    VIEWER = "viewer"
    RAG_ENGINEER = "rag_engineer"

class User(BaseModel):
    id: str
    username: str
    role: UserRole
    email: str

DEFAULT_USERS: Dict[str, User] = {
    "admin": User(id="usr_1", username="admin", role=UserRole.ADMIN, email="admin@nexusdata.ai"),
    "analyst": User(id="usr_2", username="analyst", role=UserRole.ANALYST, email="analyst@nexusdata.ai"),
    "builder": User(id="usr_3", username="builder", role=UserRole.BUILDER, email="builder@nexusdata.ai"),
    "viewer": User(id="usr_4", username="viewer", role=UserRole.VIEWER, email="viewer@nexusdata.ai"),
    "rag_eng": User(id="usr_5", username="rag_eng", role=UserRole.RAG_ENGINEER, email="rag_eng@nexusdata.ai"),
}

def get_current_user(role_name: Optional[str] = "analyst") -> User:
    """Return user object based on role header or default to analyst"""
    return DEFAULT_USERS.get((role_name or "analyst").lower(), DEFAULT_USERS["analyst"])

def check_permission(user: User, allowed_roles: List[UserRole]) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    return user.role in allowed_roles