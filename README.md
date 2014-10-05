## Oddly API

### Oddly 101 : how to clone

First of all, just create a new folder called "oddly" ( no shit ). Then clone it like a dude, ( don't forget to add a dot after clone, to put everything at the root folder  git clone @somebullshit . )

### Oddly 102 : Shit needed

**Virtualenv - VirtualenvWrapper**

This is used to install separated evironment in your system, to avoid conflict. ( It's obviously not smart to put every package on the system directly )
There's two packages, **virtualenv** and **virtualenvwrapper**

_Install python-dev:_
`sudo apt-get install python-dev`

**Then, install PIP** 

`sudo apt-get install pip`

**With PIP, install those packages**

```
pip install virtualenv
pip install virtualenvwrapper
```

**Put virtualenwrapper in your PATH ( you don't want to source virtualenvwrapper each time )**

```
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
```

**If when you exit your shell and reopen it, workon don't work ( kind of funny, no ? ), add this to your bashrc ( or whatever it is ) :**

`source /usr/local/bin/virtualenvwrapper.sh`

**You only have to know two commands**

```
mkvirtualenv env ( ou env = nom de l'env )
workon env
```

_To quit, just type "deactivate"_

**To install pip dependency :**

`pip install -r requirements.txt`

_If you have somme issues like GCC exit with failed status 1, install those motherfucker :_
```
sudo apt-get install python-dev
sudo apt-get install libxml2-dev libxslt-dev
sudo apt-get install zlib1g-dev
```

[MONGODB]

http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb

[MONGODB POUR DJANGO]

http://django-mongodb-engine.readthedocs.org/en/latest/topics/setup.html


### Howto : Put this mess in production

In case of you're using virtualmin, it create a .conf file that allow you to configure your app throught it.

So, open your .conf ( in this case, oddly.conf ) and add those lines at the top, outside <VirtualHost>:

```
WSGIPythonPath /home/oddly/public_html:/home/USER/.virtualenvs/NAMEOFTHEVIRTUALENV/local/lib/python2.7/site-package
```

Put this in the <VirtualHost> block. If you dont, you'll screw your whole Vhost. It sucks.

```
WSGIScriptAlias / /home/oddly/public_html/core/wsgi.py
```

In <Directory /home/oddly/public_html> , add those lines too :

```
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
```

Don't forget to start mongod service, 

Run ./manage.py syncdb

You're set !

### Module Cross Origin

https://github.com/OttoYiu/django-cors-headers
