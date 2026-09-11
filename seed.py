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

try:
    user1 = User(
        name="Rahul Sharma",
        email="rahul.sharma@example.com",
        role="employee",
        department="Official Statistics",
        designation="Statistical Officer",
        hashed_password="demo_password"
    )

    user2 = User(
        name="Priya Das",
        email="priya.das@example.com",
        role="employee",
        department="Data Analytics",
        designation="Data Analyst",
        hashed_password="demo_password"
    )

    user3 = User(
        name="Amit Kumar",
        email="amit.kumar@example.com",
        role="admin",
        department="Training and Capacity Building",
        designation="Training Manager",
        hashed_password="demo_password"
    )

    db.add_all([user1, user2, user3])
    db.commit()

    competency1 = CompetencyFramework(
        domain="Data Analytics",
        skill_name="SQL",
        description="Ability to query, manage and analyze structured data using SQL.",
        required_level=4
    )

    competency2 = CompetencyFramework(
        domain="Data Analytics",
        skill_name="Python",
        description="Ability to use Python for data processing and analysis.",
        required_level=4
    )

    competency3 = CompetencyFramework(
        domain="Statistics",
        skill_name="Statistical Analysis",
        description="Ability to apply statistical methods for official statistical analysis.",
        required_level=5
    )

    competency4 = CompetencyFramework(
        domain="Data Visualization",
        skill_name="Data Visualization",
        description="Ability to communicate statistical insights using effective visualizations.",
        required_level=4
    )

    competency5 = CompetencyFramework(
        domain="Artificial Intelligence",
        skill_name="Machine Learning",
        description="Understanding of machine learning concepts and practical applications.",
        required_level=3
    )

    db.add_all([
        competency1,
        competency2,
        competency3,
        competency4,
        competency5
    ])
    db.commit()

    profile1 = CompetencyProfile(
        user_id=user1.id,
        skill_id=competency1.id,
        current_level=2,
        gap_score=2
    )

    profile2 = CompetencyProfile(
        user_id=user1.id,
        skill_id=competency2.id,
        current_level=3,
        gap_score=1
    )

    profile3 = CompetencyProfile(
        user_id=user2.id,
        skill_id=competency1.id,
        current_level=3,
        gap_score=1
    )

    profile4 = CompetencyProfile(
        user_id=user2.id,
        skill_id=competency3.id,
        current_level=2,
        gap_score=3
    )

    profile5 = CompetencyProfile(
        user_id=user2.id,
        skill_id=competency4.id,
        current_level=3,
        gap_score=1
    )

    db.add_all([
        profile1,
        profile2,
        profile3,
        profile4,
        profile5
    ])
    db.commit()

    course1 = Course(
        title="SQL for Data Analysis",
        description="Learn SQL fundamentals and advanced querying techniques for data analysis.",
        provider="iGOT Karmayogi",
        duration="20 hours",
        domain="Data Analytics",
        difficulty="Intermediate",
        url="https://example.com/sql-course"
    )

    course2 = Course(
        title="Python for Data Analysis",
        description="Learn Python, Pandas and data processing techniques.",
        provider="iGOT Karmayogi",
        duration="30 hours",
        domain="Data Analytics",
        difficulty="Intermediate",
        url="https://example.com/python-course"
    )

    course3 = Course(
        title="Applied Statistics for Official Statistics",
        description="Learn statistical methods used in official statistical systems.",
        provider="iGOT Karmayogi",
        duration="25 hours",
        domain="Statistics",
        difficulty="Advanced",
        url="https://example.com/statistics-course"
    )

    course4 = Course(
        title="Data Visualization Fundamentals",
        description="Learn how to create meaningful charts and dashboards from statistical data.",
        provider="iGOT Karmayogi",
        duration="15 hours",
        domain="Data Visualization",
        difficulty="Beginner",
        url="https://example.com/visualization-course"
    )

    course5 = Course(
        title="Introduction to Machine Learning",
        description="Understand machine learning concepts and practical applications.",
        provider="iGOT Karmayogi",
        duration="25 hours",
        domain="Artificial Intelligence",
        difficulty="Intermediate",
        url="https://example.com/ml-course"
    )

    db.add_all([
        course1,
        course2,
        course3,
        course4,
        course5
    ])
    db.commit()

    recommendation1 = Recommendation(
        user_id=user1.id,
        course_id=course1.id,
        match_score=92,
        status="recommended",
        reasoning="High competency gap in SQL compared with the required level."
    )

    recommendation2 = Recommendation(
        user_id=user1.id,
        course_id=course2.id,
        match_score=84,
        status="recommended",
        reasoning="Python competency is below the required level."
    )

    recommendation3 = Recommendation(
        user_id=user2.id,
        course_id=course3.id,
        match_score=95,
        status="recommended",
        reasoning="Large gap detected in Statistical Analysis."
    )

    recommendation4 = Recommendation(
        user_id=user2.id,
        course_id=course4.id,
        match_score=86,
        status="recommended",
        reasoning="Data Visualization competency can be improved to meet the required level."
    )

    db.add_all([
        recommendation1,
        recommendation2,
        recommendation3,
        recommendation4
    ])
    db.commit()

    enrollment1 = Enrollment(
        user_id=user1.id,
        course_id=course1.id,
        status="in_progress",
        progress_pct=45
    )

    enrollment2 = Enrollment(
        user_id=user2.id,
        course_id=course3.id,
        status="enrolled",
        progress_pct=10
    )

    enrollment3 = Enrollment(
        user_id=user2.id,
        course_id=course4.id,
        status="completed",
        progress_pct=100
    )

    db.add_all([
        enrollment1,
        enrollment2,
        enrollment3
    ])
    db.commit()

    material1 = LearningMaterial(
        uploaded_by=user3.id,
        filename="Official_Statistics_Data_Analysis.pdf",
        content_type="application/pdf",
        extracted_text="Official statistics involve the collection, processing, analysis and dissemination of reliable statistical information."
    )

    material2 = LearningMaterial(
        uploaded_by=user3.id,
        filename="Statistical_Methods.pdf",
        content_type="application/pdf",
        extracted_text="Statistical methods help organizations understand data, identify patterns and make evidence-based decisions."
    )

    db.add_all([
        material1,
        material2
    ])
    db.commit()

    quiz1 = Quiz(
        material_id=material1.id,
        title="Official Statistics Quiz",
        questions_json=[
            {
                "question": "What is the main purpose of official statistics?",
                "options": [
                    "Entertainment",
                    "Evidence-based decision making",
                    "Gaming",
                    "Social networking"
                ],
                "answer": "Evidence-based decision making"
            },
            {
                "question": "Which process is important in statistical analysis?",
                "options": [
                    "Data processing",
                    "Video editing",
                    "Graphic design",
                    "Music production"
                ],
                "answer": "Data processing"
            }
        ]
    )

    quiz2 = Quiz(
        material_id=material2.id,
        title="Statistical Methods Quiz",
        questions_json=[
            {
                "question": "What do statistical methods help identify?",
                "options": [
                    "Data patterns",
                    "Passwords",
                    "Computer hardware",
                    "Websites"
                ],
                "answer": "Data patterns"
            }
        ]
    )

    db.add_all([
        quiz1,
        quiz2
    ])
    db.commit()

    attempt1 = QuizAttempt(
        quiz_id=quiz1.id,
        user_id=user1.id,
        answers_json={
            "1": "Evidence-based decision making",
            "2": "Data processing"
        },
        score=2,
        max_score=2
    )

    attempt2 = QuizAttempt(
        quiz_id=quiz2.id,
        user_id=user2.id,
        answers_json={
            "1": "Data patterns"
        },
        score=1,
        max_score=1
    )

    db.add_all([
        attempt1,
        attempt2
    ])
    db.commit()

    print("Seed data inserted successfully!")
    print("Users:", db.query(User).count())
    print("Competencies:", db.query(CompetencyFramework).count())
    print("Competency Profiles:", db.query(CompetencyProfile).count())
    print("Courses:", db.query(Course).count())
    print("Recommendations:", db.query(Recommendation).count())
    print("Enrollments:", db.query(Enrollment).count())
    print("Learning Materials:", db.query(LearningMaterial).count())
    print("Quizzes:", db.query(Quiz).count())
    print("Quiz Attempts:", db.query(QuizAttempt).count())

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()