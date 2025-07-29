from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'employee',  # <-- numele tabelului tău
        'additional_bonuses',
        existing_type=sa.Integer(),
        server_default="0"
    )


def downgrade():
    op.alter_column(
        'employee',
        'additional_bonuses',
        existing_type=sa.Integer(),
        server_default=None
    )
