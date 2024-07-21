
from pydantic import BaseModel, constr, EmailStr
from typing import List
from datetime import datetime

class User(BaseModel):
    id: int | None
    github_username: constr(min_length=1, max_length=255)  
    name: str | None
    email: str | None
    bio: str | None
    location: str | None
    created_at: datetime | None
    is_recorded_fd: bool  | None
    freshdesk_contact_id: int  | None
    
    @classmethod
    def from_query_result(cls, id, github_username, name, email, bio, location, created_at, is_recorded_fd, freshdesk_contact_id):
        return cls(
            id=id, 
            github_username=github_username, 
            name=name, 
            email=email, 
            bio=bio, 
            location=location, 
            created_at=created_at, 
            is_recorded_fd=is_recorded_fd, 
            freshdesk_contact_id=freshdesk_contact_id,
            )

