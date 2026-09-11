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

db = SessionLocal()

print("\n===== KARMA PATH AI DATABASE =====")

print("\nUsers:")
for user in db.query(User).all():
    print(user.id, user.name, user.email)

print("\nCompetency Frameworks:")
for skill in db.query(CompetencyFramework).all():
    print(skill.id, skill.skill_name, "Required:", skill.required_level)

print("\nCompetency Profiles:")
for profile in db.query(CompetencyProfile).all():
    print(
        profile.id,
        "User:", profile.user_id,
        "Skill:", profile.skill_id,
        "Current:", profile.current_level,
        "Gap:", profile.gap_score
    )

print("\nCourses:")
for course in db.query(Course).all():
    print(course.id, course.title)

print("\nRecommendations:")
for recommendation in db.query(Recommendation).all():
    print(
        recommendation.id,
        "User:", recommendation.user_id,
        "Course:", recommendation.course_id,
        "Match:", recommendation.match_score
    )

print("\nEnrollments:")
for enrollment in db.query(Enrollment).all():
    print(
        enrollment.id,
        "User:", enrollment.user_id,
        "Course:", enrollment.course_id,
        "Progress:", enrollment.progress_pct
    )

print("\nLearning Materials:")
for material in db.query(LearningMaterial).all():
    print(material.id, material.filename)

print("\nQuizzes:")
for quiz in db.query(Quiz).all():
    print(quiz.id, quiz.title)

print("\nQuiz Attempts:")
for attempt in db.query(QuizAttempt).all():
    print(
        attempt.id,
        "Quiz:", attempt.quiz_id,
        "User:", attempt.user_id,
        "Score:", attempt.score,
        "/", attempt.max_score
    )

print("\n===== DATABASE VERIFICATION COMPLETE =====")

db.close()