FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

EXPOSE 8000


CMD ["./entrypoint.sh"]

# docker-compose up
# to create a super user run:
## docker exec -it django-backend /bin/bash
## python manage.py createsuperuser
