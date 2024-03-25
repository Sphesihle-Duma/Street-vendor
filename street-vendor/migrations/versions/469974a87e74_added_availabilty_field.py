"""added availabilty field

Revision ID: 469974a87e74
Revises: 1996328f3ae1
Create Date: 2024-03-25 00:23:00.103389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '469974a87e74'
down_revision = '1996328f3ae1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('space', schema=None) as batch_op:
        batch_op.add_column(sa.Column('availability', sa.String(length=64), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('space', schema=None) as batch_op:
        batch_op.drop_column('availability')

    # ### end Alembic commands ###
