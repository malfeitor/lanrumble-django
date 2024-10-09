Install :
python -m venv /path/to/new/venv
. /path/to/new/venv/bin/activate
pip install -r requirements.txt
cp ./lanrumble_nginx_asgi.conf /etc/nginx/sites-availables
ln -s  /etc/nginx/sites-{availables,enabled}

.env :
EMAIL_HOST_PASSWORD
SECRET_KEY

Run :
service nginx start
. /path/to/new/venv/bin/activate
daphne -u /tmp/lanrumble.sock -e ssl:8000:privateKey=ca.key:certKey=ca.crt lanrumble.asgi:application


Note :
redis server (pour les websockets) https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

pour mise a jour :
git stash
git pull
git stash pop
