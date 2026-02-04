import networkx as nx
import matplotlib.pyplot as plt

# Lecture de fichiers csv
import json
import pandas as pd

# La bibliothèque pour la carte
import contextily as ctx 


G = nx.Graph() #on crée le graph G vide pour l'instant


# ===================================================================================== #
#           Chargement des noeuds (Stations) à partir du fichier exel (.csv)            #
# ===================================================================================== #


print("Chargement des stations...")
def_stations = pd.read_csv('Sations.csv', sep=';')  # on lit le fichier avec pandas en séparant par ';'


for index, row in def_stations.iterrows():   # On parcourt chaque ligne du fichier Excel pour ajouter les noeuds
    
    coordonnees = row['Geo Point'].split(',') # Coupe à la virgule pour obtenir des coordonnées utilisable pour le noeuds
    lat = float(coordonnees[0]) # Y
    lon = float(coordonnees[1]) # X

    G.add_node(row['gares_id'], pos=(lon, lat), nom=row['nom_long']) # On ajoute le nœud au graphe
    
    

# ===================================================================================== #
#                           Chargement des Aretes (Lignes)                              #
# ===================================================================================== #

# calcule du poids = sqrt((x2 - x1)**2 + (y2 - y1)**2)   / 100   On Calcul de la distance entre deux points (x1, y1) et (x2, y2)

print("Chargement des Lignes...")
def_lignes = pd.read_csv('liaisons.csv', sep=';') # on lit le fichier avec pandas en séparant par ';'

for index, row in def_lignes.iterrows():                    # On parcourt chaque ligne du fichier Excel pour ajouter les aretes
    G.add_edge(row['source'], row['target'], weight=row['weight'])



# ===================================================================================== #
#                                     Affichage                                         #
# ===================================================================================== #


# --- CRÉATION DE LA TOILE ---
fig, ax = plt.subplots(figsize=(15, 12)) 
pos = nx.get_node_attributes(G, 'pos') 


# --- STYLES DES LIGNES ---
df_dessin = pd.read_csv('Lignes.csv', sep=';') 

for index, row in df_dessin.iterrows():
    shape = json.loads(row['Shape'])
    
    couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7'
    
    if shape['type'] == 'MultiLineString':
        for segment in shape['coordinates']:
            xs, ys = zip(*segment)
            ax.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)

    elif shape['type'] == 'LineString':
        xs, ys = zip(*shape['coordinates'])
        ax.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)


# --- STYLES DES STATIONS ---
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=15, node_color='#2C3E50', alpha=0.8)


# --- AJOUT d'une VRAIE CARTE EN ARRIÈRE-PLAN ---
ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)


# --- FINITION ET AFFICHAGE ---
ax.set_title("Réseau Complet du Transport Parisien (Métro & RER)", fontsize=18, fontweight='bold', pad=20)
ax.set_axis_off() # Cache les coordonnées
plt.axis('equal') 
plt.tight_layout()
plt.show()
