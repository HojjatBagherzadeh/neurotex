FROM python:3.12-slim

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY app/ app/

# Ensure repos folder exists with proper permissions
RUN mkdir -p /app/repos && chmod -R 777 /app/repos

# Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Port exposure
EXPOSE 8001

# Force Python to flush logs immediately
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
