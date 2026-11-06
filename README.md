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
restent versionnées.

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
