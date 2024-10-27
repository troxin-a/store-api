up:
	docker compose up -d --build

migrate:
	docker compose exec app alembic upgrade head

csu:
	docker compose exec -it app /bin/sh -c "cd /app/src && python -m services.create_admin"

down:
	docker compose down