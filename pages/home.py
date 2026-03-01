import streamlit as st
from utils import charger_graphe, charger_dessin, dessiner_carte

st.title("🚇 Réseau de Transport Parisien")
st.header("Analyse de Réseau de Transport")
st.markdown("""
Bienvenue sur l'application du **Projet Graphes**. Utilisez la barre de navigation à gauche pour explorer les différentes fonctionnalités du projet.

Ce projet a pour but de modéliser, visualiser et analyser le réseau de métro parisien en utilisant la **théorie des graphes** et **Python**.

L'objectif est de transformer des données géographiques (stations) et structurelles (lignes) en un objet mathématique (Graphe) afin d'appliquer des algorithmes classiques pour résoudre des problèmes de transport (plus court chemin, identification des hubs critiques, robustesse du réseau ...).

### 📖 Concepts Théoriques
Le projet repose sur la modélisation mathématique suivante : **$G = (V, E, W)$**
* **Nœuds ($V$) :** Les stations de métro. Chaque nœud possède des attributs spatiaux $(x, y)$.
* **Arêtes ($E$) :** Les sections de tunnel reliant deux stations adjacentes, et les connexions piétonnes au sein des grandes stations.
* **Pondération ($W$) :** Le temps de trajet entre les stations en minutes.
""")

G = charger_graphe()
df_dessin = charger_dessin()

with st.spinner("Chargement de la carte complète du réseau..."):
    fig = dessiner_carte(G, df_dessin)
    st.pyplot(fig)
