up:
	docker compose up --build

up-d:
	docker compose up --build -d

down:
	docker compose down

web-install:
	cd apps/web && npm install

api-install:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

check:
	python3 -m compileall apps/api/app
	cd apps/web && npm test
