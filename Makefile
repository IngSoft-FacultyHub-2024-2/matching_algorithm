# Makefile for my Python project

.PHONY: build run test clean

test: 
	python -m unittest discover -s tests

real_test_scenario: 
	python tests/matching_algorithm_test/simulate_real_scenario.py