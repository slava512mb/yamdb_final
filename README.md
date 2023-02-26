![Yamdb Workflow Status](https://github.com/slava512mb/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# ЯП - Спринт 16 - CI и CD проекта api_yamdb (Яндекс.Практикум)


Проект развернут по адресу: http://158.160.2.107:8000/redoc/
## Описание 
 
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории:«Книги», «Фильмы», «Музыка».
Настроика для приложения Continuous Integration и Continuous Deployment, реализация:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.

Стек:
- Django 4.1.1
- DRF 3.14.0
- djangorestframework-simplejwt 5.2.1
- psycopg2-binary 2.9.3
- PyJWT 2.5.0

### Как запустить проект:
Все описанное ниже относится к ОС Linux.

### Клонируем репозиторий и и переходим в него:

```bash
git clone https://github.com/slava512mb/yamdb_final.git
```
```bash
cd yamdb_final
```

### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
```
- Windows:
```bash
source venv/Scripts/activate
```
- Linux:
```bash
source venv/bin/activate
```
### Обновим pip:
```bash
python -m pip install --upgrade pip 
```

### Ставим зависимости из requirements.txt:
```bash
pip install -r api_yamdb/requirements.txt 
```

### Переходим в папку с файлом docker-compose.yaml:
```bash
cd infra
```

### Предварительно установим Docker на ПК:
```bash
sudo apt update && apt upgrade -y
```
### Удаляем старый Docker:
```bash
sudo apt remove docker
```

### Устанавливаем Docker:
```bash
sudo apt install docker.io
```
### Смотрим версию Docker (должно выдать Docker version 20.10.16, build 20.10.16-0ubuntu1):
```bash
docker --version
```
### Активируем Docker в системе, что бы при перезагрузке запускался автоматом:
```bash
sudo systemctl enable docker
```
### Запускаем Docker:
```bash
sudo systemctl start docker
```
### Смотрим статус:
```bash
sudo systemctl status docker
```
### Не будет лишнем установить PostgreSQL:
```bash
sudo apt install postgresql postgresql-contrib -y
```

### Предварительно в папке infra создаем файл .env с следующим содержимом:
```bash
DB_ENGINE=название бд
DB_NAME=имя базы данных
POSTGRES_USER=логин для подключения к базе данных
POSTGRES_PASSWORD=пароль для подключения к БД установите свой
DB_HOST=название контейнера
DB_PORT=порт для подключения к БД
DB_PORT=порт для подключения к БД
SECRET_KEY=секретный ключ проекта django
```

### Так как требование ТЗ и тестов использовать postgresql, то создадим в системе бд:
```bash
sudo dpkg-reconfigure locales 
```
### Выбираем ru_RU.UTF-8 нажав пробел и ждем сообщения Generation complete.
```
Generating locales (this might take a while)...
...
  ru_RU.UTF-8... done
...
Generation complete.
```
### Перезапустим систему:
```bash
sudo reboot
```
### Установка PostgreSQL:
```bash
sudo apt install postgresql postgresql-contrib -y
```
### Управляем БД:
- Остановить
```bash
sudo systemctl stop postgresql
```
- Запустить
```bash
sudo systemctl start postgresql
```
- Перезапустить
```bash
sudo systemctl restart postgresql
```
- Узнать статус, текущее состояние
```bash
sudo systemctl status postgresql
```
### Создаем бд и пользователя:
```bash
sudo -u postgres psql
```
### Создаем базу:
```sql
CREATE DATABASE test_base;
```
### Создаем пользователя:
```sql
CREATE USER test_user WITH ENCRYPTED PASSWORD 'test_pass';
```
### Даем права для пользователя:
```sql
GRANT ALL PRIVILEGES ON DATABASE test_base TO test_user;
```
### Не забываем про установку, что мы сделали ранее, активировав venv:
```bash
pip install psycopg2-binary
```
```bash
pip install python-dotenv
```
### В settings.py добавляем следующее:
```python
from dotenv import load_dotenv

load_dotenv()

...

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default='5432')
    }
}
```
### Переходим в папку где находится файл settings.py. Создаем файл .env:
```bash
touch .env
```
```bash
nano .env
```
### Наполнение .env файла:
```bash
DB_ENGINE=название бд
DB_NAME=имя базы данных
POSTGRES_USER=логин для подключения к базе данных
POSTGRES_PASSWORD=пароль для подключения к БД установите свой
DB_HOST=название контейнера
DB_PORT=порт для подключения к БД
DB_PORT=порт для подключения к БД
SECRET_KEY=секретный ключ проекта django
```

### Не забываем про миграции (виртуальное окружение активировано):
```bash
python manage.py migrate
```
### Поднимаем контейнеры
    infra_db - база,
    infra_web - веб,
    nfra_nginx - nginx сервер
    может пригодится команда sudo systemctl stop nginx если запускаете в DEV режиме на ПК:
```bash
sudo docker-compose up -d --build 
```

### Выполняем миграции в контейнере infra_web:
```bash
sudo docker-compose exec web python manage.py makemigrations reviews 
```
```bash
sudo docker-compose exec web python manage.py migrate --run-syncdb
```
### Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser 
```

### Собираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input 
```

### Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json 
```

### Для заполнения базы тестовыми данными воспользуемся файлом fixtures.json, который находится в infra_sp2:
```bash
docker-compose exec web python manage.py loaddata fixtures.json
```

### Останавливаем контейнеры:
```bash
docker-compose down -v 
```

### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env
```bash
DB_ENGINE=название бд
DB_NAME=имя базы данных
POSTGRES_USER=логин для подключения к базе данных
POSTGRES_PASSWORD=пароль для подключения к БД установите свой
DB_HOST=название контейнера
DB_PORT=порт для подключения к БД
DB_PORT=порт для подключения к БД
SECRET_KEY=секретный ключ проекта django
```

### Документация API YaMDb 
Документация доступна по эндпойнту: http://158.160.2.107:8000/redoc/

### Выполнил: [Вячеслав Поликарский](https://github.com/slava512mb)
