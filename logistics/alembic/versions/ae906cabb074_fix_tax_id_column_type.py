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
    # Alter the 'customer' table columns first
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

    # Add the 'type_id' column and create foreign key
    op.add_column('customers', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_customer_type', 'customers', 'customer_types', ['type_id'], ['id'])

    # Drop the old 'type' column
    op.drop_column('customers', 'type')

    # Alter additional columns in the 'customers' table
    op.alter_column('customers', 'address',
                    existing_type=mysql.VARCHAR(length=250),
                    type_=sa.Text(),
                    existing_nullable=True)
    op.alter_column('customers', 'taxid',
                    existing_type=mysql.INTEGER(),
                    type_=sa.String(length=100),
                    existing_nullable=True)
    op.alter_column('customers', 'licensenumber',
                    type_=String(100),
                    existing_type=Integer)
    op.alter_column('customers', 'created_at',
                    existing_type=mysql.VARCHAR(length=100),
                    type_=sa.DateTime(),
                    existing_nullable=True)
    op.alter_column('customers', 'updated_at',
                    existing_type=mysql.VARCHAR(length=250),
                    type_=sa.DateTime(),
                    existing_nullable=True)

    # Add new columns (state, pincode, country)
    op.add_column('customers', sa.Column('state', sa.String(length=250), nullable=True))
    op.add_column('customers', sa.Column('pincode', sa.Integer(), nullable=True))
    op.add_column('customers', sa.Column('country', sa.String(length=250), nullable=True))

    # Alter mobile column length
    op.alter_column('customers', 'mobile',
                    existing_type=sa.Integer,
                    type_=sa.String(15),  # Adjust length as per your requirement
                    nullable=True)

    # Drop old columns (State, Pincode, Country)
    op.drop_column('customers', 'State')  # Verify column names (case-sensitive)
    op.drop_column('customers', 'Pincode')
    op.drop_column('customers', 'Country')

    # Drop tables (users and posts) if required
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('username', table_name='users')
    op.drop_table('users')

def downgrade() -> None:
    # Revert changes for 'customers'
    op.add_column('customers', sa.Column('State', mysql.VARCHAR(length=250), nullable=True))
    op.add_column('customers', sa.Column('Pincode', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('customers', sa.Column('Country', mysql.VARCHAR(length=250), nullable=True))

    # Revert column type changes
    op.alter_column('customers', 'updated_at',
                    existing_type=sa.DateTime(),
                    type_=mysql.VARCHAR(length=250),
                    existing_nullable=True)
    op.alter_column('customers', 'created_at',
                    existing_type=sa.DateTime(),
                    type_=mysql.VARCHAR(length=100),
                    existing_nullable=True)
    op.alter_column('customers', 'licensenumber',
                    existing_type=sa.String(length=100),
                    type_=mysql.INTEGER(),
                    existing_nullable=True)
    op.alter_column('customers', 'taxid',
                    existing_type=sa.String(length=100),
                    type_=mysql.INTEGER(),
                    existing_nullable=True)
    op.alter_column('customers', 'address',
                    existing_type=sa.Text(),
                    type_=mysql.VARCHAR(length=250),
                    existing_nullable=True)
    op.alter_column('customers', 'mobile',
                    existing_type=sa.String(length=15),
                    type_=sa.Integer(),
                    nullable=True)

    # Recreate tables (users and posts)
    op.create_table('users',
                    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('username', mysql.VARCHAR(length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB')
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
                    mysql_engine='InnoDB')
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)
