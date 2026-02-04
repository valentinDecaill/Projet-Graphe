import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
import contextily as ctx

# Configuration de la page
st.set_page_config(page_title="Métro Paris - Itinéraire", layout="wide")
st.title("🚇 Calculateur d'Itinéraire Parisien")

# ===================================================================================== #
#                   Chargement des Données (Mis en cache)                               #
# ===================================================================================== #

@st.cache_data
def charger_donnees():
    # On charge les 3 fichiers
    stations = pd.read_csv('Sations.csv', sep=';')
    lignes = pd.read_csv('Lignes.csv', sep=';')
    liaisons = pd.read_csv('liaisons.csv', sep=';')
    return stations, lignes, liaisons

try:
    df_stations, df_lignes, df_liaisons = charger_donnees()
except FileNotFoundError:
    st.error("Erreur : Fichiers CSV introuvables.")
    st.stop()


# ===================================================================================== #
#                           Création du Graphe (Logique Métier)                         #
# ===================================================================================== #

G = nx.Graph()

# 1. Ajout des Noeuds
for index, row in df_stations.iterrows():
    if pd.isna(row['Geo Point']): continue
    coords = row['Geo Point'].split(',')
    # Attention: Geo Point est souvent "Lat, Lon", on inverse pour (Lon, Lat) = (X, Y)
    lat, lon = float(coords[0]), float(coords[1])
    
    # On stocke le nom pour l'afficher plus tard
    G.add_node(row['gares_id'], pos=(lon, lat), nom=row['nom_long'])

# 2. Ajout des Arêtes
for index, row in df_liaisons.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])


# ===================================================================================== #
#                           Barre Latérale (Contrôles)                                  #
# ===================================================================================== #

st.sidebar.header("📍 Sélection du Trajet")

# --- 1. SÉLECTION DE DÉPART ---
# Dictionnaire {Nom de la station : ID de la station}
dict_nom_vers_id = {row['nom_long']: row['gares_id'] for i, row in df_stations.iterrows()}
# Dictionnaire inverse {ID : Nom} pour l'affichage
dict_id_vers_nom = {row['gares_id']: row['nom_long'] for i, row in df_stations.iterrows()}

liste_stations_toutes = sorted(dict_nom_vers_id.keys())

depart_nom = st.sidebar.selectbox("Départ", liste_stations_toutes)
id_depart = dict_nom_vers_id[depart_nom]


# --- 2. FILTRAGE DYNAMIQUE (Ta demande : "seul ceux relier") ---
# On regarde quelles stations sont accessibles depuis le départ (Composante Connexe)
try:
    # Récupère tous les noeuds connectés au départ
    ids_accessibles = nx.node_connected_component(G, id_depart)
    # On convertit ces IDs en noms pour la liste déroulante
    noms_accessibles = sorted([dict_id_vers_nom[i] for i in ids_accessibles if i in dict_id_vers_nom])
except:
    # Si le noeud est isolé ou bugué
    noms_accessibles = []

# --- 3. SÉLECTION D'ARRIVÉE ---
arrivee_nom = st.sidebar.selectbox("Arrivée", noms_accessibles)
id_arrivee = dict_nom_vers_id[arrivee_nom] if arrivee_nom else None


st.sidebar.markdown("---")
st.sidebar.header("👀 Options de Vue")

# Options demandées
voir_lignes = st.sidebar.checkbox("Afficher toutes les lignes métro", value=True)
zoom_sur_trajet = st.sidebar.checkbox("Zoomer sur le trajet (sinon voir tout Paris)", value=False)


# ===================================================================================== #
#                           Calculs et Statistiques                                     #
# ===================================================================================== #

chemin_trouve = []
distance_totale = 0

if id_arrivee and id_depart != id_arrivee:
    try:
        # Calcul du chemin le plus court (Dijkstra)
        chemin_trouve = nx.shortest_path(G, source=id_depart, target=id_arrivee, weight='weight')
        
        # Calcul du coût total (somme des poids)
        distance_totale = nx.shortest_path_length(G, source=id_depart, target=id_arrivee, weight='weight')
        
        # --- AFFICHAGE DES INFOS (Ta demande : "afficher des information") ---
        st.success(f"Itinéraire trouvé : {depart_nom} ➔ {arrivee_nom}")
        
        col1, col2 = st.columns(2)
        col1.metric("Nombre de stations", f"{len(chemin_trouve)} arrets")
        # Le poids ici est une estimation (distance/temps selon ton fichier liaisons.py)
        col2.metric("Coût du trajet (Poids)", f"{int(distance_totale)} unités")
        
    except nx.NetworkXNoPath:
        st.error("Aucun chemin possible entre ces deux stations.")


# ===================================================================================== #
#                                     Affichage (Matplotlib)                            #
# ===================================================================================== #

# CRÉATION DE LA TOILE
fig, ax = plt.subplots(figsize=(14, 10))
pos = nx.get_node_attributes(G, 'pos')


# --- COUCHE 1 : DESSIN DES LIGNES (SI DEMANDÉ) ---
if voir_lignes:
    for index, row in df_lignes.iterrows():
        if pd.isna(row['Shape']): continue
        shape = json.loads(row['Shape'])
        couleur = '#' + str(row['Color']) if pd.notna(row['Color']) else '#BDC3C7'
        
        if shape['type'] == 'MultiLineString':
            for segment in shape['coordinates']:
                xs, ys = zip(*segment)
                # Opacité fixe (pas de paramètre)
                ax.plot(xs, ys, color=couleur, linewidth=1.5, alpha=0.5)

        elif shape['type'] == 'LineString':
            xs, ys = zip(*shape['coordinates'])
            ax.plot(xs, ys, color=couleur, linewidth=1.5, alpha=0.5)


# --- COUCHE 2 : LE TRAJET (SI EXISTANT) ---
if chemin_trouve:
    # On dessine le trait du chemin (Gros trait rouge)
    aretes_chemin = list(zip(chemin_trouve, chemin_trouve[1:]))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=aretes_chemin, edge_color='#E74C3C', width=5)
    
    # On dessine les points du chemin
    # Départ = Vert, Arrivée = Rouge, Milieu = Jaune
    couleurs_noeuds = []
    tailles_noeuds = []
    
    for node in chemin_trouve:
        if node == id_depart: 
            couleurs_noeuds.append('#2ECC71') # Vert
            tailles_noeuds.append(150)
        elif node == id_arrivee: 
            couleurs_noeuds.append('#E74C3C') # Rouge
            tailles_noeuds.append(150)
        else: 
            couleurs_noeuds.append('#F1C40F') # Jaune
            tailles_noeuds.append(60)
            
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=chemin_trouve, node_color=couleurs_noeuds, node_size=tailles_noeuds, edgecolors='black')


# --- COUCHE 3 : LES STATIONS (SI PAS DE TRAJET OU OPTION) ---
if not chemin_trouve:
    # Si pas de trajet, on montre tout en bleu nuit simple
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=15, node_color='#2C3E50', alpha=0.8)


# --- GESTION DU ZOOM (Ta demande : "afficher toujours paris... et zoomer si besoin") ---
if chemin_trouve and zoom_sur_trajet:
    # On récupère les coordonnées des stations du chemin
    xs = [pos[n][0] for n in chemin_trouve]
    ys = [pos[n][1] for n in chemin_trouve]
    
    # On ajoute une petite marge (padding)
    marge = 0.01 
    ax.set_xlim(min(xs) - marge, max(xs) + marge)
    ax.set_ylim(min(ys) - marge, max(ys) + marge)
else:
    # Par défaut, Matplotlib cadre sur toutes les données (Tout Paris)
    pass 


# --- AJOUT DU FOND DE CARTE ---
try:
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.CartoDB.Positron)
except:
    pass

# Finitions
ax.set_axis_off()
plt.tight_layout()

# Affichage dans Streamlit
st.pyplot(fig)