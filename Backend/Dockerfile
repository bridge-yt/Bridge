# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .. .

ENV FLASK_APP=app
ENV FLASK_ENV=production

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
