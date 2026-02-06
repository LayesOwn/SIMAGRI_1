# SIMAGRI Sénégal - Dockerfile
# Version simplifiée pour le Sénégal uniquement

# Image de base avec DSSAT compilé
FROM iridl/simagridssat:latest

# Définir l'encodage UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    zlib1g \
    zlib1g-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python pour les cartes
RUN pip3 install --no-cache-dir \
    branca==0.5.0 \
    folium==0.12.1.post1 \
    dash_leaflet

# Copier les fichiers de l'application
COPY ./*.py /home/SIMAGRI/
COPY ./apps/ /home/SIMAGRI/apps/
COPY ./assets/ /home/SIMAGRI/assets/
COPY ./data/ /home/SIMAGRI/data/
COPY ./shared/ /home/SIMAGRI/shared/
COPY ./TEST_SN/* /home/SIMAGRI/DSSAT/dssat-base-files/

# Définir le répertoire de travail
WORKDIR /home/SIMAGRI/

# Exposer le port
EXPOSE 5000

# Commande de démarrage (plus besoin de l'argument "senegal")
CMD ["python3", "index.py"]
