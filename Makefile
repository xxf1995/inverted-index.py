init:
	pip install -r requirements.txt

test:
	pytest tests/ --cov inverted_index/ --cov-report term-missing