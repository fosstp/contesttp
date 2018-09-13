"""change column name

Revision ID: 0d5fa0176de6
Revises: 9ac5fa51a511
Create Date: 2018-09-13 16:50:22.628023

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0d5fa0176de6'
down_revision = '9ac5fa51a511'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('name', sa.String(length=100), nullable=False))
    op.drop_column('files', 'path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('path', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('files', 'name')
    # ### end Alembic commands ###
