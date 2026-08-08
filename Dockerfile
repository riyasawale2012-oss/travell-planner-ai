FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 libffi-dev shared-mime-info && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
ENV PYTHONPATH=/app
ENV APP_ENV=production
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
