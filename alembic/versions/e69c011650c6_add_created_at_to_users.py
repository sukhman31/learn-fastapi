"""add created_at to users

Revision ID: e69c011650c6
Revises: ad5accec9c68
Create Date: 2023-07-09 19:57:06.806677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e69c011650c6'
down_revision = 'ad5accec9c68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('users','created_at')
    pass
