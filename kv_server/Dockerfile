FROM python:3.10.0

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kv_server/kv_server.py .
COPY kv_server/persistent_kv_store.py .

EXPOSE 5000

CMD ["python3", "kv_server.py"]