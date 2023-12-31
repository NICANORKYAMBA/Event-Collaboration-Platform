"""Initial Migration

Revision ID: 1aa9113bc1e6
Revises: 
Create Date: 2023-09-28 12:12:05.977175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aa9113bc1e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=255), server_default='Attendee', nullable=False),
    sa.Column('profile_image', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('role IN ("Organizer", "Attendee")', name='user_role'),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('events',
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('event_name', sa.String(length=255), nullable=False),
    sa.Column('event_date', sa.Date(), nullable=False),
    sa.Column('event_time', sa.Time(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('organizer_id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organizer_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('event_collaborators',
    sa.Column('collaborator_id', sa.String(length=255), nullable=False),
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('collaborator_id')
    )
    op.create_table('event_comments',
    sa.Column('comment_id', sa.String(length=255), nullable=False),
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('comment_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('event_ratings',
    sa.Column('rating_id', sa.String(length=255), nullable=False),
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('rating_id')
    )
    op.create_table('tickets',
    sa.Column('ticket_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('ticket_type', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity_available', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('ticket_id')
    )
    op.create_table('rsvps',
    sa.Column('rsvp_id', sa.String(length=255), nullable=False),
    sa.Column('event_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('ticket_id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.event_id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.ticket_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('rsvp_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rsvps')
    op.drop_table('tickets')
    op.drop_table('event_ratings')
    op.drop_table('event_comments')
    op.drop_table('event_collaborators')
    op.drop_table('events')
    op.drop_table('users')
    # ### end Alembic commands ###
