"""Initial migration.

Revision ID: 3ceabb1ac2ac
Revises: 
Create Date: 2021-11-01 19:13:07.863808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ceabb1ac2ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Fv',
    sa.Column('FvId', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=45), nullable=False),
    sa.Column('Volume', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('FvId'),
    sa.UniqueConstraint('Name', name='AK__Name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Fv')
    # ### end Alembic commands ###
