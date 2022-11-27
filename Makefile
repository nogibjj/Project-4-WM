install:
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	# format code
	black *.py mylib/*.py

lint:
	# pylint
	pylint --disable=R,C *.py mylib/*.py

test:
	# test
	python -m pytest -vv --cov=mylib --cov=main test_*.py

build:
	# build container

deploy:
	# deploy