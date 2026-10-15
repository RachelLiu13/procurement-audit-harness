# The agent server (FastAPI + harness). Deployed on Render; the Vercel site forwards /api/* here.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils jq \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV RUNS_DIR=/tmp/audit-planner-runs PYTHONUNBUFFERED=1
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}"]
