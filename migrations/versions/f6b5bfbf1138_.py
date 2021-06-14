"""empty message

Revision ID: f6b5bfbf1138
Revises: 3431c65d6947
Create Date: 2021-06-09 18:10:36.748537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6b5bfbf1138'
down_revision = '3431c65d6947'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('layouts',
    sa.Column('l_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('l_id')
    )
    op.create_table('pictures',
    sa.Column('pic_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('pic_id')
    )
    op.create_table('templates',
    sa.Column('t_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('path', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('t_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('templates')
    op.drop_table('pictures')
    op.drop_table('layouts')
    # ### end Alembic commands ###
