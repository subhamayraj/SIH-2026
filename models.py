from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="employee")
    department: Mapped[str | None] = mapped_column(String(100))
    designation: Mapped[str | None] = mapped_column(String(100))
    hashed_password: Mapped[str | None] = mapped_column(Text)

    competency_profiles: Mapped[list["CompetencyProfile"]] = relationship(
        back_populates="user"
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="user"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="user"
    )
    learning_materials: Mapped[list["LearningMaterial"]] = relationship(
        back_populates="uploader"
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="user"
    )


class CompetencyFramework(Base):
    __tablename__ = "competency_frameworks"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    required_level: Mapped[int] = mapped_column(default=1)

    profiles: Mapped[list["CompetencyProfile"]] = relationship(
        back_populates="skill"
    )


class CompetencyProfile(Base):
    __tablename__ = "competency_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("competency_frameworks.id"),
        nullable=False
    )
    current_level: Mapped[int] = mapped_column(default=0)
    gap_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    embedding: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(
        back_populates="competency_profiles"
    )
    skill: Mapped["CompetencyFramework"] = relationship(
        back_populates="profiles"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    provider: Mapped[str | None] = mapped_column(String(150))
    duration: Mapped[int | None] = mapped_column()
    domain: Mapped[str | None] = mapped_column(String(100))
    difficulty: Mapped[str | None] = mapped_column(String(50))
    url: Mapped[str | None] = mapped_column(Text)
    embedding: Mapped[str | None] = mapped_column(Text)

    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="course"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course"
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )
    match_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    status: Mapped[str] = mapped_column(
        String(30),
        default="recommended"
    )
    reasoning: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(
        back_populates="recommendations"
    )
    course: Mapped["Course"] = relationship(
        back_populates="recommendations"
    )


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="enrolled"
    )
    progress_pct: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0
    )
    enrolled_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    completed_at: Mapped[datetime | None] = mapped_column()

    user: Mapped["User"] = relationship(
        back_populates="enrollments"
    )
    course: Mapped["Course"] = relationship(
        back_populates="enrollments"
    )


class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    content_type: Mapped[str | None] = mapped_column(
        String(100)
    )
    extracted_text: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    uploader: Mapped["User"] = relationship(
        back_populates="learning_materials"
    )
    quizzes: Mapped[list["Quiz"]] = relationship(
        back_populates="material"
    )


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("learning_materials.id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    questions_json: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    material: Mapped["LearningMaterial"] = relationship(
        back_populates="quizzes"
    )
    attempts: Mapped[list["QuizAttempt"]] = relationship(
        back_populates="quiz"
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    answers_json: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )
    score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )
    max_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )
    attempted_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    quiz: Mapped["Quiz"] = relationship(
        back_populates="attempts"
    )
    user: Mapped["User"] = relationship(
        back_populates="quiz_attempts"
    )