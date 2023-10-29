"""Avatar

Revision ID: b3335b72303a
Revises: 005c0e95d23f
Create Date: 2023-10-29 17:06:38.301434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3335b72303a"
down_revision: Union[str, None] = "005c0e95d23f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users_user", sa.Column("avatar", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users_user", "avatar")
    # ### end Alembic commands ###