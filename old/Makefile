.PHONY: migrations
migrations:
	@echo "Making migrations..."
	@./manage.py makemigrations
	@echo "Migrating..."
	@./manage.py migrate

.PHONY: frontend
frontend:
	@echo "Starting frontend server..."
	@cd frontend && npm run dev

.PHONY: backend
backend:
	@echo "Starting backend server..."
	@DJANGO_DEBUG=on ./manage.py runserver

test:
	@which python3

.PHONY: assets
assets:
	@echo "Collecting static files..."
	@cd frontend && npm run build:tailwind