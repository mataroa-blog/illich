#!/usr/local/bin/bash

set -e
set -x

# pull latest changes
ssh root@95.217.223.96 'cd /opt/apps/illich && git pull'

# sync requirements
ssh root@95.217.223.96 'cd /opt/apps/illich && source venv/bin/activate && pip install -r requirements.txt'

# collect static
ssh root@95.217.223.96 'cd /opt/apps/illich && source venv/bin/activate && python manage.py collectstatic --noinput'

# migrate database
ssh root@95.217.223.96 'cd /opt/apps/illich && source venv/bin/activate && source .envrc && python manage.py migrate'

# reload
ssh root@95.217.223.96 'cd /opt/apps/illich && uwsgi --reload /etc/uwsgi/vassals/illich.ini'

# copy and reload nginx config
ssh root@95.217.223.96 'cp /opt/apps/illich/collection.mataroa.blog.conf /etc/nginx/sites-available/ && nginx -t && systemctl reload nginx'
