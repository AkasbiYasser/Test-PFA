# Utiliser une image Node.js
FROM node:16-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json et installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le reste du code de l'application
COPY . .

# Construire l'application
RUN npm run build

# Installer un serveur HTTP pour servir l'application
RUN npm install -g serve

# Exposer le port utilisé par l'application
EXPOSE 3000

# Définir la commande pour lancer l'application
CMD ["serve", "-s", "build"]
