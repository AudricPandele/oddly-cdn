### Nothing to do here, refer to oddly-api to install

## Dependency for PGMAGICK 

### Install those libs on your systems :

```
sudo apt-get install libgraphicsmagick++1-dev
sudo apt-get install libgraphicsmagick++3 
sudo apt-get install libboost-python-dev
sudo apt-get install g++
```

Installer supervisor ( apt-get & pip )

Créer le fichier de conf dans le projet django cdn en copiant collant la config de celery sur leur git

créer un user celery ( si il ne s'est pas créé automatiquement ) et le metter dans la config supervisor. Mettre celery dans le meme groupe que celui qui a le droit de lire & ecrire les log + executer manage.py


- Preprod & Prod : 
  - L'utilisateur rentré dans supervisord.conf est www-data. Les logs appartiennent à celery:www-data
  - Ne pas oublier de chmod media -R avec www-data aussi, mais le dossier processed doit appartenir à oddly:oddly

_Pour lancer supervisord: dans le dossier du cdn, taper supervisord -c supervisord.conf_

**A placer dans /etc/rc0.d et le nommer K99worker**
``` 
#! bin/sh                                                                                                          
cd /home/oddly/domains/cdn.oddly.ninja/public_html && supervisord -c supervisord.conf   
```
