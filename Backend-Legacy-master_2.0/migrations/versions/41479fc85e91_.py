"""empty message

Revision ID: 41479fc85e91
Revises: 6946d61a71cc
Create Date: 2022-09-22 17:35:58.383035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41479fc85e91'
down_revision = '6946d61a71cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('PATIENT', sa.Column('cardNum', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('PATIENT', 'cardNum')
    # ### end Alembic commands ###
