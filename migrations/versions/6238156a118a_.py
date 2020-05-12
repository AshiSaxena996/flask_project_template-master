"""empty message

Revision ID: 6238156a118a
Revises: 21ab2136a378
Create Date: 2020-05-12 15:29:13.935406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6238156a118a'
down_revision = '21ab2136a378'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zomato_url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Float(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('cuisine', sa.String(), nullable=True),
    sa.Column('cost_for_two', sa.Float(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('online_order', sa.Boolean(), nullable=True),
    sa.Column('table_reservation', sa.Boolean(), nullable=True),
    sa.Column('delivery_only', sa.Boolean(), nullable=True),
    sa.Column('famous_food', sa.String(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restaurant_name'), 'restaurant', ['name'], unique=True)
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rest_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['rest_id'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rating_date_posted'), 'rating', ['date_posted'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rating_date_posted'), table_name='rating')
    op.drop_table('rating')
    op.drop_index(op.f('ix_restaurant_name'), table_name='restaurant')
    op.drop_table('restaurant')
    # ### end Alembic commands ###
