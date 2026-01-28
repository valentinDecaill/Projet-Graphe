# Analyse de Réseau de Transport

## Description du Projet
Ce projet a pour but de modéliser, visualiser et analyser un réseau de métro en utilisant la théorie des graphes et le langage Python.

L'objectif est de transformer des données géographiques (stations) et structurelles (lignes) en un objet mathématique (Graphe) afin d'appliquer des algorithmes classiques pour résoudre des problèmes de transport (plus court chemin, identification des hubs critiques, robustesse du réseau ...).

## Outils
* **Langage :** Python
* **Bibliothèques principales :**
    * `networkx` : Création, manipulation du graphe et calculs algorithmiques.
    * `matplotlib` : Visualisation graphique du réseau et des résultats.
    * `scipy` : Calculs d'algèbre linéaire (optimisation pour les grands graphes).

## Concepts de Théorie des Graphes

Le projet repose sur la modélisation suivante : **$G = (V, E, W)$**

### 1. Modélisation
* **Nœuds ($V$) :** Les stations de métro. Chaque nœud possède des attributs spatiaux $(x, y)$.
* **Arêtes ($E$) :** Les sections de tunnel reliant deux stations adjacentes.
* **Pondération ($W$) :** Le poids $w_{ij}$ associé à l'arête $(i, j)$ représente le **temps de trajet** entre les stations.

### 2. Algorithmes Implémentés
* **Plus Court Chemin (Dijkstra) :**
  Calcul de l'itinéraire optimal pour minimiser le temps de transport entre deux points du réseau.
  *Complexité : $O(E + V \log V)$*

* **Centralité d'Intermédiarité (Betweenness Centrality) :**
  Mesure de la fréquence à laquelle une station apparaît sur les plus courts chemins entre tous les autres nœuds. Cela permet d'identifier les **goulets d'étranglement** du réseau.
  $$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

* **Analyse de Robustesse :**
  Simulation de pannes : suppression des nœuds à forte centralité pour observer l'impact sur la connexité globale du graphe.
