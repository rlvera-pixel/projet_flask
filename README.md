# Comprendeshi - Projet Flask Integrateur

Projet Flask complet et professionnel realise dans le cadre d'un apprentissage du framework Flask.
Ce projet couvre **toutes les sections du tutoriel Flask de GeeksforGeeks** en les integrant dans une architecture propre et modulaire.

---

## Table des matieres

1. [Ce qui a ete fait](#ce-qui-a-ete-fait)
2. [Structure du projet](#structure-du-projet)
3. [Installation](#installation)
4. [Lancer l'application](#lancer-lapplication)
5. [Fonctionnalites detaillees](#fonctionnalites-detaillees)
6. [API REST](#api-rest)
7. [Tests](#tests)
8. [Docker](#docker)
9. [Technologies](#technologies)

---

## Ce qui a ete fait

### Avant (branche `main`)
Le projet initial etait un seul fichier `run.py` de 109 lignes avec toutes les routes melangees, pas de base de donnees, un login en dur (admin/admin), et aucune structure.

### Apres (branche `tuto_flask`)
Le projet a ete entierement restructure en architecture professionnelle :

| Aspect | Avant | Apres |
|--------|-------|-------|
| Architecture | 1 fichier `run.py` | Application factory + Blueprints |
| Base de donnees | Aucune | SQLAlchemy + migrations Alembic |
| Authentification | Login en dur (admin/admin) | Flask-Login, hashing de mots de passe, roles |
| Formulaires | HTML brut sans validation | Flask-WTF avec validation + CSRF |
| API | Aucune | REST API complete avec JSON |
| Templates | 8 fichiers en vrac | 18 templates organises par section |
| CSS | Styles inline dans base.html | Fichier CSS complet et responsive |
| Tests | Aucun | 29 tests unitaires (tous passent) |
| Deploiement | `python run.py` | Docker + Gunicorn |
| Fichiers | ~10 fichiers | ~45 fichiers organises |

---

## Structure du projet

```
projet_flask/
├── app/
│   ├── __init__.py              # Application factory (create_app)
│   │                            #   - Initialise les extensions
│   │                            #   - Enregistre les blueprints
│   │                            #   - Configure les hooks (before/after request)
│   │                            #   - Enregistre les filtres Jinja2 personnalises
│   │                            #   - Configure le logging
│   │
│   ├── config.py                # 3 configurations : Development, Production, Testing
│   ├── extensions.py            # Extensions Flask (db, migrate, login_manager, csrf)
│   │
│   ├── models/                  # Modeles de base de donnees
│   │   ├── user.py              #   - User : username, email, password (hashe), role
│   │   ├── post.py              #   - Post : title, body, tags (many-to-many)
│   │   │                        #   - Tag : nom unique, relation M-N avec Post
│   │   └── file.py              #   - File : filename, taille, type MIME
│   │
│   ├── routes/                  # Blueprints (routes organisees par theme)
│   │   ├── main.py              #   - / (accueil), /about, /hello/<name>
│   │   │                        #   - /setcookie, /getcookie (demo cookies)
│   │   │                        #   - /user/<name> (demo redirections)
│   │   ├── auth.py              #   - /auth/register, /auth/login, /auth/logout
│   │   │                        #   - /auth/profile, /auth/change-password
│   │   ├── dashboard.py         #   - /dashboard/ (tableau de bord)
│   │   │                        #   - /dashboard/posts (CRUD articles)
│   │   │                        #   - /dashboard/upload, /dashboard/files
│   │   │                        #   - /dashboard/settings, /dashboard/admin
│   │   ├── api.py               #   - /api/v1/posts (GET, POST, PUT, DELETE)
│   │   │                        #   - /api/v1/users (GET, admin seulement)
│   │   │                        #   - /api/v1/tags (GET)
│   │   └── errors.py            #   - Pages d'erreur 403, 404, 500
│   │
│   ├── templates/               # Templates Jinja2 (18 fichiers)
│   │   ├── base.html            #   Template de base (navbar, footer, flash)
│   │   ├── components/          #   Composants reutilisables
│   │   │   ├── navbar.html      #     Barre de navigation responsive
│   │   │   ├── footer.html      #     Pied de page
│   │   │   ├── flash_messages.html  # Messages flash avec fermeture auto
│   │   │   └── pagination.html  #     Macro de pagination reutilisable
│   │   ├── main/                #   Pages publiques (index, about, cookie_demo)
│   │   ├── auth/                #   Pages auth (login, register, profile)
│   │   ├── dashboard/           #   Pages dashboard (index, posts, upload, files,
│   │   │                        #     post_form, settings, admin)
│   │   └── errors/              #   Pages d'erreur (403, 404, 500)
│   │
│   ├── static/
│   │   ├── css/style.css        # ~400 lignes de CSS responsive
│   │   ├── js/main.js           # Toggle navbar, auto-dismiss flash
│   │   └── uploads/             # Dossier pour les fichiers uploades
│   │
│   ├── forms/                   # Formulaires Flask-WTF
│   │   ├── auth.py              #   LoginForm, RegisterForm, ProfileForm,
│   │   │                        #   ChangePasswordForm
│   │   ├── upload.py            #   UploadForm (avec validation type fichier)
│   │   └── post.py              #   PostForm (titre, contenu, publie/brouillon)
│   │
│   └── utils/
│       ├── decorators.py        # @admin_required (verifie le role admin)
│       └── helpers.py           # allowed_file(), save_file() (upload securise)
│
├── tests/                       # 29 tests unitaires
│   ├── conftest.py              #   Fixtures pytest (app, db, client, sample_user)
│   ├── test_models.py           #   Tests modeles (User, Post, File)
│   ├── test_auth.py             #   Tests authentification (register, login, logout)
│   └── test_api.py              #   Tests API REST (CRUD, pagination, recherche)
│
├── run.py                       # Point d'entree developpement (python run.py)
├── wsgi.py                      # Point d'entree production (gunicorn wsgi:app)
├── requirements.txt             # Dependances Python
├── .env.example                 # Variables d'environnement (a copier en .env)
├── .gitignore                   # Fichiers ignores par git
├── Dockerfile                   # Image Docker pour la production
└── docker-compose.yml           # Orchestration Docker (1 commande pour tout lancer)
```

---

## Installation

### Prerequis
- Python 3.9 ou superieur
- pip

### Etapes

```bash
# 1. Aller dans le projet
cd projet_flask

# 2. Creer un environnement virtuel
python -m venv .venv

# 3. Activer le venv
source .venv/bin/activate        # Linux / Mac
# .venv\Scripts\activate         # Windows

# 4. Installer les dependances
pip install -r requirements.txt

# 5. Copier le fichier de configuration
cp .env.example .env

# 6. Initialiser la base de donnees
flask --app run:app db init
flask --app run:app db migrate -m "Initial migration"
flask --app run:app db upgrade
```

---

## Lancer l'application

```bash
# Activer le venv (si pas deja fait)
source .venv/bin/activate

# Lancer en mode developpement
python run.py
```

L'application sera accessible sur **http://localhost:5000**

### Premiere utilisation
1. Aller sur http://localhost:5000/auth/register pour creer un compte
2. Se connecter via http://localhost:5000/auth/login
3. Acceder au tableau de bord pour creer des articles et uploader des fichiers

---

## Fonctionnalites detaillees

### Section 1 : Routes et bases Flask
- **Routes avec variables** : `/hello/<name>` accepte un parametre dans l'URL
- **Methodes HTTP** : GET et POST geres sur les formulaires, PUT et DELETE sur l'API
- **Redirections** : `/user/admin` redirige vers le dashboard, `/user/autre` vers `/hello/autre`
- **`url_for()`** : Toutes les URLs sont generees dynamiquement, jamais en dur
- **`abort()`** : Retourne une erreur 403 si un utilisateur non-admin tente d'acceder a `/dashboard/admin`

### Section 2 : Templates Jinja2
- **Heritage** : Toutes les pages heritent de `base.html` via `{% extends 'base.html' %}`
- **Inclusion** : La navbar, le footer et les flash messages sont des composants inclus avec `{% include %}`
- **Macros** : La pagination est une macro reutilisable importee avec `{% from ... import ... %}`
- **Filtres personnalises** :
  - `{{ date|datetime }}` : formate une date en `dd/mm/yyyy HH:MM`
  - `{{ size|filesizeformat }}` : convertit des octets en Ko, Mo, Go
  - `{{ text|truncate_words(30) }}` : coupe un texte apres N mots

### Section 3 : Formulaires
- **Flask-WTF** : Tous les formulaires utilisent des classes Python (LoginForm, RegisterForm, etc.)
- **Validation** : Chaque champ a des validateurs (DataRequired, Email, Length, EqualTo)
- **CSRF** : Protection automatique contre les attaques Cross-Site Request Forgery via `{{ form.hidden_tag() }}`
- **Upload securise** :
  - Validation du type de fichier (png, jpg, pdf, txt, doc, docx)
  - Taille max 16 Mo
  - Renommage avec UUID pour eviter les conflits et injections
- **Messages flash** : Feedback utilisateur apres chaque action (succes, erreur, info)

### Section 4 : Configuration
- **3 environnements** dans `app/config.py` :
  - `DevelopmentConfig` : DEBUG=True, SQLite locale
  - `ProductionConfig` : DEBUG=False, URL de base de donnees via variable d'environnement
  - `TestingConfig` : Base de donnees en memoire, CSRF desactive
- **python-dotenv** : Les secrets sont lus depuis un fichier `.env` (jamais commite)
- **`.env.example`** : Template pour les variables d'environnement

### Section 5 : Base de donnees
- **4 modeles SQLAlchemy** :
  - `User` : id, username, email, password_hash, role, created_at, is_active
  - `Post` : id, title, body, created_at, updated_at, is_published, user_id
  - `Tag` : id, name (relation Many-to-Many avec Post via table `post_tags`)
  - `File` : id, filename, original_filename, file_size, mime_type, user_id
- **Relations** :
  - Un User a plusieurs Posts (One-to-Many)
  - Un User a plusieurs Files (One-to-Many)
  - Un Post a plusieurs Tags et un Tag a plusieurs Posts (Many-to-Many)
- **Migrations** : Flask-Migrate (Alembic) pour versionner le schema de la base
- **CRUD complet** : Create, Read, Update, Delete pour les articles via le dashboard

### Section 6 : Middleware
- **`@app.before_request`** : Log chaque requete entrante et demarre un timer
- **`@app.after_request`** : Log la reponse avec le temps d'execution (ex: `GET /dashboard 200 (0.015s)`)
- **Logging** : Configuration differente selon l'environnement (debug en dev, info en prod)

### Section 7 : Authentification
- **Flask-Login** : Gestion complete des sessions utilisateur
- **Inscription** : Formulaire avec validation (username unique, email valide, mot de passe >= 6 chars)
- **Connexion** : Verification du mot de passe hashe, option "Se souvenir de moi"
- **Deconnexion** : Suppression de la session
- **Hashing** : Les mots de passe sont hashes avec `werkzeug.security` (jamais stockes en clair)
- **Protection des routes** : `@login_required` redirige vers la page de connexion
- **RBAC (Role-Based Access Control)** :
  - Role `user` : acces au dashboard, ses propres articles et fichiers
  - Role `admin` : acces au panneau admin, peut voir tous les utilisateurs
  - Decorateur `@admin_required` pour proteger les routes admin
- **Profil editable** : Modification du username, email et mot de passe

### Section 8 : API REST
- **Endpoints JSON** sous `/api/v1/`
- **CRUD posts** : GET (liste + detail), POST (creer), PUT (modifier), DELETE (supprimer)
- **Pagination** : `?page=1&per_page=10`
- **Recherche** : `?q=flask` cherche dans le titre et le contenu
- **Filtrage par tag** : `?tag=python`
- **Serialisation** : Methode `to_dict()` sur chaque modele
- **Protection** : Les routes d'ecriture necessitent une authentification
- **Reponses d'erreur** : Format JSON coherent `{"error": "message"}`

### Section 9 : Blueprints et architecture
- **5 Blueprints** : `main`, `auth`, `dashboard`, `api`, `errors`
- **Chacun a son prefix URL** : `/auth/...`, `/dashboard/...`, `/api/v1/...`
- **Separation des responsabilites** : Chaque blueprint gere son domaine
- **Pagination** : Macro Jinja2 reutilisable pour paginer les listes

### Section 10 : Erreurs et deploiement
- **Pages d'erreur personnalisees** : 403 (interdit), 404 (non trouve), 500 (erreur serveur)
- **Double format** : HTML pour le navigateur, JSON pour les appels API
- **Dockerfile** : Image Python slim, installation des dependances, Gunicorn
- **docker-compose.yml** : Lance l'app avec les bonnes variables d'environnement et des volumes persistants
- **wsgi.py** : Point d'entree pour Gunicorn en production

---

## API REST

### Endpoints disponibles

| Methode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/api/v1/posts` | Non | Liste des articles publies |
| GET | `/api/v1/posts/<id>` | Non | Detail d'un article |
| POST | `/api/v1/posts` | Oui | Creer un article |
| PUT | `/api/v1/posts/<id>` | Oui | Modifier un article (auteur ou admin) |
| DELETE | `/api/v1/posts/<id>` | Oui | Supprimer un article (auteur ou admin) |
| GET | `/api/v1/tags` | Non | Liste de tous les tags |
| GET | `/api/v1/users` | Admin | Liste des utilisateurs |
| GET | `/api/v1/users/<id>` | Admin | Detail d'un utilisateur |

### Parametres de requete (GET /api/v1/posts)

| Parametre | Type | Defaut | Description |
|-----------|------|--------|-------------|
| `page` | int | 1 | Numero de page |
| `per_page` | int | 10 | Resultats par page (max 50) |
| `q` | string | - | Recherche dans titre et contenu |
| `tag` | string | - | Filtrer par nom de tag |

### Exemple de reponse

```json
{
  "posts": [
    {
      "id": 1,
      "title": "Mon premier article",
      "body": "Contenu de l'article...",
      "author": "testuser",
      "created_at": "2024-01-15T10:30:00",
      "tags": ["python", "flask"],
      "is_published": true
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1,
  "has_next": false,
  "has_prev": false
}
```

---

## Tests

29 tests unitaires couvrant les modeles, l'authentification et l'API.

```bash
# Lancer tous les tests
pytest

# Mode verbose (voir chaque test)
pytest -v

# Un fichier specifique
pytest tests/test_models.py
pytest tests/test_auth.py
pytest tests/test_api.py
```

### Ce qui est teste

| Fichier | Tests | Ce qui est verifie |
|---------|-------|--------------------|
| `test_models.py` | 9 | Creation User/Post/File, hashing password, unicite username, relations, serialisation |
| `test_auth.py` | 8 | Page register, inscription, doublon username, login OK/KO, logout, routes protegees |
| `test_api.py` | 9+3 | GET posts vide/avec data, post unique, 404, creation auth/non-auth, recherche, pagination, tags |

---

## Docker

### Lancer avec Docker Compose

```bash
# Construire et lancer
docker-compose up --build

# Lancer en arriere-plan
docker-compose up -d --build

# Arreter
docker-compose down
```

L'application sera accessible sur **http://localhost:5000**

### Ce que fait Docker ici
- Le **Dockerfile** cree une image avec Python, installe les dependances, et lance Gunicorn
- Le **docker-compose.yml** configure l'app avec les variables d'environnement et des volumes pour persister les donnees (uploads et base de donnees)
- **Pas besoin d'installer Python** sur la machine cible, tout est dans le container

---

## Technologies

| Technologie | Version | Role |
|-------------|---------|------|
| Flask | 3.1.2 | Framework web |
| Flask-SQLAlchemy | 3.1.1 | ORM base de donnees |
| Flask-Migrate | 4.0.5 | Migrations (Alembic) |
| Flask-Login | 0.6.3 | Authentification / sessions |
| Flask-WTF | 1.2.1 | Formulaires + CSRF |
| Flask-RESTful | 0.3.10 | API REST |
| python-dotenv | 1.0.0 | Variables d'environnement |
| Werkzeug | 3.1.5 | Hashing mots de passe, utilitaires |
| SQLite | - | Base de donnees (dev) |
| Gunicorn | 21.2.0 | Serveur WSGI (production) |
| Docker | - | Containerisation |
| pytest | 7.4.3 | Tests unitaires |
