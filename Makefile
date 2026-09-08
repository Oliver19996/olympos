.PHONY: setup api web test seed check

setup:
	test -f backend/.env || cp backend/.env.example backend/.env
	python3 -m venv backend/.venv
	backend/.venv/bin/pip install -r backend/requirements.txt

api:
	cd backend && .venv/bin/python -m uvicorn app.main:app --reload --port 8000

web:
	cd web && python3 -m http.server 8080

test:
	cd backend && PYTHONPATH=. .venv/bin/python -m pytest -q

seed:
	backend/.venv/bin/python scripts/seed_demo.py

check:
	python3 -m py_compile backend/app/*.py scripts/seed_demo.py
	node --check web/app.js
