"""Without number.

Revision ID: 12f6a829eb8c
Revises: 
Create Date: 2023-07-13 03:39:40.396311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12f6a829eb8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priceTOTAL', sa.Float(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('orderstatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orderID', sa.Integer(), nullable=False),
    sa.Column('statusID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['orderID'], ['orders.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['statusID'], ['status.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productID', sa.Integer(), nullable=False),
    sa.Column('categoryID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categoryID'], ['categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['productID'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productorder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orderID', sa.Integer(), nullable=False),
    sa.Column('productID', sa.Integer(), nullable=False),
    sa.Column('priceATM', sa.Float(), nullable=False),
    sa.Column('received', sa.Integer(), nullable=False),
    sa.Column('requested', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['orderID'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['productID'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productorder')
    op.drop_table('productcategory')
    op.drop_table('orderstatus')
    op.drop_table('status')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('categories')
    # ### end Alembic commands ###