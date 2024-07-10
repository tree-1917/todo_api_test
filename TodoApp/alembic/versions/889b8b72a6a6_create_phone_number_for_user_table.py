"""Create phone number for user table

Revision ID: 889b8b72a6a6
Revises: 
Create Date: 2024-07-04 11:31:26.302694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '889b8b72a6a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users","phone_number")
    