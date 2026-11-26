"""merge multiples heads

Revision ID: e7a36528d037
Revises: 2236c0479dd2, 949c9bb04001
Create Date: 2026-11-26 03:38:58.222881

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "e7a36528d037"
down_revision: str | Sequence[str] | None = ("2236c0479dd2", "949c9bb04001")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
