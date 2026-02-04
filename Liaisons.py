

# Code par ia pour générer les liaisons entre les noeuds et aretes des fichiers


import pandas as pd
import numpy as np

def generer_liaisons_automatiques():
    print("🔄 Génération du fichier liaisons.csv en cours...")
    
    # 1. Chargement des stations
    try:
        df = pd.read_csv('Sations.csv', sep=';')
    except FileNotFoundError:
        print("❌ Erreur : Fichier 'Sations.csv' manquant.")
        return

    # On nettoie un peu : on ne garde que le Métro et RER pour simplifier
    # On filtre les colonnes utiles : ID, Nom, Ligne, X, Y
    df = df[df['mode'].isin(['METRO', 'RER'])].copy()
    
    # On supprime les doublons (certaines stations apparaissent plusieurs fois)
    df = df.drop_duplicates(subset=['nom_long', 'res_com'])

    liaisons = []

    # 2. Algorithme de tri et de connexion
    # Pour chaque ligne (ex: METRO 1, RER A...), on essaie de relier les stations
    lignes_uniques = df['res_com'].unique()

    for ligne_nom in lignes_uniques:
        if pd.isna(ligne_nom): continue
        
        # On récupère toutes les stations de cette ligne
        stations_ligne = df[df['res_com'] == ligne_nom].copy()
        
        if len(stations_ligne) < 2:
            continue

        # ASTUCE : Comment trier les stations dans l'ordre sans connaître le trajet ?
        # On regarde si la ligne est plutôt horizontale (Est-Ouest) ou verticale (Nord-Sud)
        # en comparant l'écart-type (std) des coordonnées X et Y.
        ecart_x = stations_ligne['x'].std()
        ecart_y = stations_ligne['y'].std()

        if ecart_x > ecart_y:
            # Ligne horizontale (ex: Ligne 1) -> On trie par Longitude (x)
            stations_ligne = stations_ligne.sort_values(by='x')
        else:
            # Ligne verticale (ex: Ligne 4) -> On trie par Latitude (y)
            # (Note: 'y' diminue du Nord au Sud, on trie inversé pour l'exemple, ou normal peu importe tant qu'elles se suivent)
            stations_ligne = stations_ligne.sort_values(by='y')

        # 3. Création des liens (i -> i+1)
        ids = stations_ligne['gares_id'].tolist()
        xs = stations_ligne['x'].tolist()
        ys = stations_ligne['y'].tolist()

        for i in range(len(ids) - 1):
            source = ids[i]
            cible = ids[i+1]
            
            # Calcul de la distance (poids) approximative (Pythagore simple)
            dist = np.sqrt((xs[i] - xs[i+1])**2 + (ys[i] - ys[i+1])**2)
            # On convertit en une valeur "temps" arbitraire (distance / vitesse)
            # Ici on laisse juste la distance brute ou un entier pour simplifier
            poids = int(dist / 100) # Division arbitraire pour avoir des petits chiffres
            if poids == 0: poids = 1

            liaisons.append({
                'source': source,
                'target': cible,
                'ligne': ligne_nom,
                'weight': poids
            })

    # 4. Sauvegarde dans le CSV
    df_liaisons = pd.DataFrame(liaisons)
    df_liaisons.to_csv('liaisons.csv', index=False, sep=';')
    print(f"✅ Terminé ! {len(df_liaisons)} liaisons créées dans 'liaisons.csv'.")
    print("Note : C'est une reconstruction automatique. Les embranchements (fourches) ne sont pas parfaits, mais suffisants pour un projet.")

if __name__ == "__main__":
    generer_liaisons_automatiques()