from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.models import Project, User  # Assumes SQLAlchemy models
from app.database import get_db  # Assumes a dependency for DB session
from sqlalchemy.orm import Session

router = APIRouter()

# Dummy dependency for current user (replace with real auth in production)
def get_current_user():
    # In production, extract user info from JWT/session
    # Here, just a placeholder user for demonstration
    return User(id=1, username="teacher1", role="teacher1")

class ApproveProjectRequest(BaseModel):
    project_id: int
    approve: bool
    feedback: Optional[str] = None

@router.patch("/approve_project")
def approve_project(
    req: ApproveProjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher1":
        raise HTTPException(status_code=403, detail="Not authorized")
    project = db.query(Project).filter(Project.id == req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.approved = req.approve
    project.feedback = req.feedback
    db.commit()
    return {"status": "success", "approved": req.approve}

class CompleteProjectRequest(BaseModel):
    project_id: int
    final_report_url: str

@router.post("/complete_project")
def complete_project(
    req: CompleteProjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher2":
        raise HTTPException(status_code=403, detail="Not authorized")
    project = db.query(Project).filter(Project.id == req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.final_report_url = req.final_report_url
    project.completed = True
    db.commit()
    return {"status": "success", "completed": True}