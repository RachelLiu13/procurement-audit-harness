# The whole app on Fly.io: FastAPI + harness, and the website from web/.
# Built from the repository root (see fly.toml), so the image holds part-a/ and part-b/.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils jq \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY part-b/requirements.txt part-b/requirements.txt
RUN pip install --no-cache-dir -r part-b/requirements.txt
COPY . .
WORKDIR /app/part-b
ENV RUNS_DIR=/data/runs PYTHONUNBUFFERED=1
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
