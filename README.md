# yatube_project
### ��������
���������� ���� ��������
### ����������
Python 3.7
Django 2.2.19
### ������ ������� � dev-������
- ���������� � ����������� ����������� ���������
```
python -m venv venv
source venv/Scripts/activate
deactivate 
```
- ���������� ����������� �� ����� requirements.txt
```
pip install -r requirements.txt
``` 
- � ����� � ������ manage.py ��������� �������:
```
python manage.py runserver
```
- ������� �������� ������� ��������
- ��������� ��� ��������
```
python manage.py makemigrations
python manage.py migrate
```
- ��� �������� ����������������� ��������� �������:
```
python manage.py createsuperuser
adm adm
```
```
- shell
```
python manage.py shell 

### ������
https://github.com/crazair

python manage.py startapp core 

python -m unittest -v tests.py
python manage.py test
python manage.py test posts.tests.test_urls -v 2 
coverage run --source='posts,users' manage.py test posts.tests.test_urls -v 2
coverage report
