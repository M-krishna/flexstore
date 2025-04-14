FROM python:3.10.0

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service_registry/service_registry.py .

EXPOSE 8000

CMD ["python3", "service_registry.py"]