# Utilisez l'image de base spécifique
FROM iridl/simagridssat:latest

# Installer les dépendances nécessaires
#RUN apt-get update && apt-get install -y zlib1g zlib1g-dev
RUN apt-get update && apt-get install -y zlib1g zlib1g-dev python3-pip
# Installer le module folium
RUN pip3 install branca==0.5.0
RUN pip3 install folium==0.12.1.post1
RUN pip3 install dash_leaflet

# Copier les fichiers de l'application dans le conteneur
COPY ./*.py /home/SIMAGRI/
COPY ./apps/ /home/SIMAGRI/apps/
COPY ./assets/ /home/SIMAGRI/assets/
COPY ./data/ /home/SIMAGRI/data/
COPY ./shared/ /home/SIMAGRI/shared/
COPY ./TEST_SN/* DSSAT/dssat-base-files/

# Définir le répertoire de travail
WORKDIR /home/SIMAGRI/

# Commande pour exécuter l'application
CMD ["python3", "index.py", "senegal"]
