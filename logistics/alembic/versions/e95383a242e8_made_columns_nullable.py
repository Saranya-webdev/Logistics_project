from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e95383a242e8'
down_revision: Union[str, None] = 'e9431a738ff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index('email_id', table_name='associates_credential')
    # op.drop_index('associates_id', table_name='associates_credential')
    op.drop_table('associates_credential')
    op.drop_index('associates_email', table_name='associate')
    op.drop_table('associate')
    
    # Modify columns in customer_business table (Add existing type)
    op.alter_column('customer_business', 'tax_id',
                    existing_type=sa.String(255), nullable=True)

    op.alter_column('customer_business', 'license',
                    existing_type=sa.String(255), nullable=True)

    op.alter_column('customer_business', 'company_name',
                    existing_type=sa.String(255), nullable=True)

    op.alter_column('customer_business', 'designation',
                    existing_type=sa.String(255), nullable=True)
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('associate',
    sa.Column('associates_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('associates_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('associates_mobile', mysql.VARCHAR(length=15), nullable=True),
    sa.Column('associates_email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('associates_role', mysql.ENUM('admin', 'super_admin'), nullable=False),
    sa.Column('verification_status', mysql.ENUM('none', 'pending', 'verified'), server_default=sa.text("'none'"), nullable=False),
    sa.Column('remarks', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('active_flag', mysql.INTEGER(), server_default=sa.text("'1'"), autoincrement=False, nullable=True),
    sa.Column('deleted', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"), autoincrement=False, nullable=True),
    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
    sa.Column('is_active', mysql.TINYINT(display_width=1), server_default=sa.text("'1'"), autoincrement=False, nullable=True, comment='Indicates if the associate is active or not'),
    sa.PrimaryKeyConstraint('associates_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('associates_email', 'associate', ['associates_email'], unique=True)
    op.create_table('associates_credential',
    sa.Column('associates_credential_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email_id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('associates_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='Indicates if the associate is active or not'),
    sa.ForeignKeyConstraint(['associates_id'], ['associate.associates_id'], name='associates_credential_ibfk_1'),
    sa.PrimaryKeyConstraint('associates_credential_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('idx_associates_id', 'associates_credential', ['associates_id'], unique=False)
    op.create_index('email_id', 'associates_credential', ['email_id'], unique=True)
    # ### end Alembic commands ###
