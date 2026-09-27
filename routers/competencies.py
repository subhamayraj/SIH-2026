from fastapi import APIRouter, HTTPException
from database import db

router = APIRouter(
    prefix="/competencies",
    tags=["Competencies"]
)


@router.get("/{user_id}")
async def get_user_competencies(user_id: int):

    profiles = await db.competency_profiles.find_many(
        where={"user_id": user_id},
        include={
            "competency_frameworks": True
        }
    )

    if not profiles:
        raise HTTPException(
            status_code=404,
            detail="No competency data found for this user"
        )

    return [
        {
            "skill": profile.competency_frameworks.skill_name,
            "domain": profile.competency_frameworks.domain,
            "current_level": profile.current_level,
            "required_level": profile.competency_frameworks.required_level,
            "gap_score": float(profile.gap_score or 0)
        }
        for profile in profiles
    ]