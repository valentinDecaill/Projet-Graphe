import streamlit as st
import networkx as nx
from utils import charger_graphe, charger_dessin, dessiner_carte

st.set_page_config(page_title="Le Plus Court Chemin", page_icon="static/images/PCC.webp", layout="wide")

col1, col2 = st.columns([1, 10], vertical_alignment="center")
col1.image("static/images/PCC.webp", width=80)
col2.header("Calcul du Plus Court Chemin")
st.markdown("Calcul de l'itinéraire optimal pour minimiser le temps de transport.")

G = charger_graphe()
df_dessin = charger_dessin()

# MENUS DÉROULANTS (SÉLECTION DES STATIONS)
dict_stations = {data['nom']: noeud for noeud, data in G.nodes(data=True)}
noms_stations_tries = sorted(dict_stations.keys())

col1, col2 = st.columns(2)
with col1:
    depart_nom = st.selectbox("Station de départ", noms_stations_tries)
with col2:
    arrivee_nom = st.selectbox("Station d'arrivée", noms_stations_tries)
    
st.write("---")

# BOUTON DE CALCUL ET AFFICHAGE 
if st.button("Calculer l'itinéraire", type="primary"):
    id_depart = dict_stations[depart_nom]
    id_arrivee = dict_stations[arrivee_nom]
    
    if nx.has_path(G, source=id_depart, target=id_arrivee):
        chemin_ideal = nx.shortest_path(G, source=id_depart, target=id_arrivee, weight='weight')
        temps_estime = nx.shortest_path_length(G, source=id_depart, target=id_arrivee, weight='weight')
        
        st.success(f"✅ Trajet trouvé ! Traversée de {len(chemin_ideal)} stations. (Temps estimé : {temps_estime} temps)")
        
        with st.spinner("Génération de la carte de l'itinéraire..."):
            fig = dessiner_carte(G, df_dessin, chemin=chemin_ideal)
            st.pyplot(fig)
    else:
        st.error("❌ Désolé, aucun chemin ne relie ces deux stations.")
else:
    st.info("Sélectionnez vos stations puis cliquez sur le bouton pour calculer l'itinéraire.")
