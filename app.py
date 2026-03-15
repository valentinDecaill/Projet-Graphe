import streamlit as st
from utils import charger_graphe, charger_dessin, dessiner_carte

# lancer avec la commande : streamlit run app.py

st.set_page_config(page_title="Réseau de Transport Parisien", layout="wide", page_icon="static/images/Logo.webp")

col1, col2 = st.columns([1, 10], vertical_alignment="center")
col1.image("static/images/Logo.webp", width=80)
col2.title("Réseau de Transport Parisien")

st.logo("static/images/Metro.webp", size="large")

# Configuration de la navigation Streamlit
pages = {
    "Projet": [
        st.Page("pages/home.py", title="Accueil", default=True),
        st.Page("pages/1_Plus_court_chemin.py", title="Plus court chemin"),
        st.Page("pages/2_Test_poids.py", title="Analyse du poids des nœuds (stations)"),
        st.Page("pages/3_Test_solidite.py", title="Analyse de Robustesse")
    ]
}

# Importation et application de styles CSS
from static.css import load_css
load_css()


pg = st.navigation(pages)
pg.run()
