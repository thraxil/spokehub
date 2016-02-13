REPO=thraxil
APP=spokehub
MAX_COMPLEXITY=5

include *.mk

all: jenkins

deploy: ./ve/bin/python check jenkins
	./ve/bin/fab deploy

travis_deploy: ./ve/bin/python check jenkins
	./ve/bin/fab deploy -i spokehub_rsa
