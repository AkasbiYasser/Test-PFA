# Utiliser l'image MySQL officielle comme base
FROM mysql:8.0

# Ajouter le script d'initialisation dans le répertoire approprié
COPY backup1.sql /docker-entrypoint-initdb.d/

# Définir les variables d'environnement nécessaires
ENV MYSQL_ROOT_PASSWORD=yasser1234
ENV MYSQL_DATABASE=templates
