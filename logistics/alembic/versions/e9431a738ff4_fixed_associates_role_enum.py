"""Fixed associates_role Enum

Revision ID: e9431a738ff4
Revises: 679d952e1332
Create Date: 2025-01-25 02:07:15.721903
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.engine.reflection import Inspector

# Revision identifiers, used by Alembic.
revision: str = 'e9431a738ff4'
down_revision: Union[str, None] = '679d952e1332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Bind the current connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Drop the 'associates_email' index if it exists
    indexes = [index['name'] for index in inspector.get_indexes('associate')]
    if 'associates_email' in indexes:
        op.drop_index('associates_email', table_name='associate')

    # Drop the 'associates_mobile' index if it exists
    if 'associates_mobile' in indexes:
        op.drop_index('associates_mobile', table_name='associate')

    # Drop the 'associate' table if it exists
    if inspector.has_table('associate'):
        op.drop_table('associate')

    # Drop the 'email_id' index from 'associate_credentials' if it exists
    indexes_credentials = [index['name'] for index in inspector.get_indexes('associate_credentials')]
    if 'email_id' in indexes_credentials:
        op.drop_index('email_id', table_name='associate_credentials')

    # Drop the 'associate_credentials' table if it exists
    if inspector.has_table('associate_credentials'):
        op.drop_table('associate_credentials')

    # Alter the column in the 'carrier' table
    op.alter_column('carrier', 'is_active',
                    existing_type=mysql.TINYINT(display_width=1),
                    comment='Indicates if the carrier is active or not',
                    existing_nullable=True,
                    existing_server_default=sa.text("'1'"))


def downgrade() -> None:
    # Recreate the 'associate_credentials' table
    op.create_table('associate_credentials',
        sa.Column('associate_credential_id', mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('email_id', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('password', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('associates_id', mysql.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['associates_id'], ['associate.associates_id'], name='associate_credentials_ibfk_1', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('associate_credential_id'),
        mysql_collate='utf8mb4_0900_ai_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_index('email_id', 'associate_credentials', ['email_id'], unique=True)

    # Recreate the 'associate' table with fixed associates_role enum
    op.create_table('associate',
        sa.Column('associates_id', mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('associates_name', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('associates_email', mysql.VARCHAR(length=255), nullable=False),
        sa.Column('associates_mobile', mysql.VARCHAR(length=15), nullable=False),
        sa.Column('associates_roles', mysql.ENUM('admin','super_admin'), nullable=False),
        sa.Column('associates_verification_status', mysql.ENUM('none', 'pending', 'verified'), server_default=sa.text("'none'"), nullable=True),
        sa.Column('remarks', mysql.VARCHAR(length=255), nullable=True),
        sa.PrimaryKeyConstraint('associates_id'),
        mysql_collate='utf8mb4_0900_ai_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_index('associates_mobile', 'associate', ['associates_mobile'], unique=True)
    op.create_index('associates_email', 'associate', ['associates_email'], unique=True)

    # Revert the column alteration in the 'carrier' table
    op.alter_column('carrier', 'is_active',
                    existing_type=mysql.TINYINT(display_width=1),
                    comment=None,
                    existing_nullable=True,
                    existing_server_default=sa.text("'1'"))
