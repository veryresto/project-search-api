import sqlite3
import os
from typing import List, Dict, Any, Tuple

# Path to the database file relative to the project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sqlite3")

def get_connection():
    """Provides a sqlite3 connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

def get_projects_by_area(area: str, page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    """
    Fetches projects filtered by area with pagination and sorting.
    Returns a tuple of (projects_list, total_count).
    """
    offset = (page - 1) * per_page
    
    with get_connection() as conn:
        # 1. Total Count Query
        count_query = """
        SELECT COUNT(*) as total
        FROM project_area_map pam
        WHERE pam.area = ?
        """
        count_row = conn.execute(count_query, (area,)).fetchone()
        total_count = count_row["total"] if count_row else 0
        
        if total_count == 0:
            return [], 0
        
        # 2. Main Paginated Query
        # Join Logic: project_area_map -> projects -> companies
        projects_query = """
        SELECT
            p.project_name,
            p.project_start,
            p.project_end,
            c.company_name as company,
            p.description,
            p.project_value
        FROM project_area_map pam
        JOIN projects p ON pam.project_id = p.project_id
        JOIN companies c ON p.company_id = c.company_id
        WHERE pam.area = ?
        ORDER BY p.project_value DESC, p.project_name ASC
        LIMIT ? OFFSET ?
        """
        
        cursor = conn.execute(projects_query, (area, per_page, offset))
        projects = [dict(row) for row in cursor.fetchall()]
        
    return projects, total_count
