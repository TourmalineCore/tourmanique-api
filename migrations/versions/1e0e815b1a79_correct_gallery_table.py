"""correct_gallery_table

Revision ID: 1e0e815b1a79
Revises: 27eed96405ee
Create Date: 2023-03-17 06:13:45.926307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e0e815b1a79'
down_revision = '27eed96405ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('galleries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at_utc', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('galleries', schema=None) as batch_op:
        batch_op.drop_column('deleted_at_utc')

    # ### end Alembic commands ###
