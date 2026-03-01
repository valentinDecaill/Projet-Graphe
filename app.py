import streamlit as st
from utils import charger_graphe, charger_dessin, dessiner_carte

# lancer avec la commande : streamlit run app.py

st.set_page_config(page_title="Réseau de Transport Parisien", layout="wide", page_icon="🚇")

st.logo("🚇", size="large")

# Configuration de la navigation Streamlit
pages = {
    "Projet": [
        st.Page("pages/home.py", title="Accueil", icon="🏠", default=True),
        st.Page("pages/1_Plus_court_chemin.py", title="Plus court chemin", icon="📍"),
        st.Page("pages/2_Test_solidite.py", title="Analyse de Robustesse", icon="🏗️")
    ]
}

# Importation et application de styles CSS
from static.css import load_css
load_css()


pg = st.navigation(pages)
pg.run()
