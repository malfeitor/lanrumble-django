FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["daphne", "-e", "ssl:8000:privateKey=ca.key:certKey=ca.crt", "lanrumble.asgi:application"]
