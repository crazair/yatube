# yatube_project
### Описание
Социальная сеть блогеров
### Технологии
Python 3.7
Django 2.2.19
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
deactivate 
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
- команда создания скрипта миграций
- запустить все миграции
```
python manage.py makemigrations
python manage.py migrate
```
- Для создания суперпользователя выполните команду:
```
python manage.py createsuperuser
adm adm
```
```
- shell
```
python manage.py shell 

### Авторы
https://github.com/crazair

python manage.py startapp core 

python -m unittest -v tests.py
python manage.py test
python manage.py test posts.tests.test_urls -v 2 
coverage run --source='posts,users' manage.py test posts.tests.test_urls -v 2
coverage report
