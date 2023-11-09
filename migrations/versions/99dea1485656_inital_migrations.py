"""inital migrations

Revision ID: 99dea1485656
Revises: 
Create Date: 2022-03-02 19:11:26.563133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99dea1485656'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addproduct')
    op.add_column('register_customer', sa.Column('f_name', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('register_customer', 'f_name')
    op.create_table('addproduct',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), nullable=False),
    sa.Column('price', sa.NUMERIC(precision=10, scale=2), nullable=False),
    sa.Column('discount', sa.INTEGER(), nullable=True),
    sa.Column('stock', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=False),
    sa.Column('pub_date', sa.DATETIME(), nullable=False),
    sa.Column('brand_id', sa.INTEGER(), nullable=False),
    sa.Column('category_id', sa.INTEGER(), nullable=False),
    sa.Column('image_1', sa.VARCHAR(length=150), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
