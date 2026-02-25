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

# génération de la carte du métro parisien avec les données CSV
@st.cache_resource # pour garder dans la mémoire cache pour éviter de recalculer pour le site web streamlit
def generer_carte():
    G = nx.Graph()

    # Chargement des Noeuds
    
    print("Chargement des Noeuds en cours ...")
    df_stations = pd.read_csv('Stations.csv', sep=';') # On lit et ajoute les données des Noeuds
    for _, row in df_stations.iterrows():
        coords = row['Geo Point'].split(',')
        G.add_node(row['gares_id'], pos=(float(coords[1]), float(coords[0])), nom=row['nom_long'])

    # Chargement des Arêtes
    
    print("Chargement des Arêtes en cours ...")
    df_lignes = pd.read_csv('liaisons.csv', sep=';') # On lit et ajoute les données des Arêtes
    for _, row in df_lignes.iterrows():
        G.add_edge(row['source'], row['target'], weight=row['weight'])

    # Préparation du Dessin
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.get_node_attributes(G, 'pos')

    # Tracé des lignes
    df_dessin = pd.read_csv('Lignes.csv', sep=';')
    for _, row in df_dessin.iterrows():
        shape = json.loads(row['Shape'])
        couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7'
        
        if shape['type'] == 'MultiLineString':
            for segment in shape['coordinates']:
                xs, ys = zip(*segment)
                ax.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)
        elif shape['type'] == 'LineString':
            xs, ys = zip(*shape['coordinates'])
            ax.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)

    # Tracé des stations et fond de carte
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=15, node_color='#2C3E50', alpha=0.8)
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
    
    ax.set_axis_off()
    plt.tight_layout()
    
    return fig

# Affichage sur le site
figure_prete = generer_carte()
st.pyplot(figure_prete)