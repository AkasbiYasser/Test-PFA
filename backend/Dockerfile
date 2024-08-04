# Utiliser une image Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port utilisé par Flask
EXPOSE 5000

# Définir la commande pour lancer l'application
CMD ["python", "app.py"]
