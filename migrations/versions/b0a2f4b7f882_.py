"""empty message

Revision ID: b0a2f4b7f882
Revises: d08150b1d778
Create Date: 2023-08-26 15:08:00.980398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0a2f4b7f882'
down_revision: Union[str, None] = 'd08150b1d778'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'is_superuser',server_default=None)

def downgrade() -> None:
    op.alter_column('user', 'is_superuser',server_default='false')