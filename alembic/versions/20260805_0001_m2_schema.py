"""create M2 tables"""

import sqlalchemy as sa

from alembic import op

revision = "20260805_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("email", sa.String(320), nullable=False), sa.Column("password_hash", sa.String(512), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("email"))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("jobs", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("company", sa.String(200), nullable=False), sa.Column("position", sa.String(200), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("url", sa.String(2048), nullable=False), sa.Column("note", sa.Text(), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("priority", sa.Integer(), nullable=False), sa.Column("deadline", sa.Date(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    for name in ("user_id", "company", "position", "status"):
        op.create_index(f"ix_jobs_{name}", "jobs", [name])
    op.create_table("application_events", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("job_id", sa.Uuid(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False), sa.Column("event_type", sa.String(100), nullable=False), sa.Column("note", sa.Text(), nullable=False), sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("tasks", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("job_id", sa.Uuid(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True), sa.Column("title", sa.String(300), nullable=False), sa.Column("due_date", sa.Date(), nullable=True), sa.Column("completed", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("documents", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("job_id", sa.Uuid(), sa.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=True), sa.Column("document_type", sa.String(50), nullable=False), sa.Column("filename", sa.String(255), nullable=False), sa.Column("stored_path", sa.String(1000), nullable=False, unique=True), sa.Column("content_type", sa.String(100), nullable=False), sa.Column("size_bytes", sa.Integer(), nullable=False), sa.Column("parse_status", sa.String(30), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for table in ("application_events", "tasks", "documents"):
        op.create_index(f"ix_{table}_user_id", table, ["user_id"])
        if table == "application_events":
            op.create_index("ix_application_events_job_id", table, ["job_id"])


def downgrade() -> None:
    for table in ("documents", "tasks", "application_events", "jobs", "users"):
        op.drop_table(table)
