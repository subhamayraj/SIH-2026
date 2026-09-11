from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, CompetencyProfile, CompetencyFramework, Course, Recommendation

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/user/{user_id}")
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
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
        .order_by(CompetencyProfile.gap_score.desc())
        .all()
    )

    recommendations = []

    for profile, framework in profiles:
        if profile.gap_score <= 0:
            continue

        courses = (
            db.query(Course)
            .filter(Course.domain == framework.domain)
            .all()
        )

        for course in courses:
            existing = (
                db.query(Recommendation)
                .filter(
                    Recommendation.user_id == user_id,
                    Recommendation.course_id == course.id
                )
                .first()
            )

            if existing:
                match_score = existing.match_score
                reasoning = existing.reasoning
            else:
                match_score = min(100, 70 + int(profile.gap_score * 10))
                reasoning = (
                    f"Recommended because the employee has a competency gap "
                    f"in {framework.skill_name}."
                )

                new_recommendation = Recommendation(
                    user_id=user_id,
                    course_id=course.id,
                    match_score=match_score,
                    status="recommended",
                    reasoning=reasoning
                )

                db.add(new_recommendation)
                db.commit()

            recommendations.append({
                "skill": framework.skill_name,
                "domain": framework.domain,
                "gap_score": float(profile.gap_score),
                "course_id": course.id,
                "course_title": course.title,
                "provider": course.provider,
                "difficulty": course.difficulty,
                "match_score": match_score,
                "reasoning": reasoning
            })

    return {
        "user_id": user.id,
        "user_name": user.name,
        "recommendations": recommendations
    }