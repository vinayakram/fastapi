"""add cascade delete

Revision ID: ae8c973ce54f
Revises: c702e09f4469
Create Date: 2025-11-25 16:47:44.208929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae8c973ce54f'
down_revision: Union[str, Sequence[str], None] = 'c702e09f4469'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the old FK constraint
    op.drop_constraint(
        'job_posts_job_board_id_fkey',
        'job_posts',
        type_='foreignkey'
    )

    # Create FK with ON DELETE CASCADE
    op.create_foreign_key(
        None,                  # Alembic will generate a name
        'job_posts',           # source table
        'job_boards',          # referent table
        ['job_board_id'],      # source column
        ['id'],                # referent column
        ondelete='CASCADE'     # ⭐ THIS IS THE IMPORTANT PART
    )


def downgrade():
    # Drop the cascade FK
    op.drop_constraint(None, 'job_posts', type_='foreignkey')

    # Restore original FK (no cascade)
    op.create_foreign_key(
        'job_posts_job_board_id_fkey',
        'job_posts',
        'job_boards',
        ['job_board_id'],
        ['id']
    )

