"""empty message

Revision ID: d6512f3fb0b6
Revises: 1b645529b687
Create Date: 2022-12-29 02:01:26.517158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6512f3fb0b6'
down_revision = '1b645529b687'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookmark',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=240), nullable=True),
    sa.Column('headline', sa.String(length=300), nullable=True),
    sa.Column('read_flag', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_bookmark_headline'), ['headline'], unique=False)
        batch_op.create_index(batch_op.f('ix_bookmark_url'), ['url'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_bookmark_url'))
        batch_op.drop_index(batch_op.f('ix_bookmark_headline'))

    op.drop_table('bookmark')
    # ### end Alembic commands ###