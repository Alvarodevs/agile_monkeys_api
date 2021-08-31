"""empty message

Revision ID: 2bae68741b61
Revises: 5d854204202c
Create Date: 2021-08-31 16:04:14.692196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bae68741b61'
down_revision = '5d854204202c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('admin_name', sa.String(length=30), nullable=False))
    op.drop_constraint('admin_user_name_key', 'admin', type_='unique')
    op.create_unique_constraint(None, 'admin', ['admin_name'])
    op.drop_column('admin', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('user_name', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'admin', type_='unique')
    op.create_unique_constraint('admin_user_name_key', 'admin', ['user_name'])
    op.drop_column('admin', 'admin_name')
    # ### end Alembic commands ###