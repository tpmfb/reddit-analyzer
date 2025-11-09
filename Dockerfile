# ----- Stage 1: dependency layer -----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----- Stage 2: runtime -----
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY reddit_r00m.py .

# .env will be mounted or loaded via env_file; never copied in
CMD ["python", "reddit_r00m.py"]