from fastapi import APIRouter, HTTPException

from database import db

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/{user_id}")
async def get_user_recommendations(user_id: int):

    recommendations = await db.recommendations.find_many(
        where={"user_id": user_id},
        include={
            "courses": True
        },
        order={
            "match_score": "desc"
        }
    )

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found for this user"
        )

    return [
        {
            "id": recommendation.id,
            "user_id": recommendation.user_id,
            "course": (
                recommendation.courses.title
                if recommendation.courses
                else None
            ),
            "match_score": float(
                recommendation.match_score or 0
            ),
            "status": recommendation.status,
            "reasoning": recommendation.reasoning
        }
        for recommendation in recommendations
    ]