"""added profile picture

Revision ID: 2bb813fc525f
Revises: c257ff17b557
Create Date: 2022-01-26 17:50:26.132900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb813fc525f'
down_revision = 'c257ff17b557'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture', sa.String(length=72), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_picture')
    # ### end Alembic commands ###
