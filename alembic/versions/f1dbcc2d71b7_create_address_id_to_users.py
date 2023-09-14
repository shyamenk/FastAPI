"""create address_id to users

Revision ID: f1dbcc2d71b7
Revises: 3bca8001f97d
Create Date: 2023-09-13 00:15:49.622677

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1dbcc2d71b7"
down_revision: Union[str, None] = "3bca8001f97d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "address_users_fk",
        source_table="users",
        referent_table="address",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint("address_users_fk", table_name="users")
    op.drop_column("users", "address_id")
