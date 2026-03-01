import networkx as nx  
import matplotlib.pyplot as plt
import pandas as pd 
import json
import contextily as ctx
import streamlit as st

@st.cache_resource
def charger_graphe():
    G = nx.Graph()
    
    df_stations = pd.read_csv('Stations.csv', sep=';')
    for _, row in df_stations.iterrows():
        coords = row['Geo Point'].split(',')
        id_station = str(row['gares_id']) 
        G.add_node(id_station, pos=(float(coords[1]), float(coords[0])), nom=row['nom_long'])
        
    df_lignes = pd.read_csv('liaisons.csv', sep=';')
    for _, row in df_lignes.iterrows():
        id_source = str(row['source'])
        id_target = str(row['target'])
        G.add_edge(id_source, id_target, weight=row['weight'])
        
    stations_par_nom = {}
    for noeud, data in G.nodes(data=True):
        nom = data['nom']
        if pd.notna(nom):
            if nom not in stations_par_nom:
                stations_par_nom[nom] = []
            stations_par_nom[nom].append(noeud)
            
    for nom, noeuds in stations_par_nom.items():
        if len(noeuds) > 1:
            for i in range(len(noeuds)):
                for j in range(i+1, len(noeuds)):
                    G.add_edge(noeuds[i], noeuds[j], weight=3)
                    
    return G

@st.cache_data
def charger_dessin():
    return pd.read_csv('Lignes.csv', sep=';')

def dessiner_carte(G, df_dessin, chemin=None):
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = nx.get_node_attributes(G, 'pos')

    for _, row in df_dessin.iterrows():
        shape = json.loads(row['Shape'])
        couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7'
        
        alpha_val = 0.2 if chemin else 0.5 
        
        if shape['type'] == 'MultiLineString':
            for segment in shape['coordinates']:
                xs, ys = zip(*segment)
                ax.plot(xs, ys, color=couleur, linewidth=2, alpha=alpha_val)
        elif shape['type'] == 'LineString':
            xs, ys = zip(*shape['coordinates'])
            ax.plot(xs, ys, color=couleur, linewidth=2, alpha=alpha_val)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=10, node_color='#2C3E50', alpha=0.3)

    if chemin:
        chemin_edges = list(zip(chemin[:-1], chemin[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=chemin_edges, ax=ax, edge_color='red', width=4)
        nx.draw_networkx_nodes(G, pos, nodelist=chemin, ax=ax, node_size=40, node_color='red')

    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    plt.tight_layout()
    
    return fig
