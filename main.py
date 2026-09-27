from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import db
from routers.competencies import router as competency_router
from routers.recommendations import router as recommendations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(
    title="KarmaPathAI API",
    description="AI-enabled learning platform for Official Statistical System",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(competency_router)
app.include_router(recommendations_router)


@app.get("/")
async def home():
    return {
        "message": "KarmaPathAI API is running!"
    }


@app.get("/users")
async def get_users():
    users = await db.users.find_many()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "designation": user.designation
        }
        for user in users
    ]


@app.get("/competencies")
async def get_competencies():
    profiles = await db.competency_profiles.find_many(
        include={
            "competency_frameworks": True
        }
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
        if profile.competency_frameworks
    ]


@app.get("/courses")
async def get_courses():
    courses = await db.courses.find_many()

    return [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "provider": course.provider,
            "duration": course.duration,
            "domain": course.domain,
            "difficulty": course.difficulty,
            "url": course.url
        }
        for course in courses
    ]


@app.get("/recommendations")
async def get_recommendations():
    recommendations = await db.recommendations.find_many(
        include={
            "courses": True
        }
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


@app.get("/enrollments")
async def get_enrollments():
    enrollments = await db.enrollments.find_many(
        include={
            "courses": True
        }
    )

    return [
        {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course": (
                enrollment.courses.title
                if enrollment.courses
                else None
            ),
            "status": enrollment.status,
            "progress": float(
                enrollment.progress_pct or 0
            )
        }
        for enrollment in enrollments
    ]


@app.get("/learning-materials")
async def get_learning_materials():
    materials = await db.learning_materials.find_many()

    return [
        {
            "id": material.id,
            "uploaded_by": material.uploaded_by,
            "filename": material.filename,
            "content_type": material.content_type,
            "extracted_text": material.extracted_text
        }
        for material in materials
    ]


@app.get("/quizzes")
async def get_quizzes():
    quizzes = await db.quizzes.find_many()

    return [
        {
            "id": quiz.id,
            "material_id": quiz.material_id,
            "title": quiz.title,
            "questions": quiz.questions_json
        }
        for quiz in quizzes
    ]


@app.get("/quiz-attempts")
async def get_quiz_attempts():
    attempts = await db.quiz_attempts.find_many()

    return [
        {
            "id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "user_id": attempt.user_id,
            "answers": attempt.answers_json,
            "score": float(attempt.score or 0),
            "max_score": float(attempt.max_score or 0)
        }
        for attempt in attempts
    ]