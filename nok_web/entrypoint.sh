#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Ожидаем постгрес..." "$SQL_HOST" "$SQL_PORT" "..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL запущен"
fi

#python manage.py flush --no-input
python manage.py migrate

exec "$@"