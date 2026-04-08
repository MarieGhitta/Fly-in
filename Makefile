PYTHON = python3
MAIN = main.py
REQUIREMENTS = requirements.txt
CONFIG = config.py

all: run

install:
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf .mypy_cache .pytest_cache .DS_Store
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +


lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy --strict .


.PHONY: all install run debug clean lint lint-strict