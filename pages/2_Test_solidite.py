import streamlit as st
import networkx as nx

st.set_page_config(page_title="Test de Solidité", page_icon="🏗️", layout="wide")

st.title("🏗️ Analyse de Robustesse du Réseau")
st.markdown("""
### Tests de solidité (En développement)
Simulation de pannes : suppression des nœuds à forte centralité pour observer l'impact sur la connexité globale du graphe.
""")

st.info("Cette fonctionnalité est en cours de développement. Bientôt, vous pourrez simuler des fermetures de stations et visualiser l'impact sur le réseau.")
