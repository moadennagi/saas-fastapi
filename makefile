install:
	pip install --upgrade pip && \
	pip install -r requirements.txt
test:
	coverage run -m pytest && coverage report
all: install test