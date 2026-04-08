from app.db import get_projects_by_area
from app.schemas import ProjectResponse, ProjectBase
from typing import List, Dict, Any

def fetch_projects(area: str, page: int, per_page: int) -> ProjectResponse:
    """
    Business logic layer for fetching projects.
    """
    projects_list, total_count = get_projects_by_area(area, page, per_page)
    
    # Transformation to match the response schema
    projects = [ProjectBase(**p) for p in projects_list]
    
    return ProjectResponse(
        area=area,
        page=page,
        per_page=per_page,
        total=total_count,
        projects=projects
    )
