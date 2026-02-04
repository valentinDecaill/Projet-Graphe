import networkx as nx
import matplotlib.pyplot as plt

# Lecture de fichiers csv
import json
import pandas as pd


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
#                                   Affichage                                           #
# ===================================================================================== #

plt.figure(figsize=(15, 12)) # Taille de l'image de la carte
pos = nx.get_node_attributes(G, 'pos') # on ajoutes les position calculées au graphe G


# --- STYLES DES LIGNES ---
def_lignes = pd.read_csv('Lignes.csv', sep=';') # On utilise Lignes.csv pour dessiner les courbes colorées du métro

for index, row in def_lignes.iterrows():
    shape = json.loads(row['Shape'])
    
    couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7' # On récupère la couleur dans le tableau
    
    if shape['type'] == 'MultiLineString': # On a plusieurs morceaux de ligne, donc on boucle sur chaque morceau pour les afficher
        for segment in shape['coordinates']:
            # On sépare les Longitudes et Latitudes du segment actuel
            xs, ys = zip(*segment)
            # On dessine le segment
            plt.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)

    elif shape['type'] == 'LineString':
        # On n'a qu'un seul morceau continu
        # On sépare directement les Longitudes et Latitudes
        xs, ys = zip(*shape['coordinates'])
        # On dessine la ligne
        plt.plot(xs, ys, color=couleur, linewidth=2, alpha=0.5)


# --- STYLES DES STATIONS ---
nx.draw_networkx_nodes(G, pos, node_size=15, node_color='#2C3E50', alpha=0.8) # On dessine les stations en petits points noirs par-dessus les lignes


# --- FINITION ET AFFICHAGE---
plt.title("Réseau Complet dU Transport Parisien (Métro & RER)", fontsize=18, fontweight='bold', pad=20)
plt.axis('equal') # Pour garder les bonnes proportions de la carte de Paris
plt.axis('off') 
plt.tight_layout()
plt.show()
