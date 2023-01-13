# Foodgram

### Описание проекта:

Делитесь и пробуйте новые рецепты.

### С помощью сервиса вы можете:
1) Создавать рецепты
2) Делиться рецептами
3) Подписываться на интересных вам авторов
4) Добавлять в избранное любимые рецепты
5) Искать рецепты по тегам
6) Добавить рецепты в список покупок и получить лист необходимых покупок для приготовления


### Используемые технологии

* Django
* Django Rest Framework
* Djoser
* Docker
* Nginx
* Postgresql

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:Ta9ear/foodgram-project-react.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Установить docker и docker-compose:

```
https://www.docker.com/
```

Подготовить файл .env на уровне проект:

```
SECRET_KEY=default-key #your secret key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres #db name 
POSTGRES_USER=postgres #db login
POSTGRES_PASSWORD=postgres #db password (make your own)
DB_HOST=db #db container name
DB_PORT=5432 #db port
```

Запустите следующие команды из папки infra/:

```
docker-compose up --build # expand the containers in the new structure
docker exec web python manage.py migrate # apply migrations
docker exec web python manage.py createsuperuser # create superuser
docker exec web python manage.py collectstatic --no-input # collect static
```

Загрузка тестовых данных:

```
docker exec web python manage.py laod_ingredients --path 'recipes/data/tags.csv' # load test tags
docker exec web python manage.py laod_ingredients --path 'recipes/data/ingredients.csv' # load test ingredients
```

Перейдите по адресу: http://localhost/


Посмотреть развернутый проект можно по ссылке:
http://51.250.87.105/

![Deploy badge](https://github.com/Ta9ear/yamdb_final/actions/workflows/foodgram_workflow.yml/badge.svg)
