"""adding a field to the permit table

Revision ID: 970a1ad0094a
Revises: 077bb3b164e4
Create Date: 2024-03-21 14:36:42.031223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '970a1ad0094a'
down_revision = '077bb3b164e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=64), nullable=False))
        batch_op.create_index(batch_op.f('ix_permit_status'), ['status'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permit_status'))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
