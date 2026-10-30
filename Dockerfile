FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATABASE=/data/accounts.db
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && mkdir /data && chown nobody:nogroup /data
COPY service ./service
USER nobody
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
