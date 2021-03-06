"""new user model

Revision ID: 8dac8fe3e9b2
Revises: 
Create Date: 2018-04-11 22:26:58.088861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8dac8fe3e9b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('title.akas')
    op.drop_column('title.basics', 'runtimeMinutes')
    op.drop_column('title.basics', 'endYear')
    op.drop_column('title.basics', 'isAdult')
    op.drop_column('title.basics', 'originalTitle')
    op.alter_column('title.crew', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.drop_constraint('title.crew_ibfk_1', 'title.crew', type_='foreignkey')
    op.add_column('title.principals', sa.Column('ID', sa.Integer(), nullable=False))
    op.alter_column('title.principals', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.drop_constraint('title.principals_ibfk_1', 'title.principals', type_='foreignkey')
    op.drop_constraint('nconst_key', 'title.principals', type_='foreignkey')
    op.drop_column('title.principals', 'id')
    op.drop_constraint('tconst_key', 'title.ratings', type_='foreignkey')
    op.alter_column('user.favorites', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.alter_column('user.favorites', 'user_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('user.friends', 'friend1_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('user.friends', 'friend2_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('user.ratings', 'ratings',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.alter_column('user.ratings', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    op.alter_column('user.ratings', 'user_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.add_column('user_info', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user_info', sa.Column('favorite_movies', sa.String(length=140), nullable=True))
    op.add_column('user_info', sa.Column('groups', sa.String(length=140), nullable=True))
    op.add_column('user_info', sa.Column('reviews', sa.String(length=140), nullable=True))
    op.alter_column('user_info', 'email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('user_info', 'password',
               existing_type=mysql.VARCHAR(length=128),
               nullable=True)
    op.alter_column('user_info', 'username',
               existing_type=mysql.VARCHAR(length=16),
               nullable=True)
    op.drop_column('user_info', 'Admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('Admin', mysql.TINYINT(display_width=4), server_default=sa.text("'0'"), autoincrement=False, nullable=True))
    op.alter_column('user_info', 'username',
               existing_type=mysql.VARCHAR(length=16),
               nullable=False)
    op.alter_column('user_info', 'password',
               existing_type=mysql.VARCHAR(length=128),
               nullable=False)
    op.alter_column('user_info', 'email',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.drop_column('user_info', 'reviews')
    op.drop_column('user_info', 'groups')
    op.drop_column('user_info', 'favorite_movies')
    op.drop_column('user_info', 'about_me')
    op.alter_column('user.ratings', 'user_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user.ratings', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.alter_column('user.ratings', 'ratings',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('user.friends', 'friend2_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user.friends', 'friend1_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user.favorites', 'user_ID',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('user.favorites', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.create_foreign_key('tconst_key', 'title.ratings', 'title.basics', ['tconst'], ['tconst'])
    op.add_column('title.principals', sa.Column('id', mysql.INTEGER(display_width=10, unsigned=True), nullable=False))
    op.create_foreign_key('nconst_key', 'title.principals', 'name', ['nconst'], ['nconst'])
    op.create_foreign_key('title.principals_ibfk_1', 'title.principals', 'title.basics', ['tconst'], ['tconst'])
    op.alter_column('title.principals', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.drop_column('title.principals', 'ID')
    op.create_foreign_key('title.crew_ibfk_1', 'title.crew', 'title.basics', ['tconst'], ['tconst'])
    op.alter_column('title.crew', 'tconst',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.add_column('title.basics', sa.Column('originalTitle', mysql.TEXT(), nullable=True))
    op.add_column('title.basics', sa.Column('isAdult', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('title.basics', sa.Column('endYear', mysql.TEXT(), nullable=True))
    op.add_column('title.basics', sa.Column('runtimeMinutes', mysql.TEXT(), nullable=True))
    op.create_table('title.akas',
    sa.Column('titleId', mysql.TEXT(), nullable=True),
    sa.Column('ordering', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('title', mysql.TEXT(), nullable=True),
    sa.Column('region', mysql.TEXT(), nullable=True),
    sa.Column('language', mysql.TEXT(), nullable=True),
    sa.Column('types', mysql.TEXT(), nullable=True),
    sa.Column('attributes', mysql.TEXT(), nullable=True),
    sa.Column('isOriginalTitle', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
