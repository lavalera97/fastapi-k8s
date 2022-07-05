FROM python:3.9.13-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000
RUN useradd app

RUN apt-get update && apt-get install -y curl iputils-ping && apt-get upgrade -y

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

COPY ./src /app

USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]