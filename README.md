# Lan Rumble django code

to use it you must do :
- pull image (docker pull armitage1/lanrumble-django) -OR- clone this repo
- create a docker compose with a postgres image for DB
- volume for media
- volume for logs
- __secret for certificates__
- secret for sendgrid's api key
- __secret for django key__
- environment for DB connection

## compose.yaml example :

```
services:
  back:
    build: .
    image: armitage1/lanrumble-django
    restart: always
    depends_on:
      - db
    ports:
      - 8000:8000
    volumes:
      - media:/app/jeux/media
      - logs:/var/log/
    secrets:
      - source: crt
        target: /app/ca.crt
      - source: key
        target: /app/ca.key
    environment:
      SECRET_KEY : ${SECRET_KEY}
      EMAIL_HOST_PASSWORD : ${EMAIL_HOST_PASSWORD}
      DEBUG : ${DEBUG}
      POSTGRES_DATABASE : django
      POSTGRES_USER : django
      POSTGRES_PASSWORD : ${POSTGRES_PASSWORD}
      POSTGRES_HOST : db

  db:
    image: postgres:latest
    restart: always
    environment:
      POSTGRES_ROOT_PASSWORD : ${POSTGRES_ROOT_PASSWORD}
      POSTGRES_DATABASE : django
      POSTGRES_USER : django
      POSTGRES_PASSWORD : ${POSTGRES_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data: {}
  media: {}
  logs: {}

secrets:
  crt:
    file: ./ca.crt
  key:
    file: ./ca.key
  django_secret:
    environment: SECRET_KEY
  email_host_password:
    environment: EMAIL_HOST_PASSWORD
```