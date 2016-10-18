ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

build:
	docker build -t $(IMAGE) .

compose-run:
	docker-compose up

compose-migrate:
	docker-compose run web migrate

compose-createsuperuser:
	docker-compose run web manage createsuperuser

compose-waffle-flags:
	docker-compose run web manage waffle_flag main --everyone --create

.PHONY: build compose-run compose-migrate compose-superuser
