"""empty message

Revision ID: 7fec12563289
Revises: 
Create Date: 2024-12-02 16:35:59.935688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fec12563289'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=500), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('size',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gear_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('typeID', sa.Integer(), nullable=True),
    sa.Column('sizeID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sizeID'], ['size.id'], ),
    sa.ForeignKeyConstraint(['typeID'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('borrowed_table',
    sa.Column('memberID', sa.Integer(), nullable=False),
    sa.Column('gearID', sa.Integer(), nullable=False),
    sa.Column('qtyBorrowed', sa.Integer(), nullable=True),
    sa.Column('dateBorrowed', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['gearID'], ['gear_table.id'], ),
    sa.ForeignKeyConstraint(['memberID'], ['member_table.id'], ),
    sa.PrimaryKeyConstraint('memberID', 'gearID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrowed_table')
    op.drop_table('gear_table')
    op.drop_table('type')
    op.drop_table('size')
    op.drop_table('member_table')
    # ### end Alembic commands ###
