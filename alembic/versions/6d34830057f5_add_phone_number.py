"""add phone number

Revision ID: 6d34830057f5
Revises: 
Create Date: 2023-09-13 00:09:18.355467

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6d34830057f5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade():
    op.drop_column("users", "phone_number")
