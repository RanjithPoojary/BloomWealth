"""Portfolio update

Revision ID: 9b4d7bb2ab35
Revises: 5cc7213645a8
Create Date: 2025-01-08 12:04:19.396278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4d7bb2ab35'
down_revision = '5cc7213645a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fund_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('units_owned', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('purchase_price', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('investment_amount', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('purchase_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('scheme_code')
        batch_op.drop_column('units')
        batch_op.drop_column('fund_house')
        batch_op.drop_column('current_value')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_value', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('fund_house', sa.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('units', sa.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('scheme_code', sa.VARCHAR(length=20), nullable=False))
        batch_op.drop_column('purchase_date')
        batch_op.drop_column('investment_amount')
        batch_op.drop_column('purchase_price')
        batch_op.drop_column('units_owned')
        batch_op.drop_column('fund_name')

    # ### end Alembic commands ###
