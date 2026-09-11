from fastapi import FastAPI
from routers.competencies import router as competency_router
from database import SessionLocal
from models import (
    User,
    CompetencyFramework,
    CompetencyProfile,
    Course,
    Recommendation,
    Enrollment,
    LearningMaterial,
    Quiz,
    QuizAttempt
)

app = FastAPI(
    title="KarmaPathAI API",
    description="AI-enabled learning platform for Official Statistical System",
    version="1.0.0"
)
app.include_router(competency_router)


@app.get("/")
def home():
    return {"message": "KarmaPathAI API is running!"}


@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()

    result = [
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

    db.close()
    return result


@app.get("/competencies")
def get_competencies():
    db = SessionLocal()
    profiles = db.query(CompetencyProfile).all()

    result = []

    for profile in profiles:
        skill = db.query(CompetencyFramework).filter(
            CompetencyFramework.id == profile.skill_id
        ).first()

        result.append({
            "skill": skill.skill_name,
            "domain": skill.domain,
            "current_level": profile.current_level,
            "required_level": skill.required_level,
            "gap_score": float(profile.gap_score)
        })

    db.close()
    return result


@app.get("/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()

    result = [
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

    db.close()
    return result


@app.get("/recommendations")
def get_recommendations():
    db = SessionLocal()
    recommendations = db.query(Recommendation).all()

    result = []

    for recommendation in recommendations:
        course = db.query(Course).filter(
            Course.id == recommendation.course_id
        ).first()

        result.append({
            "id": recommendation.id,
            "user_id": recommendation.user_id,
            "course": course.title,
            "match_score": float(recommendation.match_score),
            "status": recommendation.status,
            "reasoning": recommendation.reasoning
        })

    db.close()
    return result


@app.get("/enrollments")
def get_enrollments():
    db = SessionLocal()
    enrollments = db.query(Enrollment).all()

    result = []

    for enrollment in enrollments:
        course = db.query(Course).filter(
            Course.id == enrollment.course_id
        ).first()

        result.append({
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course": course.title,
            "status": enrollment.status,
            "progress": float(enrollment.progress_pct)
        })

    db.close()
    return result


@app.get("/learning-materials")
def get_learning_materials():
    db = SessionLocal()
    materials = db.query(LearningMaterial).all()

    result = [
        {
            "id": material.id,
            "uploaded_by": material.uploaded_by,
            "filename": material.filename,
            "content_type": material.content_type,
            "extracted_text": material.extracted_text
        }
        for material in materials
    ]

    db.close()
    return result


@app.get("/quizzes")
def get_quizzes():
    db = SessionLocal()
    quizzes = db.query(Quiz).all()

    result = [
        {
            "id": quiz.id,
            "material_id": quiz.material_id,
            "title": quiz.title,
            "questions": quiz.questions_json
        }
        for quiz in quizzes
    ]

    db.close()
    return result


@app.get("/quiz-attempts")
def get_quiz_attempts():
    db = SessionLocal()
    attempts = db.query(QuizAttempt).all()

    result = [
        {
            "id": attempt.id,
            "quiz_id": attempt.quiz_id,
            "user_id": attempt.user_id,
            "answers": attempt.answers_json,
            "score": float(attempt.score),
            "max_score": float(attempt.max_score)
        }
        for attempt in attempts
    ]

    db.close()
    return result