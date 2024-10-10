FROM python:3.11-alpine AS build

RUN apk add --update --virtual .build-deps \
    build-base \
    python3-dev
COPY requirements.txt .
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt --target=packages

FROM python:3.11-alpine AS runtime
COPY --from=build packages /usr/lib/python3.11/site-packages
ENV PYTHONPATH=/usr/lib/python3.11/site-packages

COPY --from=build /app /app
WORKDIR /app
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "daphne", "-e", "ssl:8000:privateKey=ca.key:certKey=ca.crt", "lanrumble.asgi:application"]
