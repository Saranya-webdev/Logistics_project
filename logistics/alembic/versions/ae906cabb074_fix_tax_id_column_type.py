"""Fix tax_id column type

Revision ID: ae906cabb074
Revises: 
Create Date: 2024-12-29 17:19:08.498831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import Integer, String

# revision identifiers, used by Alembic.
revision: str = 'ae906cabb074'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('username', table_name='users')
    op.drop_table('users')
    op.add_column('customer', sa.Column('state', sa.String(length=250), nullable=True))
    op.add_column('customer', sa.Column('pincode', sa.Integer(), nullable=True))
    op.add_column('customer', sa.Column('country', sa.String(length=250), nullable=True))
    op.alter_column('customer', 'address',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.Text(),
               existing_nullable=True)
    op.alter_column('customer', 'taxid',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('customer', 'licensenumber',
                    type_=String(100),
                    existing_type=Integer)
    op.alter_column('customer', 'created_at',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('customer', 'updated_at',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.drop_column('customer', 'State')
    op.drop_column('customer', 'Pincode')
    op.drop_column('customer', 'Country')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('Country', mysql.VARCHAR(length=250), nullable=True))
    op.add_column('customer', sa.Column('Pincode', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('customer', sa.Column('State', mysql.VARCHAR(length=250), nullable=True))
    op.alter_column('customer', 'updated_at',
               existing_type=sa.DateTime(),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=True)
    op.alter_column('customer', 'created_at',
               existing_type=sa.DateTime(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('customer', 'licensenumber',
               existing_type=sa.String(length=100),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('customer', 'taxid',
               existing_type=sa.String(length=100),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    op.alter_column('customer', 'address',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=True)
    op.drop_column('customer', 'country')
    op.drop_column('customer', 'pincode')
    op.drop_column('customer', 'state')
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('posts',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('content', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)
    # ### end Alembic commands ###
