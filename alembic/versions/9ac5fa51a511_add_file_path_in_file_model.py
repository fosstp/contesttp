"""add file path in File model

Revision ID: 9ac5fa51a511
Revises: 57f7b1253bc7
Create Date: 2018-09-13 16:48:39.427782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ac5fa51a511'
down_revision = '57f7b1253bc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('path', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'path')
    # ### end Alembic commands ###
