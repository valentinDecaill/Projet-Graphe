import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd
from utils import charger_graphe

st.title("Analyse de l'importance des stations")

st.write("Cette page permet d'identifier les stations les plus importantes du reseau, que ce soit par leur position de carrefour ou par leur nombre de correspondances.")

G = charger_graphe()
pos = nx.get_node_attributes(G, 'pos')

st.header("1. Stations les plus centrales (Carrefours)")
st.write("Ce score estime la frequantation. Plus une station est un passage oblige entre d'autres stations, plus son score est eleve.")

bc = nx.betweenness_centrality(G, weight='weight')
top_bc = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:10]

donnees_bc = []
for noeud, score in top_bc:
    nom_station = G.nodes[noeud].get('nom', str(noeud))
    donnees_bc.append({"Station": nom_station, "Score": round(score, 4)})

st.table(pd.DataFrame(donnees_bc))

st.write("Carte des carrefours strategiques")
fig_bc, ax_bc = plt.subplots(figsize=(14, 12))
nx.draw_networkx_edges(G, pos, ax=ax_bc, alpha=0.1, edge_color='gray')

tailles_bc = [bc[noeud] * 15000 + 30 for noeud in G.nodes()]
nx.draw_networkx_nodes(G, pos, ax=ax_bc, node_size=tailles_bc, node_color='blue', alpha=0.6)

for noeud, score in top_bc:
    x, y = pos[noeud]
    nom_station = G.nodes[noeud].get('nom', str(noeud))
    ax_bc.text(x, y, nom_station, fontsize=10, fontweight='bold', color='black', ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

ctx.add_basemap(ax_bc, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
ax_bc.set_axis_off()
st.pyplot(fig_bc)

st.header("2. Stations avec le plus de correspondances")
st.write("Ces stations possedent le plus grand nombre de lignes ou de voisins directs.")

degrees = dict(G.degree())
top_degree = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]

donnees_deg = []
for noeud, score in top_degree:
    nom_station = G.nodes[noeud].get('nom', str(noeud))
    donnees_deg.append({"Station": nom_station, "Correspondances": score})

st.table(pd.DataFrame(donnees_deg))

st.write("Carte des correspondances")
fig_deg, ax_deg = plt.subplots(figsize=(14, 12))
nx.draw_networkx_edges(G, pos, ax=ax_deg, alpha=0.1, edge_color='gray')

tailles_deg = [degrees[noeud] * 150 + 30 for noeud in G.nodes()]
nx.draw_networkx_nodes(G, pos, ax=ax_deg, node_size=tailles_deg, node_color='red', alpha=0.6)

for noeud, score in top_degree:
    x, y = pos[noeud]
    nom_station = G.nodes[noeud].get('nom', str(noeud))
    ax_deg.text(x, y, nom_station, fontsize=10, fontweight='bold', color='black', ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

ctx.add_basemap(ax_deg, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
ax_deg.set_axis_off()
st.pyplot(fig_deg)
