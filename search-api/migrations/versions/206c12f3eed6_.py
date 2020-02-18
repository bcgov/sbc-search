"""empty message

Revision ID: 206c12f3eed6
Revises: 69f37ca73364
Create Date: 2020-02-04 08:17:15.801101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '206c12f3eed6'
down_revision = '69f37ca73364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CORP_NAME',
    sa.Column('corp_num', sa.String(length=10), nullable=False),
    sa.Column('CORP_NAME_TYP_CD', sa.String(length=2), nullable=True),
    sa.Column('START_EVENT_ID', sa.Integer(), nullable=True),
    sa.Column('CORP_NAME_SEQ_NUM', sa.Integer(), nullable=True),
    sa.Column('END_EVENT_ID', sa.Integer(), nullable=True),
    sa.Column('CORP_NME', sa.String(length=150), nullable=True),
    sa.Column('DD_CORP_NUM', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('corp_num')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CORP_NAME')
    # ### end Alembic commands ###
