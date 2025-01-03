build:
	docker compose up -d --force-recreate

down:
	docker compose down --rmi local

