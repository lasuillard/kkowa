#!/usr/bin/env -S make -f

MAKEFLAGS += --warn-undefined-variable
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --silent

-include Makefile.*

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help

help: Makefile  ## Show help
	for makefile in $(MAKEFILE_LIST)
	do
		@echo "$${makefile}"
		@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' "$${makefile}" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
	done


# =============================================================================
# Common
# =============================================================================
install:  ## Install the app locally
	poetry install
.PHONY: install

init:  ## Initialize project repository
	pre-commit autoupdate
	pre-commit install --install-hooks --hook-type pre-commit --hook-type commit-msg
.PHONY: init

run:  ## Run GUI application
	dotenv poetry run python ./main.py app
.PHONY: run


# =============================================================================
# CI
# =============================================================================
ci: generate lint scan test benchmark e2e-test  ## Run CI tasks
.PHONY: ci

generate:  ## Generate codes from schemas
	mkdir -p _generated/grpc

	function sig() {
		# tar cf - _generated/ | sha1sum | awk '{ print $$1 }'
		find _generated -type f -print0 | sort -z | xargs -0 sha1sum | sha1sum | awk '{ print $$1 }'
	}

	before="$$(sig)"
	poetry run python -m grpc_tools.protoc \
		--proto_path=idl/grpc \
		--grpc_python_out=_generated/grpc \
		--python_out=_generated/grpc \
		--pyi_out=_generated/grpc \
		idl/grpc/*.proto
	after="$$(sig)"

	if [[ "$$after" != "$$before" ]]; then
		echo 'There are changes in generated stubs.'
		exit 1
	fi
.PHONY: generate

format:  ## Run autoformatters
	poetry run ruff check --fix .
	poetry run black .
.PHONY: format

lint: generate  ## Run all linters
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy --show-error-codes --pretty .
.PHONY: lint

scan:  ## Run all scans
	checkov --quiet --directory .
.PHONY: scan

test: generate  ## Run tests
	poetry run pytest
.PHONY: test

benchmark:  ## Run benchmarks
	poetry run pytest --benchmark-only -n 0
.PHONY: benchmark

e2e-test: generate  ## Run e2e tests

.PHONY: e2e-test

build: generate  ## Build application
	poetry run pyinstaller \
		--onefile \
		--hidden-import opentelemetry-sdk \
		--copy-metadata opentelemetry-sdk \
		main.py
.PHONY: build

docs:  ## Generate dev documents

.PHONY: docs


# =============================================================================
# Handy Scripts
# =============================================================================
clean:  ## Remove temporary files
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ build/ dist/ htmlcov/ .coverage coverage.xml report.xml
	find . -path '*/__pycache__*' -delete
	find . -path "*.log*" -delete
.PHONY: clean
