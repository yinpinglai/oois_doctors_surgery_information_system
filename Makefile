.ONESHELL:

.PHONY: clean install init_db init_test_db test_server run_server start_server run_client start_client

python3 = /usr/local/opt/python@3.7/bin/python3
pip3 = /usr/local/opt/python@3.7/bin/pip3

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:
	python3 -m venv ./venv; \
	source ./venv/bin/activate; \
	pip3 install -r requirements.txt;

init_db:
	mysql -u root -p < init_db.sql

init_test_db:
	mysql -u root -p < init_test_db.sql

test_server:
	source ./venv/bin/activate; \
	python3 manage.py test_server

run_server:
	. venv/bin/activate; \
	python3 manage.py run_server

start_server: clean install init_db test_server run_server

run_client:
	. venv/bin/activate; \
	python3 manage.py run_client

start_client: run_client
