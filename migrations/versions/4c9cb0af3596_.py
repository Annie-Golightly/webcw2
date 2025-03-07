"""empty message

Revision ID: 4c9cb0af3596
Revises: 7fec12563289
Create Date: 2024-12-02 18:02:40.390786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c9cb0af3596'
down_revision = '7fec12563289'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gear_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qtyTotal', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('qtyAvailable', sa.Integer(), nullable=True))
        batch_op.drop_column('qty')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gear_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qty', sa.INTEGER(), nullable=True))
        batch_op.drop_column('qtyAvailable')
        batch_op.drop_column('qtyTotal')

    # ### end Alembic commands ###
