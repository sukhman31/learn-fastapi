"""create posts table

Revision ID: 7a757e714a08
Revises: 
Create Date: 2023-07-09 19:06:45.063332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a757e714a08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False, primary_key=True),
                    sa.Column('title',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
