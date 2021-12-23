.DEFAULT_GOAL := say_hello
# .PHONY: test

# .PHONY: all say_hello generate clean

# fix tabs - perl -pi -e 's/^  */\t/' Makefile
# test:
# 	PYTHONPATH=. pytest

say_hello:
	@echo "Hello World"

clean:
	@echo "Clean Up..."
	find . -type f -iname ".DS_Store" -delete
	find . -type d -iname ".pytest_cache" -exec rm -r {} +
	find . -type d -iname "__pycache__" -exec rm -r {} +

test:
	@echo "Testing..."
	poetry run pytest -vrP src/tests/

deploy:
	@echo "Deploying to fold..."
	poetry run python src/deploy.py

lint:
	@echo "Linting..."
	poetry run black src/
	poetry run flake8 src/