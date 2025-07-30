"""add_role

Revision ID: 33a3b478d30d
Revises: 08fe6db773be
Create Date: 2025-07-30 16:32:21.535509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33a3b478d30d'
down_revision = '08fe6db773be'
branch_labels = None
depends_on = None


def upgrade():

    role_enum = sa.Enum('EMPLOYEE', 'MANAGER', name='roleenum')
    role_enum.create(op.get_bind())


    with op.batch_alter_table('employee_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', role_enum, nullable=True))

def downgrade():
        with op.batch_alter_table('employee_data', schema=None) as batch_op:
            batch_op.drop_column('role')


        sa.Enum(name='roleenum').drop(op.get_bind())

    # ### end Alembic commands ###
