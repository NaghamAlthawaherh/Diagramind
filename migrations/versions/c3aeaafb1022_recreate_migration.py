"""Recreate migration

Revision ID: c3aeaafb1022
Revises: 
Create Date: 2025-05-14 15:10:51.902954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3aeaafb1022'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('use_case_diagrams')
    op.drop_table('use_cases')
    op.drop_table('functional_requirements')
    op.drop_table('actors')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('company', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('user_type', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('terms_accepted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('terms_accepted')
        batch_op.drop_column('user_type')
        batch_op.drop_column('company')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    op.create_table('actors',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('diagram_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['diagram_id'], ['use_case_diagrams.id'], name='FK__actors__diagram___45F365D3'),
    sa.PrimaryKeyConstraint('id', name='PK__actors__3213E83F36332812')
    )
    op.create_table('functional_requirements',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=200, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('complexity', sa.VARCHAR(length=6, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('estimated_hours', sa.FLOAT(precision=53), autoincrement=False, nullable=True),
    sa.Column('diagram_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('actor_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('use_case_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], name='FK__functiona__actor__03F0984C'),
    sa.ForeignKeyConstraint(['diagram_id'], ['use_case_diagrams.id'], name='FK__functiona__diagr__02FC7413'),
    sa.ForeignKeyConstraint(['use_case_id'], ['use_cases.id'], name='FK__functiona__use_c__04E4BC85'),
    sa.PrimaryKeyConstraint('id', name='PK__function__3213E83FCFC4446E')
    )
    op.create_table('use_cases',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('diagram_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['diagram_id'], ['use_case_diagrams.id'], name='FK__use_cases__diagr__48CFD27E'),
    sa.PrimaryKeyConstraint('id', name='PK__use_case__3213E83F53254AC7')
    )
    op.create_table('use_case_diagrams',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('extracted_text', sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='PK__use_case__3213E83FD8B8D45B')
    )
    # ### end Alembic commands ###
