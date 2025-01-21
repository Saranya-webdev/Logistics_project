"""Fix tax_id column type

Revision ID: ae906cabb074
Revises: 
Create Date: 2024-12-29 17:19:08.498831

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'ae906cabb074'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Alter the 'customer' table columns first
    op.alter_column('customer', 'customer_address',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.Text(),
                    existing_nullable=True)
    op.alter_column('customer', 'customer_mobile',
                    existing_type=mysql.VARCHAR(length=15),
                    type_=sa.String(15),
                    existing_nullable=True)
    op.alter_column('customer', 'customer_email',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=False)
    op.alter_column('customer', 'customer_city',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=False)
    op.alter_column('customer', 'customer_state',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=False)
    op.alter_column('customer', 'customer_country',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=False)
    op.alter_column('customer', 'customer_pincode',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=True)
    op.alter_column('customer', 'customer_geolocation',
                    existing_type=mysql.VARCHAR(length=255),
                    type_=sa.String(255),
                    existing_nullable=False)

    # Add the 'type_id' column and create foreign key
    op.add_column('customer', sa.Column('type_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_customer_type', 'customer', 'customer_types', ['type_id'], ['id'])

    # Alter 'customer_type' and 'customer_category' columns with Enum
    op.alter_column('customer', 'customer_type', type_=sa.Enum('individual', 'corporate', name="customer_type_enum"), existing_nullable=True)
    op.alter_column('customer', 'customer_category', type_=sa.Enum('tier_1', 'tier_2', 'tier_3', name="customer_category_enum"), existing_nullable=True)



    # Drop old columns (State, Pincode, Country)
    op.drop_column('customer', 'customer_state')
    op.drop_column('customer', 'customer_pincode')
    op.drop_column('customer', 'customer_country')

    # Drop tables (users and posts) if required
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('username', table_name='users')
    op.drop_table('users')

def downgrade() -> None:
    # Revert changes for 'customer'
    op.add_column('customer', sa.Column('State', mysql.VARCHAR(length=250), nullable=True))
    op.add_column('customer', sa.Column('Pincode', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('customer', sa.Column('Country', mysql.VARCHAR(length=250), nullable=True))

    # Revert column type changes
    op.alter_column('customer', 'updated_at',
                existing_type=sa.String(255),
                type_=sa.DateTime(),
                existing_nullable=True)
    op.alter_column('customer', 'created_at',
                existing_type=sa.String(255),
                type_=sa.DateTime(),
                existing_nullable=False)

    op.alter_column('customer', 'customer_mobile',
                    existing_type=sa.String(15),
                    type_=mysql.VARCHAR(length=15),
                    existing_nullable=True)

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
