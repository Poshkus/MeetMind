# ADR-003: Upload limits and validation

## Status
Accepted

## Context
MeetMind принимает загрузки аудио/видео для последующей обработки (ffmpeg → wav → STT).
Риск: загрузка произвольных файлов, попытки залить очень большой файл и забить диск (DoS).

## Decision
В API `/upload` добавлено:
- allowlist по `content_type` (минимальная фильтрация на входе)
- серверная генерация имени файла (UUID), игнорируем `filename` пользователя
- ограничение размера загрузки: `MAX_UPLOAD_BYTES = 1GB`
  - лимит считается по фактически прочитанным байтам
  - при превышении возвращаем `413 Payload Too Large`
  - временный файл удаляется

## Consequences
- Клиент может получить 415, если `content_type` не в allowlist — нужно учитывать на фронте.
- Для более строгой защиты позже можно добавить:
  - проверку “магических байт” (file signature)
  - лимиты на уровне reverse proxy (nginx `client_max_body_size`)
  - лимиты на уровне S3/MinIO presigned upload (если перейдём на прямую загрузку)