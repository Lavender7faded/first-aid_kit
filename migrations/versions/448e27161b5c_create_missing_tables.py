"""Create missing tables

Revision ID: 448e27161b5c
Revises: 71c50a84f4d5
Create Date: 2025-04-11 20:04:02.936748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '448e27161b5c'
down_revision = '71c50a84f4d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medicine')
    op.drop_table('alert')
    # ### end Alembic commands ###
