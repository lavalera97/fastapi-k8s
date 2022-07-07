export COMPOSE_PROJECT_NAME=web
export COMPOSE_FILE=./ci/docker-compose.yml

up:
	docker-compose up

build:
	docker-compose build

create_migration:
	docker-compose run web alembic revision --autogenerate

migrate:
	docker-compose run web alembic upgrade head

downgrade:
	docker-compose run web alembic downgrade -1
