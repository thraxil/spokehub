[![Build Status](https://travis-ci.org/thraxil/spokehub.svg?branch=master)](https://travis-ci.org/thraxil/spokehub)
[![Coverage Status](https://coveralls.io/repos/github/thraxil/spokehub/badge.svg?branch=master)](https://coveralls.io/github/thraxil/spokehub?branch=master)

# Spokehub Website

## Installation/setup

If you have Python and a basic build environment, you can check out
the code and run the unit tests by running

```
$ make
```

That will install all the python requirements into a local virtualenv
and then run the test suite.

To run a development server, the only other thing you need is a
database. If you have postgres running and your current user has
password-less access to it, you can do:

```
$ createdb spokehub
$ make migrate
```

which will create the initial database schema.

If you need a different database setup, create a
`spokehub/local_settings.py` file and drop in a standard Django
database config stanza there to point to the DB you want to use (that
file is ignored by git). Then you can create the database and run
`make migrate` to set it up.

After that, you'll probably want a superuser so you can login:

```
$ ./manage.py createsuperuser
```

Then you can start up a dev server on port 8000 with:

```
$ make runserver
```

`make` is smart enough to detect changes to `requirements.txt` and
`package.json` and automatically re-build/re-install whatever is
necessary to keep things up to date. (sometimes when you run `make
runserver` it will do a bunch of stuff before actually starting up the
dev server; this is why).

## Contributing

* the unit tests must all pass
* code must pass `flake8` (automatically run by `make`)

Spokehub is
[continuously deployed](https://www.thoughtworks.com/continuous-delivery),
so if those checks pass, the code will be automatically deployed to
the production server. This means:

* Make sure you are ready. Don't check code into `master` if you
  aren't sure. Make a PR and ask for a code review if in doubt.
* Use feature flags liberally (spokehub uses
  [waffle](http://waffle.readthedocs.io/)) to deploy code without
  releasing.
  
## SASS/client-side asset pipeline

TODO

## Docker

If you have [Docker](https://www.docker.com/) and
[Docker Compose](https://docs.docker.com/compose/) installed on your
system, you can use that for a very easy dev setup.

(Note: if you're running on OS X or in a virtual machine, there might
be some extra complexity as far as setting up port mapping for the
VM. The rest of this is written assuming that you're either running on
Linux, or that you are familiar enough with your docker setup to make
the necessary adjustments)

```
$ make build
$ make compose-migrate
$ make compose-createsuperuser
$ make compose-run
```

The first step will take a while since it's building the image from scratch

From then on, you'll mostly just need to run `make compose-run` to
start up the dev server.

Some caveats:

Unlike the "plain" non-docker setup above, the Makefile isn't clever
enough to rebuild things when `requirements.txt` or `package.json`
changes. You'll want to watch those yourself and just re-run `make
build` anytime there are changes to either of those files.
  
Similarly, if you see any new migrations (any files with `migrations/`
in the filename) come across, you'll need to run `make
compose-migrate` to apply those migrations to the database.

You can run arbitrary Django "manage.py" commands within the docker
environment like:

```
$ docker-compose run web manage help
$ docker-compose run web manage shell
```

etc. Note that it is `manage` there, not `manage.py`
