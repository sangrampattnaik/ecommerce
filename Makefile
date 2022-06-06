manage=./manage.py
python=python3
dev=--settings=ecommerce.settings.dev
prod=--settings=ecommerce.settings.prod
testing=--settings=ecommerce.settings.testing
staging=--settings=ecommerce.settings.staging

runserver-dev:
	$(python) $(manage) runserver 0.0.0.0:8000 $(dev)

runserver-prod:
	$(python) $(manage) runserver 0.0.0.0:8000 $(prod)

collectstaic:
	$(python) $(manage) collectstatic

check:
	$(python) $(manage) check

install:
	pip install -r requirements.txt

migrate-dev:
	$(python) $(manage) makemigrations $(dev) && $(python) $(manage) migrate $(dev)

freeze:
	pip freeze > requirements.txt

shell:
	$(python) $(manage) shell_plus

reset-db:
	$(python) $(manage) reset_db
	make migrate

db-backup:
	$(python) $(manage) db_backup

superuser:
	$(python) $(manage) superuser

woker:
	celery -A venya worker -l info

beat:
	celery -A venya beat -l info
