# docker-compose project makefile

PROJECT:=$(notdir $(shell pwd))
DC:=docker-compose --env-file .env
BUILD_ARGS:=--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) 
BUILD:=${DC} build ${BUILD_ARGS}

ps:
	@${DC} ps

build:
	${BUILD}

rebuild: 
	${BUILD} --no-cache

run:
	${DC} run ${PROJECT}

start:
	${DC} up -d

stop:
	${DC} down --remove-orphans

shell:
	${DC} exec ${PROJECT} /bin/bash -l

tail:
	@${DC} logs --follow --tail="all" ${PROJECT}

plan:
	${DC} run ${PROJECT} bash -c 'make plan'
