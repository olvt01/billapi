# django-bill-api
bill api source code.

## API Specifications

End point: http://ec2-13-209-42-228.ap-northeast-2.compute.amazonaws.com

|Url|Method|Specification|
|--|--|--|
| api/user/create/ | POST | Creating an user account |
| api/user/token/ | POST | Obtaing a token for authentication |
| api/user/me/ | GET, PUT, PATCH, HEAD | Managing an user |
| api/bill/bills/ | GET | Retrieving items / *Options for filtering & searching |
| api/bill/bills_detail/ | GET | Retrieving items / *Options for filtering & searching |
| api/subscribes/ | GET, POST | Creating or Retrieving user subscriptions |
| api/subscribes/{pk}/ | GET, PUT, PATCH, DELETE | Managing user subscriptions |
| api/bookmarks/ | GET, POST | Creating or Retrieving user bookmarks  |
| api/bookmarks/{pk}/ | GET, PUT, PATCH, DELETE | Managing user bookmarks |

## Skills

- Python
- Django
- Django Rest Framework
- PostgreSQL

## Deployment note

### Environments

- Docker
- Nginx
- Gunicorn

### Installation

```
mkdir awslive && cd awslive
git clone https://github.com/olvt01/billapi .
git checkout master
```

### Configuration files for deployment (Manually added)

1. awslive/docker-compose.prod.yml:
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
              gunicorn --bind 0.0.0.0:8000 app.wsgi"
    volumes:
      - ./app/:/usr/src/app/
      - static_volume:/usr/src/app/staticfiles
      - media_volume:/usr/src/app/mediafiles
    environment:
      - DB_HOST=#####
      - DB_NAME=#####
      - DB_USER=#####
      - DB_PASS=#####
      - DEBUG=False
      - ALLOWED_HOSTS=#####
      - CORS_ORIGIN_WHITELIST=#####
    networks:
      - backend_net

volumes:
  static_volume:
  media_volume:
networks:
  backend_net:
```

2. awslive/app/secrets.json:
```json
{
  "SECRET_KEY": "DJANGO SECRET KEY"
}
```

### Making images with Dockerfiles
```
docker build -t awslive-app app
docker build -t awslive-nginx nginx
```

### Deploying with Docker swarm
```
docker swarm init
docker stack deploy -c docker-compose.prod.yml awslive
```
