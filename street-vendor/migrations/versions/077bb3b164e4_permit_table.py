"""permit table

Revision ID: 077bb3b164e4
Revises: 0b3a9f0cb1e0
Create Date: 2024-03-21 14:30:14.209195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '077bb3b164e4'
down_revision = '0b3a9f0cb1e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendor_name', sa.String(length=64), nullable=False),
    sa.Column('street_name', sa.String(length=64), nullable=False),
    sa.Column('space_number', sa.Integer(), nullable=False),
    sa.Column('about_business', sa.String(length=140), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['space_number'], ['space.space_number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_permit_space_number'), ['space_number'], unique=False)
        batch_op.create_index(batch_op.f('ix_permit_street_name'), ['street_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_permit_vendor_name'), ['vendor_name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permit', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permit_vendor_name'))
        batch_op.drop_index(batch_op.f('ix_permit_street_name'))
        batch_op.drop_index(batch_op.f('ix_permit_space_number'))

    op.drop_table('permit')
    # ### end Alembic commands ###
