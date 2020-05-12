"""empty message

Revision ID: c4e9b1c921e6
Revises: 68c912898f45
Create Date: 2020-05-12 15:22:18.728257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e9b1c921e6'
down_revision = '68c912898f45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('area', sa.String(), nullable=True))
    op.add_column('restaurant', sa.Column('cost_for_two', sa.Float(), nullable=True))
    op.add_column('restaurant', sa.Column('cusine', sa.String(), nullable=True))
    op.add_column('restaurant', sa.Column('delivery_only', sa.Boolean(), nullable=True))
    op.add_column('restaurant', sa.Column('famous_food', sa.String(), nullable=True))
    op.add_column('restaurant', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('restaurant', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('restaurant', sa.Column('online_order', sa.Boolean(), nullable=True))
    op.add_column('restaurant', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('restaurant', sa.Column('rating_count', sa.Float(), nullable=True))
    op.add_column('restaurant', sa.Column('table_reservation', sa.Boolean(), nullable=True))
    op.add_column('restaurant', sa.Column('telephone', sa.String(), nullable=True))
    op.add_column('restaurant', sa.Column('zomato_url', sa.String(), nullable=False))
    op.alter_column('restaurant', 'address',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_index(op.f('ix_restaurant_name'), 'restaurant', ['name'], unique=True)
    op.drop_constraint(None, 'restaurant', type_='foreignkey')
    op.drop_column('restaurant', 'locality_id')
    op.drop_column('restaurant', 'booking')
    op.drop_column('restaurant', 'url')
    op.drop_column('restaurant', 'delivery')
    op.drop_column('restaurant', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurant', sa.Column('phone', sa.VARCHAR(), nullable=True))
    op.add_column('restaurant', sa.Column('delivery', sa.BOOLEAN(), nullable=True))
    op.add_column('restaurant', sa.Column('url', sa.VARCHAR(), nullable=False))
    op.add_column('restaurant', sa.Column('booking', sa.BOOLEAN(), nullable=True))
    op.add_column('restaurant', sa.Column('locality_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'restaurant', 'locality', ['locality_id'], ['id'])
    op.drop_index(op.f('ix_restaurant_name'), table_name='restaurant')
    op.alter_column('restaurant', 'address',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('restaurant', 'zomato_url')
    op.drop_column('restaurant', 'telephone')
    op.drop_column('restaurant', 'table_reservation')
    op.drop_column('restaurant', 'rating_count')
    op.drop_column('restaurant', 'rating')
    op.drop_column('restaurant', 'online_order')
    op.drop_column('restaurant', 'longitude')
    op.drop_column('restaurant', 'latitude')
    op.drop_column('restaurant', 'famous_food')
    op.drop_column('restaurant', 'delivery_only')
    op.drop_column('restaurant', 'cusine')
    op.drop_column('restaurant', 'cost_for_two')
    op.drop_column('restaurant', 'area')
    # ### end Alembic commands ###
