"""rename student column

Revision ID: 3652ac23b89d
Revises: 0d5fa0176de6
Create Date: 2018-09-14 10:38:35.784912

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3652ac23b89d'
down_revision = '0d5fa0176de6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('competition_signup', 'student_name',
                    new_column_name='student1_name', existing_type=sa.VARCHAR(100), existing_nullable=True)
    op.alter_column('competition_signup', 'student_class',
                    new_column_name='student1_class', existing_type=sa.VARCHAR(100), existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('competition_signup', 'student1_name',
                    new_column_name='student_name', existing_type=sa.VARCHAR(100), existing_nullable=True)
    op.alter_column('competition_signup', 'student1_class',
                    new_column_name='student_class', existing_type=sa.VARCHAR(100), existing_nullable=True)
    # ### end Alembic commands ###
