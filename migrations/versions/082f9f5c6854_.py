"""empty message

Revision ID: 082f9f5c6854
Revises: 50e3c5c9f865
Create Date: 2021-08-31 02:21:48.813694

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '082f9f5c6854'
down_revision = '50e3c5c9f865'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('surname', sa.String(length=40), nullable=False),
    sa.Column('avatar_url', sa.String(length=300), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('modifications',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'customer_id')
    )
    op.drop_table('customers')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], name='users_admin_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('user_name', name='users_user_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('customers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('surname', sa.VARCHAR(length=40), autoincrement=False, nullable=False),
    sa.Column('avatar_url', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('modified_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id_creator', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_name_creator', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id_creator'], ['users.id'], name='customers_user_id_creator_fkey'),
    sa.PrimaryKeyConstraint('id', name='customers_pkey')
    )
    op.drop_table('modifications')
    op.drop_table('user')
    op.drop_table('customer')
    # ### end Alembic commands ###
