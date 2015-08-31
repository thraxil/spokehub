[![Build Status](https://travis-ci.org/thraxil/spokehub.svg?branch=master)](https://travis-ci.org/thraxil/spokehub)

## Development setup

Download:

1. [Node](https://nodejs.org/)

2. [Grunt](http://gruntjs.com/getting-started)

3. [Bower](http://bower.io/)

4. [Vagrant](https://www.vagrantup.com/)

open whatever terminal or terminal emulator you prefer and run:

```
vagrant up
vagrant ssh
```

Now you'll be in a virtual linux box from here you need to make a couple users and then run the server.

```
sudo -i -u postgres
createuser -s vagrant
createuser -s root
cd /vagrant/
```

This is probably the first time you're setting this up. If so you'll want to run:

```
make install
make migrate
```

then you can start a development server

```
./manage.py runserver 0.0.0.0:8000
```

Leave that session running and in a new tab run
```
npm install
bower install
grunt build
grunt
```

Now you can open localhost:8080 and you should see the site up and running.
