# 📝SnakeNote (To‑DoList)

Une application web légère permettant de gérer vos tâches par collections, avec changement de thème à la volée (classique, techno, médiéval, coquette, lac).

## Badges

[![Django](https://img.shields.io/badge/Django-4.2-blue.svg)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-3.11-yellow.svg)](https://www.python.org/) 

## Features

* 🎨Changement de thème 
* 🗂Organisation des tâches par collection
* ➕Ajout / ❌suppression de tâches et collections
* 🔔Messages flash pour le feedback utilisateur

## Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/djelines/SnakeNote.git
cd SnakeNote

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  
# sous Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate
```

## Deployment

```bash
# Lancer le serveur de développement
python manage.py runserver

# Accéder à l’application
# http://127.0.0.1:8000/  
```
