# Makefile for my Python project

.PHONY: build run test clean

install:
	pip install -r requirements.txt

build_docker:
	docker compose up --build

format:
	black .

isort:
	isort .

pylint:
	pylint .

test: 
	python -m unittest discover -s tests

real_test_scenario: 
	python tests/matching_algorithm_test/simulate_real_scenario.py

run:
	uvicorn src.app:app --host 0.0.0.0 --port 8080

