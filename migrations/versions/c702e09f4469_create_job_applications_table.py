"""create job_applications table

Revision ID: c702e09f4469
Revises: 123f42e545ca
Create Date: 2025-11-25 15:13:16.670954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c702e09f4469'
down_revision: Union[str, Sequence[str], None] = '123f42e545ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "job_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_post_id", sa.Integer(), sa.ForeignKey("job_posts.id"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("resume_url", sa.String(), nullable=False)
    )

def downgrade():
    op.drop_table("job_applications")
