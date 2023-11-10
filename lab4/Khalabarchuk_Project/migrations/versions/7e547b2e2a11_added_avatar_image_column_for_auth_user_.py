"""Added avatar_image column for Auth_User table

Revision ID: 7e547b2e2a11
Revises: ff9eba42bdfb
Create Date: 2023-11-05 15:25:22.725199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e547b2e2a11'
down_revision = 'ff9eba42bdfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_image', sa.String(length=30), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.drop_column('avatar_image')

    # ### end Alembic commands ###