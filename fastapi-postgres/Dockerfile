FROM python:3.10-slim

RUN groupadd -r mygroup && useradd -r -g mygroup myuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER myuser

ENTRYPOINT ["uvicorn"]
CMD ["app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
