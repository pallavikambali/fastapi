"""create missing tables

Revision ID: e9356b008a91
Revises: bd793e4e9712
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e9356b008a91'
down_revision: Union[str, Sequence[str], None] = 'bd793e4e9712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_users_email'),
        'users',
        ['email'],
        unique=True
    )

    # Add missing columns to the existing posts table
    op.add_column('posts', sa.Column('content', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=True))
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'posts_owner_id_fkey',
        'posts',
        'users',
        ['owner_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # Create votes table
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )


def downgrade() -> None:
    op.drop_table('votes')
    op.drop_constraint('posts_owner_id_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'content')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')