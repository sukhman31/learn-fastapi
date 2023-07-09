"""add content column to posts table

Revision ID: 09304deab2cb
Revises: 7a757e714a08
Create Date: 2023-07-09 19:11:03.535818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09304deab2cb'
down_revision = '7a757e714a08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
