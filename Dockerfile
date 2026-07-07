FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

<<<<<<< HEAD:DockerFile
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
=======
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> ddea9b8b1914c90fcb421c068b44de0d258e0122:Dockerfile
