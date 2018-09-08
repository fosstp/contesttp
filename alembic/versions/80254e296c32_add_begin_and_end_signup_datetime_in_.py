"""add begin and end signup datetime in Competition model

Revision ID: 80254e296c32
Revises: 79b82f50bcd4
Create Date: 2018-09-08 14:55:03.753786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80254e296c32'
down_revision = '79b82f50bcd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition', sa.Column('begin_signup_datetime', sa.DateTime(), nullable=False))
    op.add_column('competition', sa.Column('end_signup_datetime', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('competition', 'end_signup_datetime')
    op.drop_column('competition', 'begin_signup_datetime')
    # ### end Alembic commands ###
