FROM python:3.10-slim



WORKDIR /app
ADD docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
COPY /backend /app
COPY requirements.txt .

RUN pip3 install -r requirements.txt


CMD './docker-entrypoint.sh'
EXPOSE 8000
