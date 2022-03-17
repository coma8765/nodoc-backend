include .env

all:
	echo "commands: dev(.docker or .local), start(.local or .docker), black"

install.local:
	pipenv install

start.docker:
	docker build --name ${DOCKER_API_NAME} --target prod .;
	docker-compose up -d
