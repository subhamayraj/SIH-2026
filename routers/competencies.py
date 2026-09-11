from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, CompetencyProfile, CompetencyFramework

router = APIRouter(prefix="/competency", tags=["Competency Gap"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user/{user_id}")
def get_user_competency_gap(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profiles = (
        db.query(CompetencyProfile, CompetencyFramework)
        .join(
            CompetencyFramework,
            CompetencyProfile.skill_id == CompetencyFramework.id
        )
        .filter(CompetencyProfile.user_id == user_id)
        .all()
    )

    result = []

    for profile, framework in profiles:
        gap = max(framework.required_level - profile.current_level, 0)

        result.append({
            "skill": framework.skill_name,
            "domain": framework.domain,
            "required_level": framework.required_level,
            "current_level": profile.current_level,
            "gap_score": gap
        })

    return {
        "user_id": user.id,
        "user_name": user.name,
        "department": user.department,
        "designation": user.designation,
        "competency_gaps": result
    }