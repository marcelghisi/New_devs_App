dev:
	$(MAKE) back & $(MAKE) front & wait

infra:
	docker compose up db redis

back:
	cd backend && \
	DATABASE_URL=postgresql://postgres:postgres@localhost:5433/propertyflow \
	REDIS_URL=redis://localhost:6380/0 \
	SECRET_KEY=debug_challenge_secret \
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

front:
	cd frontend && npm run dev

pre-commit:
	cd backend && uv add --dev pre-commit
	uv run pre-commit install --install-hooks --overwrite

uv-install:
	cd backend && uv sync
