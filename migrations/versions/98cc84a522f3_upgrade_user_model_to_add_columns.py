"""upgrade user model to add columns

Revision ID: 98cc84a522f3
Revises: 5a1d7ba89720
Create Date: 2024-07-01 11:02:50.647291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '98cc84a522f3'
down_revision: Union[str, None] = '5a1d7ba89720'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###