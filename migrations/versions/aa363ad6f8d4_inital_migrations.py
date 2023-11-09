"""inital migrations

Revision ID: aa363ad6f8d4
Revises: 99dea1485656
Create Date: 2022-03-02 19:34:13.113854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa363ad6f8d4'
down_revision = '99dea1485656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('register_customer', 'f_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('register_customer', sa.Column('f_name', sa.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###
