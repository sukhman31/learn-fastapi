"""drop created_at from users

Revision ID: ad5accec9c68
Revises: 4994093ccba9
Create Date: 2023-07-09 19:55:06.391545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad5accec9c68'
down_revision = '4994093ccba9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('users','created_at')
    pass


def downgrade() -> None:
    op.add_column('users',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False))
    pass
