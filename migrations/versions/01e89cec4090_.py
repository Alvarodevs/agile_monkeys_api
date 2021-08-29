"""empty message

Revision ID: 01e89cec4090
Revises: 93ff31a6d9ba
Create Date: 2021-08-29 00:14:43.965516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e89cec4090'
down_revision = '93ff31a6d9ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'customers', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'admin', ['admin_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'admin_id')
    op.drop_constraint(None, 'customers', type_='foreignkey')
    op.drop_column('customers', 'user_id')
    # ### end Alembic commands ###
