# Comprendeshi - Projet Flask Intégrateur

Projet Flask complet et professionnel couvrant toutes les sections du tutoriel Flask GeeksforGeeks.

## Fonctionnalités

- **Authentification** : Inscription, connexion, profil, changement de mot de passe, rôles (user/admin)
- **CRUD complet** : Articles avec tags, pagination, brouillons
- **Upload de fichiers** : Envoi sécurisé avec validation de type et taille
- **API REST** : Endpoints JSON avec pagination, recherche et filtrage
- **Blueprints** : Architecture modulaire (main, auth, dashboard, api, errors)
- **Formulaires** : Flask-WTF avec validation et protection CSRF
- **Base de données** : SQLAlchemy avec migrations Alembic
- **Middleware** : Hooks before/after request, logging
- **Gestion d'erreurs** : Pages 403, 404, 500 personnalisées
- **Docker** : Prêt pour la production

## Installation

### Prérequis
- Python 3.9+
- pip

### Installation locale

```bash
# Cloner et aller dans le projet
cd projet_flask

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier de configuration
cp .env.example .env

# Initialiser la base de données
flask --app run:app db init
flask --app run:app db migrate -m "Initial migration"
flask --app run:app db upgrade

# Lancer l'application
python run.py
```

L'application sera accessible sur http://localhost:5000

### Docker

```bash
docker-compose up --build
```

## Structure du projet

```
projet_flask/
├── app/
│   ├── __init__.py         # Application factory
│   ├── config.py           # Configuration (dev/prod/test)
│   ├── extensions.py       # Extensions Flask
│   ├── models/             # Modèles SQLAlchemy (User, Post, File, Tag)
│   ├── routes/             # Blueprints (main, auth, api, dashboard, errors)
│   ├── templates/          # Templates Jinja2
│   ├── static/             # CSS, JS, uploads
│   ├── forms/              # Formulaires Flask-WTF
│   └── utils/              # Décorateurs et helpers
├── tests/                  # Tests pytest
├── run.py                  # Point d'entrée développement
├── wsgi.py                 # Point d'entrée production (Gunicorn)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API REST

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/v1/posts` | Liste des articles (pagination, recherche) |
| GET | `/api/v1/posts/<id>` | Détail d'un article |
| POST | `/api/v1/posts` | Créer un article (auth) |
| PUT | `/api/v1/posts/<id>` | Modifier un article (auth) |
| DELETE | `/api/v1/posts/<id>` | Supprimer un article (auth) |
| GET | `/api/v1/tags` | Liste des tags |
| GET | `/api/v1/users` | Liste des utilisateurs (admin) |

### Paramètres de requête (GET /api/v1/posts)
- `page` : numéro de page (défaut: 1)
- `per_page` : résultats par page (défaut: 10, max: 50)
- `q` : recherche dans le titre et le contenu
- `tag` : filtrer par tag

## Tests

```bash
pytest
pytest -v              # Mode verbose
pytest tests/test_api.py  # Tests API uniquement
```

## Technologies

- Flask 3.1.2
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Flask-RESTful 0.3.10
- SQLite (dev) / PostgreSQL (prod)
- Gunicorn (production)
- Docker
