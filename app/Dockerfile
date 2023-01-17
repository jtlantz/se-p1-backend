FROM python:3.10-slim

WORKDIR /app
COPY /backend /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations

CMD ["gunicorn", "-b", "0.0.0.0:8000", "backend.wsgi"]
EXPOSE 8000