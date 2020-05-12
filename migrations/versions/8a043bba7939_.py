"""empty message

Revision ID: 8a043bba7939
Revises: c4e9b1c921e6
Create Date: 2020-05-12 15:24:45.559887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a043bba7939'
down_revision = 'c4e9b1c921e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('restaurant')
    op.drop_index('ix_rating_date_posted', table_name='rating')
    op.drop_table('rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_table('restaurant',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('address', sa.VARCHAR(), nullable=False),
    sa.Column('locality_id', sa.INTEGER(), nullable=True),
    sa.Column('phone', sa.VARCHAR(), nullable=True),
    sa.Column('delivery', sa.BOOLEAN(), nullable=True),
    sa.Column('booking', sa.BOOLEAN(), nullable=True),
    sa.Column('url', sa.VARCHAR(), nullable=False),
    sa.Column('area', sa.VARCHAR(), nullable=True),
    sa.Column('cost_for_two', sa.FLOAT(), nullable=True),
    sa.Column('cusine', sa.VARCHAR(), nullable=True),
    sa.Column('delivery_only', sa.BOOLEAN(), nullable=True),
    sa.Column('famous_food', sa.VARCHAR(), nullable=True),
    sa.Column('latitude', sa.FLOAT(), nullable=True),
    sa.Column('longitude', sa.FLOAT(), nullable=True),
    sa.Column('online_order', sa.BOOLEAN(), nullable=True),
    sa.Column('rating', sa.FLOAT(), nullable=True),
    sa.Column('rating_count', sa.FLOAT(), nullable=True),
    sa.Column('table_reservation', sa.BOOLEAN(), nullable=True),
    sa.Column('telephone', sa.VARCHAR(), nullable=True),
    sa.CheckConstraint('booking IN (0, 1)'),
    sa.CheckConstraint('delivery IN (0, 1)'),
    sa.ForeignKeyConstraint(['locality_id'], ['locality.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
