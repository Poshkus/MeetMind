# backend/app/models/meeting.py
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, IdMixin, TimestampMixin

class MeetingStatus(str, enum.Enum):
    uploaded = "uploaded"
    queued = "queued"
    processing = "processing"
    done = "done"
    failed = "failed"

class Meeting(Base, IdMixin, TimestampMixin):
    __tablename__ = "meetings"

    # owner_id позже привяжем к users (когда добавим auth и таблицу users)
    owner_id: Mapped[int] = mapped_column(nullable=False, index=True)

    title: Mapped[str | None] = mapped_column(String(200), nullable=True)

    status: Mapped[MeetingStatus] = mapped_column(
        Enum(MeetingStatus, name="meeting_status"),
        nullable=False,
        default=MeetingStatus.uploaded,
        index=True,
    )

    # Ссылки на файлы/объекты в S3/MinIO заведём позже, пока поле под ключ объекта.
    source_object_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)

    # Результаты обработки (потом можно вынести в отдельные таблицы)
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)