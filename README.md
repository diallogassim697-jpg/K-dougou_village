# Kédougou, terre des hommes

Site Django consacré à Kédougou : actualités, événements, histoire, galerie
photos, informations pratiques et contact.

Les coordonnées de contact et les repères historiques détaillés restent à
compléter avec des informations vérifiées et fournies localement.

## Installation locale (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Le site sera disponible sur http://127.0.0.1:8000/.

## Configuration

En local, Django utilise le mode développement. Pour un déploiement, définir
`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` et `DJANGO_ALLOWED_HOSTS` dans
l'environnement d'exécution. `.env.example` liste les variables attendues ;
ne jamais y placer de vraie clé secrète.

La base SQLite locale, l'environnement virtuel et les fichiers `.env` sont
ignorés par Git. Les photos du dossier `media/` sont des contenus du site et
restent versionnées. L'export `main/fixtures/initial_data.json` permet de
transférer les sept articles et les trois événements déjà publiés, avec leurs
liaisons aux photos.

## Mettre le site en ligne avec PythonAnywhere

PythonAnywhere convient à ce petit site Django avec SQLite. Créez un compte
sur [PythonAnywhere](https://www.pythonanywhere.com/), puis ouvrez une console
Bash dans votre tableau de bord.

### 1. Télécharger le projet et installer Django

Dans la console Bash, clonez le dépôt et créez un environnement virtuel avec
Python 3.13 (ou une version disponible compatible avec Django 6.1) :

```bash
git clone https://github.com/diallogassim697-jpg/K-dougou_village.git
cd K-dougou_village
mkvirtualenv --python=/usr/bin/python3.13 kedougou-venv
pip install -r requirements.txt
```

### 2. Créer l'application web

Dans l'onglet **Web**, ajoutez une application avec **Manual configuration**
et choisissez la même version de Python que l'environnement virtuel. Indiquez
`/home/VOTRE_NOM/K-dougou_village` comme répertoire du projet et de travail,
et `~/.virtualenvs/kedougou-venv` comme environnement virtuel. Remplacez
`VOTRE_NOM` par votre nom de compte PythonAnywhere.

Dans le fichier WSGI accessible depuis l'onglet **Web**, remplacez le contenu
par le bloc ci-dessous. Remplacez les valeurs indiquées ; générez une clé
secrète dans la console avec la commande Python indiquée après le bloc.
Gardez cette clé privée : ne l'ajoutez jamais à GitHub.

```python
import os
import sys

project_home = "/home/VOTRE_NOM/K-dougou_village"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ["DJANGO_SETTINGS_MODULE"] = "village_site.settings"
os.environ["DJANGO_DEBUG"] = "False"
os.environ["DJANGO_ALLOWED_HOSTS"] = "VOTRE_NOM.pythonanywhere.com"
os.environ["DJANGO_SECRET_KEY"] = "COLLER_ICI_VOTRE_CLE_SECRETE"

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

Pour générer la clé, activez d'abord l'environnement virtuel avec
`workon kedougou-venv`, puis exécutez :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé affichée dans le fichier WSGI, sans la publier ni la partager.

### 3. Préparer la base, les contenus et les fichiers statiques

Dans la console Bash :

```bash
cd ~/K-dougou_village
workon kedougou-venv
python manage.py migrate
python manage.py loaddata main/fixtures/initial_data.json
python manage.py collectstatic --noinput
```

`loaddata` importe les articles, événements et leurs photos dans la base en
ligne. Faites cette importation une seule fois sur une base neuve. Pour gérer
le site en ligne, vous pouvez aussi créer un compte administrateur avec
`python manage.py createsuperuser`.

### 4. Afficher les photos et le style

Dans la section **Static files** de l'onglet **Web**, ajoutez ces deux
correspondances en adaptant `VOTRE_NOM` :

| URL | Répertoire |
| --- | --- |
| `/static/` | `/home/VOTRE_NOM/K-dougou_village/staticfiles` |
| `/media/` | `/home/VOTRE_NOM/K-dougou_village/media` |

Cliquez sur **Reload** dans l'onglet **Web**. Votre site sera alors
accessible à l'adresse `https://VOTRE_NOM.pythonanywhere.com/`. Dans l'onglet
**Web**, activez aussi **Force HTTPS** pour rediriger les visiteurs vers la
connexion sécurisée. Le dépôt
GitHub contient le code et l'export des articles/événements ; la base en ligne
et les comptes d'administration restent séparés du dépôt.

## Envoyer le projet avec Git

Après avoir créé un dépôt vide sur GitHub ou un autre hébergeur Git, remplacer
les valeurs d'exemple par les vôtres :

```powershell
git config user.name "Votre nom"
git config user.email "votre-adresse@example.com"
git add .
git commit -m "Prepare Kédougou website"
git branch -M main
git remote add origin "https://github.com/VOTRE_COMPTE/NOM_DU_DEPOT.git"
git push -u origin main
```
