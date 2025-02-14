"""Portfolio add: Scheme Code

Revision ID: 4a338fa17f30
Revises: 9b4d7bb2ab35
Create Date: 2025-01-08 12:23:45.488874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a338fa17f30'
down_revision = '9b4d7bb2ab35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.add_column(sa.Column('scheme_code', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolio', schema=None) as batch_op:
        batch_op.drop_column('scheme_code')

    # ### end Alembic commands ###
