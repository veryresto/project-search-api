from fastapi import FastAPI, Query, HTTPException, status
from app.schemas import ProjectResponse, ErrorResponse
from app.service import fetch_projects
from typing import Optional

app = FastAPI(title="Project Search API", version="1.0.0")

@app.get("/")
def read_root():
    """Simple root message."""
    return {"message": "Welcome to the Project Search API. Use /projects to fetch project data."}

@app.get("/projects", response_model=ProjectResponse, responses={400: {"model": ErrorResponse}})
def get_projects(
    area: str = Query(..., description="Area to filter projects by"),
    page: int = Query(1, gt=0, description="Page number (1-based)"),
    per_page: int = Query(10, gt=0, description="Number of items per page")
):
    """
    Returns construction project data filtered by area.
    """
    # area must be non-empty
    if not area.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Area must be provided and non-empty."
        )
    
    try:
        # Business logic orchestrated by service layer
        return fetch_projects(area=area, page=page, per_page=per_page)
    except Exception as e:
        # Logging here could be added as a bonus (impl note in spec)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database or internal error: {str(e)}"
        )

# For running with uvicorn directly if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
