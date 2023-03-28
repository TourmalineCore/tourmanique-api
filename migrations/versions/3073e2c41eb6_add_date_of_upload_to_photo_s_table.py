"""add_date_of_upload_to_photo's_table

Revision ID: 3073e2c41eb6
Revises: 1e0e815b1a79
Create Date: 2023-03-21 11:12:15.876430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3073e2c41eb6'
down_revision = '1e0e815b1a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_of_upload', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('photos', schema=None) as batch_op:
        batch_op.drop_column('date_of_upload')

    # ### end Alembic commands ###