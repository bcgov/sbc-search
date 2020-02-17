"""empty message

Revision ID: 10ec817e65d0
Revises: e4d106926f51
Create Date: 2020-02-17 07:52:47.686042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10ec817e65d0'
down_revision = 'e4d106926f51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CORP_OP_STATE',
    sa.Column('STATE_TYP_CD', sa.String(length=3), nullable=False),
    sa.Column('OP_STATE_TYP_CD', sa.String(length=3), nullable=True),
    sa.Column('SHORT_DESC', sa.String(length=15), nullable=True),
    sa.Column('FULL_DESC', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('STATE_TYP_CD')
    )
    op.create_table('CORP_STATE',
    sa.Column('CORP_NUM', sa.String(length=10), nullable=False),
    sa.Column('START_EVENT_ID', sa.Integer(), nullable=False),
    sa.Column('END_EVENT_ID', sa.Integer(), nullable=True),
    sa.Column('STATE_TYP_CD', sa.String(length=3), nullable=True),
    sa.Column('DD_CORP_NUM', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('CORP_NUM', 'START_EVENT_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CORP_STATE')
    op.drop_table('CORP_OP_STATE')
    # ### end Alembic commands ###
