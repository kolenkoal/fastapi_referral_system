"""Changed user_id to referrer_id in users_referral_codes

Revision ID: 1a9c8ec1d5c2
Revises: 78e41b108d29
Create Date: 2024-02-06 17:12:55.729008

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1a9c8ec1d5c2"
down_revision: Union[str, None] = "78e41b108d29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_referral_codes",
        sa.Column(
            "referrer_id",
            fastapi_users_db_sqlalchemy.generics.GUID(),
            nullable=False,
        ),
    )
    op.drop_constraint(
        "user_referral_codes_user_id_fkey",
        "user_referral_codes",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "user_referral_codes",
        "users",
        ["referrer_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("user_referral_codes", "user_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_referral_codes",
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "user_referral_codes", type_="foreignkey")
    op.create_foreign_key(
        "user_referral_codes_user_id_fkey",
        "user_referral_codes",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("user_referral_codes", "referrer_id")
    # ### end Alembic commands ###