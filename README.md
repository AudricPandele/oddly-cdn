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

Attention, donner les droits à www-data:www-data sur le dossier media, sinon apache pourra pas écrire dedans.


Preprod : L'utilisateur rentré dans supervisord.conf est www-data. Les logs appartiennent à celery:www-data

Pour lancer supervisord: dans le dossier du cdn, taper supervisord -c supervisord.conf

Faire un script bash pour le lancer au démarrage
