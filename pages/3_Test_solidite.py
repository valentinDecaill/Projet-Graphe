import streamlit as st
import networkx as nx
import random
import matplotlib.pyplot as plt
import contextily as ctx
from utils import charger_graphe

st.title("Analyse de robustesse")

if 'removed_nodes' not in st.session_state:
    st.session_state.removed_nodes = []

G = charger_graphe()
pos = nx.get_node_attributes(G, 'pos')

col1, col2 = st.columns(2)
with col1:
    if st.button("Lancer la simulation"):
        st.session_state.removed_nodes = random.sample(list(G.nodes()), 5)

with col2:
    if st.button("Remettre les stations"):
        st.session_state.removed_nodes = []

if st.session_state.removed_nodes:
    G_copy = G.copy()
    G_copy.remove_nodes_from(st.session_state.removed_nodes)
    
    st.write("Stations supprimees :")
    for node in st.session_state.removed_nodes:
        nom_station = G.nodes[node].get('nom', node)
        st.write(nom_station)
        
    nb_components = nx.number_connected_components(G_copy)
    st.write("Nombre de composantes connexes :", nb_components)
    
    if nb_components == 1:
        st.write("Le reseau est toujours entier.")
    else:
        st.write("Le reseau a ete fracture en plusieurs morceaux.")
        
    st.write("Carte du reseau apres suppression")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    nx.draw_networkx_edges(G_copy, pos, ax=ax, alpha=0.2)
    nx.draw_networkx_nodes(G_copy, pos, ax=ax, node_size=10, node_color='blue', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=st.session_state.removed_nodes, ax=ax, node_size=100, node_color='red', alpha=0.9)
    
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    st.pyplot(fig)
else:
    st.write("Aucune station supprimee.")
