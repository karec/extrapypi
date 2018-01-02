"""remove digest from release model

Revision ID: 21a32f52b0c3
Revises: e9ba59cdb7b9
Create Date: 2018-01-02 18:30:24.105748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21a32f52b0c3'
down_revision = 'e9ba59cdb7b9'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('release', 'md5_digest')


def downgrade():
    op.add_column('release', sa.Column('md5_digest', sa.VARCHAR(length=32), nullable=False))
