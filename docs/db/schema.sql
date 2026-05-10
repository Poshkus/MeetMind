-- MeetMind DB schema (MVP)
-- Source of truth: Alembic migrations, this file is a readable snapshot.

CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Note: SQLAlchemy/Alembic may generate slightly different DDL depending on dialect/version.
-- Keep columns aligned with backend/app/models/meeting.py and the migration.
CREATE TABLE IF NOT EXISTS meetings (
    id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,

    owner_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL,

    source_object_key VARCHAR(1024) NOT NULL,

    transcript_text TEXT NULL,
    summary_text TEXT NULL,

    processed_at TIMESTAMPTZ NULL,
    error_message TEXT NULL,

    CONSTRAINT meetings_pkey PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_meetings_owner_id ON meetings (owner_id);
CREATE INDEX IF NOT EXISTS ix_meetings_status ON meetings (status);
CREATE INDEX IF NOT EXISTS ix_meetings_created_at ON meetings (created_at);