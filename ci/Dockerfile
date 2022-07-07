FROM python:3.9.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.1.13

RUN apt-get update && apt-get install -y curl iputils-ping && apt-get upgrade -y
RUN pip install --upgrade pip "poetry==$POETRY_VERSION"

EXPOSE 8000
RUN useradd app

WORKDIR /app
COPY ../poetry.lock ../pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY ../src /app

USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]