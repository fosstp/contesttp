"""fix foreign key mapping column name

Revision ID: 57e0d34f355f
Revises: b2713869b3a2
Create Date: 2018-09-09 14:17:19.225353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '57e0d34f355f'
down_revision = 'b2713869b3a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition_news', sa.Column('manager_id', sa.Integer(), nullable=True))
    op.drop_constraint('competition_news_ibfk_2', 'competition_news', type_='foreignkey')
    op.create_foreign_key(None, 'competition_news', 'managers', ['manager_id'], ['id'])
    op.drop_column('competition_news', 'manager')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition_news', sa.Column('manager', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'competition_news', type_='foreignkey')
    op.create_foreign_key('competition_news_ibfk_2', 'competition_news', 'managers', ['manager'], ['id'])
    op.drop_column('competition_news', 'manager_id')
    # ### end Alembic commands ###