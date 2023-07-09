"""add fkey to post table

Revision ID: 12c1e37745b7
Revises: c602e8e185cd
Create Date: 2023-07-09 19:38:31.994227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c1e37745b7'
down_revision = 'c602e8e185cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts',referent_table='users',local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
