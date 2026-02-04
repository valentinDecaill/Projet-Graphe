import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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


plt.figure(figsize=(12, 10)) # Taille de l'image

# On récupère les positions
pos = nx.get_node_attributes(G, 'pos')

# On dessine tout le réseau
nx.draw_networkx_nodes(G, pos, node_size=10, node_color='black')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, alpha=0.5)

plt.title("test metro paris")
plt.axis('equal') 
plt.show()
