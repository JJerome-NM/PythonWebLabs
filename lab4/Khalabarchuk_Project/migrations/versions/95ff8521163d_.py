"""empty message

Revision ID: 95ff8521163d
Revises: b6c502e7906d
Create Date: 2023-12-31 18:14:32.707878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95ff8521163d'
down_revision = 'b6c502e7906d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=35),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=200),
               existing_nullable=False)
        batch_op.alter_column('avatar_image',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=60),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.alter_column('avatar_image',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=35),
               existing_nullable=False)

    # ### end Alembic commands ###
