ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

wheelhouse/requirements.txt: $(REQUIREMENTS) Dockerfile
	mkdir -p $(WHEELHOUSE)
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/$(WHEELHOUSE):/wheelhouse \
	ccnmtl/django.build
	cp $(REQUIREMENTS) $(WHEELHOUSE)/requirements.txt
	touch $(WHEELHOUSE)/requirements.txt

build: $(WHEELHOUSE)/requirements.txt
	docker build -t $(IMAGE) .

compose-run:
	docker-compose up

compose-migrate:
	docker-compose run web migrate

compose-createsuperuser:
	docker-compose run web manage createsuperuser

.PHONY: build compose-run compose-migrate compose-superuser
