"""Endpoints updated, Admin w. password + jwtToken, reordered tables fields

Revision ID: 27ba512f735e
Revises: 01e89cec4090
Create Date: 2021-08-29 01:21:55.469718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27ba512f735e'
down_revision = '01e89cec4090'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('user_name', sa.String(length=30), nullable=False))
    op.add_column('admin', sa.Column('password', sa.String(length=80), nullable=False))
    op.create_unique_constraint(None, 'admin', ['password'])
    op.create_unique_constraint(None, 'admin', ['user_name'])
    op.add_column('customers', sa.Column('user_id_creator', sa.Integer(), nullable=True))
    op.drop_constraint('customers_user_id_fkey', 'customers', type_='foreignkey')
    op.create_foreign_key(None, 'customers', 'users', ['user_id_creator'], ['id'])
    op.drop_column('customers', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.create_foreign_key('customers_user_id_fkey', 'customers', 'users', ['user_id'], ['id'])
    op.drop_column('customers', 'user_id_creator')
    op.drop_constraint(None, 'admin', type_='unique')
    op.drop_constraint(None, 'admin', type_='unique')
    op.drop_column('admin', 'password')
    op.drop_column('admin', 'user_name')
    # ### end Alembic commands ###