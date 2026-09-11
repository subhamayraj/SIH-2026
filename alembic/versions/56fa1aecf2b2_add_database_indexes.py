from typing import Sequence, Union

from alembic import op


revision: str = "56fa1aecf2b2"
down_revision: Union[str, Sequence[str], None] = "ad0fbded09e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_competency_profiles_user_id",
        "competency_profiles",
        ["user_id"]
    )
    op.create_index(
        "ix_competency_profiles_skill_id",
        "competency_profiles",
        ["skill_id"]
    )
    op.create_index(
        "ix_recommendations_user_id",
        "recommendations",
        ["user_id"]
    )
    op.create_index(
        "ix_recommendations_course_id",
        "recommendations",
        ["course_id"]
    )
    op.create_index(
        "ix_enrollments_user_id",
        "enrollments",
        ["user_id"]
    )
    op.create_index(
        "ix_enrollments_course_id",
        "enrollments",
        ["course_id"]
    )
    op.create_index(
        "ix_learning_materials_uploaded_by",
        "learning_materials",
        ["uploaded_by"]
    )
    op.create_index(
        "ix_quizzes_material_id",
        "quizzes",
        ["material_id"]
    )
    op.create_index(
        "ix_quiz_attempts_quiz_id",
        "quiz_attempts",
        ["quiz_id"]
    )
    op.create_index(
        "ix_quiz_attempts_user_id",
        "quiz_attempts",
        ["user_id"]
    )


def downgrade() -> None:
    op.drop_index(
        "ix_quiz_attempts_user_id",
        table_name="quiz_attempts"
    )
    op.drop_index(
        "ix_quiz_attempts_quiz_id",
        table_name="quiz_attempts"
    )
    op.drop_index(
        "ix_quizzes_material_id",
        table_name="quizzes"
    )
    op.drop_index(
        "ix_learning_materials_uploaded_by",
        table_name="learning_materials"
    )
    op.drop_index(
        "ix_enrollments_course_id",
        table_name="enrollments"
    )
    op.drop_index(
        "ix_enrollments_user_id",
        table_name="enrollments"
    )
    op.drop_index(
        "ix_recommendations_course_id",
        table_name="recommendations"
    )
    op.drop_index(
        "ix_recommendations_user_id",
        table_name="recommendations"
    )
    op.drop_index(
        "ix_competency_profiles_skill_id",
        table_name="competency_profiles"
    )
    op.drop_index(
        "ix_competency_profiles_user_id",
        table_name="competency_profiles"
    )