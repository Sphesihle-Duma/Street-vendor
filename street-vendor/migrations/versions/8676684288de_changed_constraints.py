"""changed constraints

Revision ID: 8676684288de
Revises: 970a1ad0094a
Create Date: 2024-03-21 23:40:21.818328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8676684288de'
down_revision = '970a1ad0094a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
        batch_op.drop_index('ix_permit_street_name')
        batch_op.create_index(batch_op.f('ix_permit_street_name'), ['street_name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permit_street_name'))
        batch_op.create_index('ix_permit_street_name', ['street_name'], unique=True)
        batch_op.alter_column('created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###
