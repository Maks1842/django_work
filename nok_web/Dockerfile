FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/docker-entrypoint
COPY . /app/
RUN chmod +x /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]