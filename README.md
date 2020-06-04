# Тест sibdev
## Зависимости
python3.6, sqlite 

## Разворачивание и запуск проекта
Клонировать репозиторий проекта локально  
`git clone https://github.com/hazarin/sdtest.git` 

### Без docker
Создать и активировать новую виртуальную среду 
```
cd sdtest
python -m venv venv
source ./venv/bin/activate
```
Выполнить установку зависимостей проекта  
`pip install -r requirements.txt`  
Выполнить миграции и загрузку фикстур  
`python manage.py migrate`  
`python manage.py loaddata.shedule.json` - расписание рассылки для Django-q  
`python manage.py load_participants participants.jsonl` - предпочтения и участники  
Запустить сервер разработки и кластер очередей django-q  
`python manage.py qcluster & python manage.py runserver 127.0.0.1:8000`

### Запуск проекта с использованием docker
```
cd sdtest
docker-compose up -d
```

После этого проект доступен по адресу: http://localhost:8000
Администратор:  
login: *admin@admin.com* 
password: *admin* 
