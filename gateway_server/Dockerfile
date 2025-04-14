FROM python:3.10.0

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gateway_server/gateway_server.py .

EXPOSE 8002

CMD ["python3", "gateway_server.py"]