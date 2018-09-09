"""change column name _password to password

Revision ID: be011eb18c7d
Revises: c3aa13fb1cf7
Create Date: 2018-09-09 15:14:45.259468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be011eb18c7d'
down_revision = 'c3aa13fb1cf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('managers', sa.Column('password', sa.String(length=125), nullable=False))
    op.drop_column('managers', '_password')
    op.add_column('schools', sa.Column('password', sa.String(length=125), nullable=False))
    op.drop_column('schools', '_password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schools', sa.Column('_password', mysql.VARCHAR(length=125), nullable=False))
    op.drop_column('schools', 'password')
    op.add_column('managers', sa.Column('_password', mysql.VARCHAR(length=125), nullable=False))
    op.drop_column('managers', 'password')
    # ### end Alembic commands ###
