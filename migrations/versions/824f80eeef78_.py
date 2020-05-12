"""empty message

Revision ID: 824f80eeef78
Revises: 8a0cfc0cb4d4
Create Date: 2020-05-12 15:27:31.336430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '824f80eeef78'
down_revision = '8a0cfc0cb4d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_rating_date_posted', table_name='rating')
    op.drop_table('rating')
    op.drop_index('ix_restaurant_name', table_name='restaurant')
    op.drop_table('restaurant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('zomato_url', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('area', sa.VARCHAR(), nullable=True),
    sa.Column('rating', sa.FLOAT(), nullable=True),
    sa.Column('rating_count', sa.FLOAT(), nullable=True),
    sa.Column('telephone', sa.VARCHAR(), nullable=True),
    sa.Column('cusine', sa.VARCHAR(), nullable=True),
    sa.Column('cost_for_two', sa.FLOAT(), nullable=True),
    sa.Column('address', sa.VARCHAR(), nullable=True),
    sa.Column('online_order', sa.BOOLEAN(), nullable=True),
    sa.Column('table_reservation', sa.BOOLEAN(), nullable=True),
    sa.Column('delivery_only', sa.BOOLEAN(), nullable=True),
    sa.Column('famous_food', sa.VARCHAR(), nullable=True),
    sa.Column('longitude', sa.FLOAT(), nullable=True),
    sa.Column('latitude', sa.FLOAT(), nullable=True),
    sa.CheckConstraint('delivery_only IN (0, 1)'),
    sa.CheckConstraint('online_order IN (0, 1)'),
    sa.CheckConstraint('table_reservation IN (0, 1)'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_restaurant_name', 'restaurant', ['name'], unique=1)
    op.create_table('rating',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('rest_id', sa.INTEGER(), nullable=True),
    sa.Column('rating', sa.INTEGER(), nullable=True),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('date_posted', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['rest_id'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rating_date_posted', 'rating', ['date_posted'], unique=False)
    # ### end Alembic commands ###
