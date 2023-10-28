"""Portals

Revision ID: ce5eb75dd667
Revises: 9f3936f7c89e
Create Date: 2023-10-28 19:19:49.198729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ce5eb75dd667"
down_revision: Union[str, None] = "9f3936f7c89e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users_user", sa.Column("department_id", sa.UUID(), nullable=True))
    op.add_column("users_user", sa.Column("portal_id", sa.UUID(), nullable=True))
    op.create_foreign_key(None, "users_user", "portals_department", ["department_id"], ["id"])
    op.create_foreign_key(None, "users_user", "portals_portal", ["portal_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users_user", type_="foreignkey")
    op.drop_constraint(None, "users_user", type_="foreignkey")
    op.drop_column("users_user", "portal_id")
    op.drop_column("users_user", "department_id")
    # ### end Alembic commands ###
