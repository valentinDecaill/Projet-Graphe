# Lancement :  $ streamlit run GrapheMatplotlib.py

import streamlit as st # pour générer un site web interactif

import networkx as nx  
import matplotlib.pyplot as plt

import pandas as pd # pour la lecture des données CSV
import json

import contextily as ctx # pour l'affichage d'une carte en arrière plan

# Configuration de l'interface Web
st.set_page_config(page_title="Projet Graphes", layout="wide")
st.title("Réseau de Transport Parisien")

# ========================================================================= #

@st.cache_resource # On garde en mémoire (cache) pour éviter de tout recalculer pour le site
def charger_graphe(): # fonction pour charger le graphe G avec les donnée des CSV
    
    G = nx.Graph()
    
    # Chargement des Stations (Noeuds)
    df_stations = pd.read_csv('Stations.csv', sep=';')
    for _, row in df_stations.iterrows():
        coords = row['Geo Point'].split(',')
        id_station = str(row['gares_id']) 
        G.add_node(id_station, pos=(float(coords[1]), float(coords[0])), nom=row['nom_long'])
        
    # Chargement des Lignes (Arêtes)
    df_lignes = pd.read_csv('liaisons.csv', sep=';')
    for _, row in df_lignes.iterrows():
        id_source = str(row['source'])
        id_target = str(row['target'])
        G.add_edge(id_source, id_target, weight=row['weight'])
        
    return G # on returne le graphe finit et charger

# ========================================================================= #

# On met en cache la lecture du CSV pour le dessin
@st.cache_data
def charger_dessin():
    return pd.read_csv('Lignes.csv', sep=';')

# ========================================================================= #


# appel des fonctions
G = charger_graphe()
df_dessin = charger_dessin()

# ========================================================================= #

# MENUS DÉROULANTS (SÉLECTION DES STATIONS)
# On crée un dictionnaire { "Nom de la station" : "ID de la station" }
dict_stations = {data['nom']: noeud for noeud, data in G.nodes(data=True)}
# On trie les noms de stations par ordre alphabétique pour le menu déroulant
noms_stations_tries = sorted(dict_stations.keys())

# Affichage des menus sur deux colonnes
col1, col2 = st.columns(2)
with col1:
    depart_nom = st.selectbox("📍 Station de départ", noms_stations_tries)
with col2:
    arrivee_nom = st.selectbox("🏁 Station d'arrivée", noms_stations_tries)
    
# ========================================================================= #

# Fonction qui dessine le chemin trouver en rouge
def dessiner_carte(chemin=None):
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.get_node_attributes(G, 'pos')

    # Tracé des lignes géographiques (en fond)
    for _, row in df_dessin.iterrows():
        shape = json.loads(row['Shape'])
        couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7'
        
        # Si un chemin est affiché, on rend le reste du réseau un peu plus transparent pour la visibilité
        alpha_val = 0.2 if chemin else 0.5 
        
        if shape['type'] == 'MultiLineString':
            for segment in shape['coordinates']:
                xs, ys = zip(*segment)
                ax.plot(xs, ys, color=couleur, linewidth=2, alpha=alpha_val)
        elif shape['type'] == 'LineString':
            xs, ys = zip(*shape['coordinates'])
            ax.plot(xs, ys, color=couleur, linewidth=2, alpha=alpha_val)

    # Tracé de toutes les stations
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=10, node_color='#2C3E50', alpha=0.3)

    # TRACÉ DU PLUS COURT CHEMIN
    if chemin:
        # On découpe le chemin en paires 
        chemin_edges = list(zip(chemin[:-1], chemin[1:]))
        
        # On dessine le trait rouge (les arêtes du chemin trouver)
        nx.draw_networkx_edges(G, pos, edgelist=chemin_edges, ax=ax, edge_color='red', width=4)
        
        # On dessine les gros points rouges (les stations traversées)
        nx.draw_networkx_nodes(G, pos, nodelist=chemin, ax=ax, node_size=40, node_color='red')

    # Ajout du fond de carte OpenStreetMap
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    plt.tight_layout()
    
    return fig 

# ========================================================================= #


# BOUTON DE CALCUL ET AFFICHAGE 
# Quand on clique sur le bouton :
if st.button("Calculer le plus court chemin"):
    # On retrouve l'ID des stations choisies
    id_depart = dict_stations[depart_nom]
    id_arrivee = dict_stations[arrivee_nom]
    
    # On vérifie logiquement si les deux stations sont bien connectées et on calcul
    if nx.has_path(G, source=id_depart, target=id_arrivee):
        
        chemin_ideal = nx.shortest_path(G, source=id_depart, target=id_arrivee, weight='weight')
        
        st.success(f"Trajet trouvé ! Il passe par {len(chemin_ideal)} stations.")
        
        with st.spinner("Génération de la carte avec l'itinéraire..."):
            fig = dessiner_carte(chemin=chemin_ideal)
            st.pyplot(fig)
            
    else:
        # Si has_path() renvoie False (stations pas relier)
        st.error("Désolé, aucun chemin ne relie ces deux stations.")
        
else:
    # Affichage normal
    with st.spinner("Chargement de la carte complète..."):
        fig = dessiner_carte()
        st.pyplot(fig)