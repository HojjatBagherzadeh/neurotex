FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
COPY app/ app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
