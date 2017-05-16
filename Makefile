migrate:
	python manage.py makemigrations accounts companys job newletters
	python manage.py migrate

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

test:
	python manage.py test

lint:
	flake8 --exclude migrations/,env/ .

ci: lint test
