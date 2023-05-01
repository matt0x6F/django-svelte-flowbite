local:
	docker compose up --build

migrations:
	docker compose exec backend ./manage.py makemigrations && docker compose exec backend ./manage.py migrate

clean:
	rm -rf frontend/node_modules && rm -rf frontend/.svelte-kit && rm -rf frontend/package-lock.json
	cd frontend && npm install