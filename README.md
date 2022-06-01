# Описание сервиса:
### Тестовое для Webtr..
Нужно иметь модели User и Post(который создает конкретный User).
Реализовать авторизацию и логирование пользователя на сайте, возможность создавать пост и ставить like или unlike.
Авторизация через Токен JWT.
Остальное по усмотрению.

### Технологии
Python 3.7, Django, Django REST Framework

### API для сервиса позволяет:
- Создать пользователя
http://127.0.0.1:8000/signup/
- Залогиниться на сайте
http://127.0.0.1:8000/login/
- Получить токен
http://127.0.0.1:8000/token/
- Посмотреть посты
http://127.0.0.1:8000/posts/
- Создать пост
http://127.0.0.1:8000/posts/
- Поставить like залогининым пользователем
http://127.0.0.1:8000/posts/{id}/like/
- Поставить unlike залогининым пользователем
http://127.0.0.1:8000/posts/{id}/unlike/

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tochilkinva/webtro_test.git
```

```
cd webtro_test
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект из папки с manage.py:

```
python manage.py runserver
```

## Команды для загрузки данных в базу данных:

Загрузить данные в базу
```
python manage.py loaddata fixtures
```


## Подробную документацию с примерами запросов вы найдете по адресу:
http://127.0.0.1:8000/redoc/
