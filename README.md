# django-bill-api
bill api source code.

## API Specification

|-|-|
|-|-|
|admin/ | |
| api/user/create/ | |
| api/user/token/ | |
| api/user/me/ | |
| api/bill/bills/ | |
| api/bill/bills_detail/ | |
| api/subscribes/ | |
| api/subscribes/{pk}/ | |

## Deployment note

### Environments

- Docker
- Nginx
- Gunicorn

### Installation

mkdir awslive && cd awslive
git pull git clone https://github.com/olvt01/billapi .
git checkout master

### Configuration files for deployment (Manually added)

awslive/docker-compose.prod.yml:
```yml
version: '3'

services:
  nginx:
    image: awslive-nginx:latest
    ports:
      - "80:80"
    volumes:
      - static_volume:/usr/src/app/staticfiles
      - media_volume:/usr/src/app/mediafiles
    depends_on:
      - web
    networks:
      - backend_net

  web:
    image: awslive-app:latest
    command: >
      sh -c  "python manage.py makemigrations &&
              python manage.py migrate &&
              python manage.py collectstatic --no-input &&
              gunicorn --bind app.wsgi:application --reload --bind 0.0.0.0:8000"
    volumes:
      - ./app/:/usr/src/app/
      - static_volume:/usr/src/app/staticfiles
      - media_volume:/usr/src/app/mediafiles
    environment:
      - DB_HOST=#####
      - DB_NAME=#####
      - DB_USER=#####
      - DB_PASS=#####
      - ALLOWED_HOSTS=#####
      - DEBUG=False
    networks:
      - backend_net

volumes:
  static_volume:
  media_volume:
networks:
  backend_net:
```

awslive/app/secrets.json:
```json
{
  "SECRET_KEY": "DJANGO SECRET KEY"
}
```

### Making images with Dockerfiles
docker build -t awslive-app app
docker build -t awslive-nginx nginx

### Deploying with Docker swarm
docker swarm init
docker stack deploy -c docker-compose.prod.yml awslive
