from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProjectBase(BaseModel):
    project_name: str
    project_start: str # SQLite dates are often strings
    project_end: str
    company: str
    description: Optional[str] = None
    project_value: int

class ProjectResponse(BaseModel):
    area: str
    page: int
    per_page: int
    total: int
    projects: List[ProjectBase]

class ErrorResponse(BaseModel):
    error: str
