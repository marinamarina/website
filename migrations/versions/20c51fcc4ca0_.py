"""empty message

Revision ID: 20c51fcc4ca0
Revises: 3f62635bf146
Create Date: 2014-10-07 19:27:09.524373

"""

# revision identifiers, used by Alembic.
revision = '20c51fcc4ca0'
down_revision = '3f62635bf146'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_roles_default', 'roles')
    op.drop_column('roles', 'default')
    ### end Alembic commands ###
