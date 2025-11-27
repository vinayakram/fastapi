"""add status to job_posts

Revision ID: 123f42e545ca
Revises: 2355b6ab3f23
Create Date: 2025-11-25 15:02:09.911724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '123f42e545ca'
down_revision: Union[str, Sequence[str], None] = '2355b6ab3f23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("job_posts", sa.Column("status", sa.String(20), server_default="open", nullable=False))

def downgrade():
    op.drop_column("job_posts", "status")

