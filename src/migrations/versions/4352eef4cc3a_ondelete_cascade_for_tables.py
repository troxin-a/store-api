"""ondelete_cascade for tables

Revision ID: 4352eef4cc3a
Revises: 9b24f25e85da
Create Date: 2024-10-27 11:40:55.052712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4352eef4cc3a'
down_revision: Union[str, None] = '9b24f25e85da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cart_products_cart_id_fkey', 'cart_products', type_='foreignkey')
    op.drop_constraint('cart_products_product_id_fkey', 'cart_products', type_='foreignkey')
    op.create_foreign_key(None, 'cart_products', 'carts', ['cart_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'cart_products', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('carts_user_id_fkey', 'carts', type_='foreignkey')
    op.create_foreign_key(None, 'carts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.create_foreign_key('carts_user_id_fkey', 'carts', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'cart_products', type_='foreignkey')
    op.drop_constraint(None, 'cart_products', type_='foreignkey')
    op.create_foreign_key('cart_products_product_id_fkey', 'cart_products', 'products', ['product_id'], ['id'])
    op.create_foreign_key('cart_products_cart_id_fkey', 'cart_products', 'carts', ['cart_id'], ['id'])
    # ### end Alembic commands ###
