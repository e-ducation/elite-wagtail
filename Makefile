.PHONY: help

help: ## display help message
	@echo "Please user 'make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

static: ## compile static
	@cd ./elite_wagtail/elite_wagtail/static && sass --update sass:css

run:
	source env/bin/activate && cd elite_wagtail && python manage.py runserver
