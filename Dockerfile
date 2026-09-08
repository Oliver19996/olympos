FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend backend
COPY web web
WORKDIR /app/backend
ENV OLYMPOS_ENV=production
ENV OLYMPOS_CORS_ORIGINS=*
ENV OLYMPOS_DB_PATH=/data/olympos_phase0.db
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
