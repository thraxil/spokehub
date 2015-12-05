REPO=thraxil
APP=spokehub

include *.mk

deploy: ./ve/bin/python validate jenkins
	./ve/bin/fab deploy

travis_deploy: ./ve/bin/python validate jenkins
	./ve/bin/fab deploy -i spokehub_rsa
