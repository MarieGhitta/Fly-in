PYTHON = python3
MAIN = main.py
REQUIREMENTS = requirements.txt
CONFIG = config.py

all: run

install:
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

run:
	@map=$$(find maps -name "*.txt" | sort | gum choose); \
	$(PYTHON) $(MAIN) $$map

debug:
	@map=$$(find maps -name "*.txt" | sort | gum choose); \
	$(PYTHON) -m pdb $(MAIN) $$map

clean:
	rm -rf .mypy_cache .pytest_cache .DS_Store
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +


lint:
	$(PYTHON) -m flake8 src main.py
	$(PYTHON) -m mypy src main.py

lint-strict:
	$(PYTHON) -m flake8 src main.py
	$(PYTHON) -m mypy --strict src main.py


.PHONY: all install run debug clean lint lint-strict