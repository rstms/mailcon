# docker-compose project makefile

PROJECT:=$(notdir $(shell pwd))
DC:=docker-compose --env-file .env
BUILD_ARGS:=--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) 
BUILD:=${DC} build ${BUILD_ARGS}

ps:
	@${DC} ps

clean:
	cd ${PROJECT}/src && make clean

build: clean
	${BUILD}

rebuild: clean
	${BUILD} --no-cache

run:
	${DC} run ${PROJECT} ${CMD}

dev:
	${DC} run -e DEVMODE=1 ${PROJECT}

start:
	${DC} up -d

stop:
	${DC} down --remove-orphans

tail:
	@${DC} logs --follow --tail="all" ${PROJECT}

plan:
	${DC} run ${PROJECT} bash -c 'make plan'
