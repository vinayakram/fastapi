"""add cascade job applications

Revision ID: db0c49040049
Revises: ae8c973ce54f
Create Date: 2025-11-25 16:58:50.294322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db0c49040049'
down_revision: Union[str, Sequence[str], None] = 'ae8c973ce54f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1️⃣ Drop old foreign key (no cascade)
    op.drop_constraint(
        'job_applications_job_post_id_fkey',
        'job_applications',
        type_='foreignkey'
    )

    # 2️⃣ Create new FK with ON DELETE CASCADE
    op.create_foreign_key(
        None,                         # Alembic will auto-name the constraint
        'job_applications',           # Source table
        'job_posts',                  # Referenced table
        ['job_post_id'],              # Column in job_applications
        ['id'],                       # Column in job_posts
        ondelete='CASCADE'            # ⭐ enable cascade
    )


def downgrade():
    # 1️⃣ Remove the cascade-enabled FK
    op.drop_constraint(
        None,
        'job_applications',
        type_='foreignkey'
    )

    # 2️⃣ Recreate the original FK WITHOUT cascade
    op.create_foreign_key(
        'job_applications_job_post_id_fkey',  # explicit name
        'job_applications',                   # table
        'job_posts',                          # referenced table
        ['job_post_id'],                      # local column
        ['id'],                               # referenced column
        ondelete=None                         # ❌ no cascade
    )

