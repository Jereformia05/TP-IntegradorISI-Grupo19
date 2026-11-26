"""agregar tabla questions

Revision ID: 949c9bb04001
Revises: 50251a33219b
Create Date: 2026-11-25 12:41:25.093416

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "949c9bb04001"
down_revision: str | Sequence[str] | None = "50251a33219b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("questions", schema=None, recreate="always") as batch_op:
        batch_op.create_foreign_key(
            "fk_questions_user_id_users", "users", ["user_id"], ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("questions", schema=None, recreate="always") as batch_op:
        batch_op.drop_constraint("fk_questions_user_id_users", type_="foreignkey")
        batch_op.drop_column("category_id")
        batch_op.drop_column("user_id")
        batch_op.drop_column("created_at")
        batch_op.drop_column("text")
        batch_op.drop_column("title")
