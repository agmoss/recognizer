SHELL := /bin/bash

COLOR_RESET=\033[0m
COLOR_CYAN=\033[1;36m
COLOR_GREEN=\033[1;32m
COLOR_RED=\033[1;31m

src = src
venv = .venv/bin/activate

.PHONY: install rm-venv deactivate-venv upgrade-poetry install-dependencies install-pre-commit post-install lint format typecheck test test-algo test-zum dotenv-init pre-commit clean changelog clean-build clean-pyc version-patch version-minor version-major

install: upgrade-poetry install-dependencies install-pre-commit post-install

rm-venv:
	@echo -e "$(COLOR_CYAN)Removing virtual environment$(COLOR_RESET)"
	$(RM) -rf .venv

deactivate-venv:
	@echo -e "$(COLOR_CYAN)Deactivating virtual environment$(COLOR_RESET)"
	exit

upgrade-poetry:
	@echo -e "$(COLOR_CYAN)Upgrading poetry...$(COLOR_RESET)"
	poetry self update

install-dependencies:
	@echo -e "$(COLOR_CYAN)Installing poetry dependencies...$(COLOR_RESET)"
	poetry install --no-root

install-pre-commit:
	@echo -e "$(COLOR_CYAN)Installing pre-commit hooks...$(COLOR_RESET)"
	pre-commit install

post-install:
	@echo -e "$(COLOR_GREEN)Install complete.$(COLOR_RESET)"
	@echo -e "$(COLOR_RED)YOU MUST ACTIVATE YOUR VIRTUAL ENVIRONMENT, RUN A: \"source .venv/bin/activate\"$(COLOR_RESET)"

lint:
	pylint $(src)

format:
	isort $(src)
	black $(src)

typecheck:
	mypy ./$(src) --check-untyped-defs

test:
	pytest tests

dotenv-init:
	cp -n .env.example .env

pre-commit:
	pre-commit run --all-files

clean: clean-build clean-pyc

changelog:
	git-changelog -io CHANGELOG.md -c angular

clean-build:
	$(RM) -fr build/
	$(RM) -fr dist/
	$(RM) -fr .eggs/
	find . -name '*.egg-info' -exec $(RM) -fr {} +
	find . -name '*.egg' -exec $(RM) -f {} +

clean-pyc:
	find . -name '*.pyc' -exec $(RM) -f {} +
	find . -name '*.pyo' -exec $(RM) -f {} +
	find . -name '*~' -exec $(RM) -f {} +
	find . -name '__pycache__' -exec $(RM) -fr {} +

version-patch:
	poetry version patch

version-minor:
	poetry version minor

version-major:
	poetry version major
