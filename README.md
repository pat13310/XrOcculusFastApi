# 🚀 XrOcculus FastAPI Backend

Bienvenue sur le backend de l'API XrOcculus, développé avec FastAPI. Ce projet fournit des fonctionnalités pour gérer les utilisateurs, les groupes et les sessions.

## 📋 Table des matières

- [🚀 XrOcculus FastAPI Backend](#-xrocculus-fastapi-backend)
  - [📋 Table des matières](#-table-des-matières)
  - [📦 Installation](#-installation)
  - [⚙️ Configuration](#️-configuration)
  - [🛠️ Utilisation](#️-utilisation)
  - [📚 Routes](#-routes)
    - [🔐 Authentification](#-authentification)
    - [👥 Utilisateurs](#-utilisateurs)
    - [👥 Groupes](#-groupes)
    - [📅 Sessions](#-sessions)
  - [📝 Modèles de données](#-modèles-de-données)
  - [📄 Licence](#-licence)

## 📦 Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/xrocculus-backend.git
   cd xrocculus-backend
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows, utilisez `.venv\Scripts\activate`
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez la base de données :
   ```bash
   alembic upgrade head
   ```

## ⚙️ Configuration

Assurez-vous de configurer les variables d'environnement nécessaires dans un fichier `.env` ou directement dans votre environnement. Voici un exemple de configuration :

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🛠️ Utilisation

Pour démarrer le serveur FastAPI, exécutez la commande suivante :

```bash
uvicorn main:app --reload
```

Le serveur sera disponible à l'adresse `http://127.0.0.1:8000`.

## 📚 Routes

### 🔐 Authentification

- **POST** `/login` : Authentifie un utilisateur et retourne un token d'accès.

### 👥 Utilisateurs

- **GET** `/users` : Liste tous les utilisateurs.
- **POST** `/users` : Crée un nouvel utilisateur.
- **GET** `/users/{user_id}` : Récupère les détails d'un utilisateur par ID.
- **PUT** `/users/{user_id}` : Met à jour les informations d'un utilisateur.
- **DELETE** `/users/{user_id}` : Supprime un utilisateur par ID.

### 👥 Groupes

- **GET** `/groups` : Liste tous les groupes.
- **POST** `/groups` : Crée un nouveau groupe.
- **GET** `/groups/{group_id}` : Récupère les détails d'un groupe par ID.
- **PUT** `/groups/{group_id}` : Met à jour les informations d'un groupe.
- **DELETE** `/groups/{group_id}` : Supprime un groupe par ID.

### 📅 Sessions

- **GET** `/sessions` : Liste toutes les sessions.
- **POST** `/sessions` : Crée une nouvelle session.
- **DELETE** `/sessions/delete/{session_id}` : Supprime une session par ID.
- **GET** `/sessions/stop/{session_id}` : Arrête une session par ID.
- **POST** `/sessions/{session_id}/add_user/{user_id}` : Associe un utilisateur à une session.

## 📝 Modèles de données

### Utilisateur (User)

- `id` : Identifiant unique de l'utilisateur.
- `email` : Adresse email de l'utilisateur.
- `username` : Nom d'utilisateur.
- `full_name` : Nom complet de l'utilisateur.
- `hashed_password` : Mot de passe haché.
- `disabled` : Indique si l'utilisateur est désactivé.
- `role` : Rôle de l'utilisateur (par défaut "user").
- `group` : Identifiant du groupe auquel l'utilisateur appartient.
- `created_at` : Date de création de l'utilisateur.
- `updated_at` : Date de dernière mise à jour de l'utilisateur.
- `deleted_at` : Date de suppression de l'utilisateur (nullable).
- `last_login` : Date de dernière connexion de l'utilisateur (nullable).

### Session

- `id` : Identifiant unique de la session.
- `name` : Nom de la session.
- `created_at` : Date de création de la session.
- `ended_at` : Date de fin de la session (nullable).
- `state` : État de la session (par défaut "inactive").
- `users` : Liste des utilisateurs associés à la session.

### Groupe (Group)

- `id` : Identifiant unique du groupe.
- `name` : Nom du groupe.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.