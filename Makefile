migrate: migrations
	python manage.py migrate

migrations:
	python manage.py makemigrations accounts companys job newletters

run:
	python manage.py runserver

collect:
	python manage.py collectstatic

remove:
	git rm -rf companys/migrations/.
	git rm -rf accounts/migrations/.
	git rm -rf job/migrations/.
	git rm -rf newletters/migrations/.

service:
	python3 services/services.py

shell:
	python manage.py shell -i ipython

test: migrations
	python manage.py test --verbosity 3

lint:
	flake8 --exclude manage.py,migrations/,settings/,venv/,env/ .

ci: lint test
