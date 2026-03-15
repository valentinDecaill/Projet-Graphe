import streamlit as st
import networkx as nx
from utils import charger_graphe

st.title("Statistiques du reseau")

G = charger_graphe()

st.metric("Stations", G.number_of_nodes())
st.metric("Liaisons", G.number_of_edges())

if nx.is_connected(G):
    st.write("Le reseau est totalement connecte.")
else:
    st.write("Le reseau n'est pas totalement connecte.")
