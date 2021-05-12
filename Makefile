all:
	python website/manage.py runserver

database:
	python website/manage.py makemigrations
	python website/manage.py migrate