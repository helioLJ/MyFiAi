"""Insight month Integer

Revision ID: e0b643f2d5fa
Revises: 44af9d2b1504
Create Date: 2024-02-16 19:23:51.292262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0b643f2d5fa'
down_revision = '44af9d2b1504'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE insight ALTER COLUMN month TYPE INTEGER USING month::integer')

def downgrade():
    op.execute('ALTER TABLE insight ALTER COLUMN month TYPE VARCHAR(120) USING month::text')
