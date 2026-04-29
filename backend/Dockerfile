# =========================
# Builder Stage
# =========================
FROM python:3.6.15-slim-buster AS builder

WORKDIR /app

RUN echo "deb http://archive.debian.org/debian/ buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip==21.3.1 \
 && pip install --no-cache-dir -r requirements.txt


# =========================
# Runtime Stage
# =========================
FROM python:3.6.15-slim-buster

WORKDIR /app

RUN echo "deb http://archive.debian.org/debian/ buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

RUN apt-get update && apt-get install -y \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

COPY . .
RUN chmod +x entrypoint.sh

RUN useradd --no-create-home appuser \
 && chown -R appuser /app
USER appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "conduit.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]