# Fly-in Project -- Roadmap

## 1. Objectif

Passer d'un parser fonctionnel à un système complet : - Parser -
Représentation des données (objets) - Graphe - Pathfinding -
Simulation - Optimisation

------------------------------------------------------------------------

## 2. Structure des classes

### Zone

-   name
-   x, y
-   zone_type
-   color
-   max_drones
-   is_start / is_end

### Connection

-   zone_a
-   zone_b
-   max_link_capacity

### DroneMap

-   nb_drones
-   zones (dict)
-   connections (list)
-   adjacency (dict)
-   start_zone
-   end_zone

------------------------------------------------------------------------

## 3. Parser (à améliorer)

### À corriger :

-   Reset des valeurs par défaut à chaque ligne
-   Vérifier len(...) == attendu
-   Corriger logique metadata (pas de else mal placé)
-   Gérer lignes vides
-   Vérifier doublons de connexions
-   Valider noms (pas d'espace ni '-')

------------------------------------------------------------------------

## 4. Construire le graphe

Créer une adjacency list :

{ "A": \["B", "C"\], "B": \["A"\] }

------------------------------------------------------------------------

## 5. Pathfinding (1 drone)

Objectif : - Aller de start → end - Éviter blocked - Gérer coûts : -
normal = 1 - priority = 1 (favorisé) - restricted = 2

Algorithme conseillé : Dijkstra simplifié

------------------------------------------------------------------------

## 6. Simulation

Tour par tour : - Chaque drone peut bouger ou attendre - Gérer : -
capacité des zones - capacité des connexions - transit (restricted = 2
tours)

Créer classe DroneState

------------------------------------------------------------------------

## 7. Multi-drones

Ajouter : - Distribution sur plusieurs chemins - Attente stratégique -
Éviter collisions - Maximiser débit

------------------------------------------------------------------------

## 8. Output

Format : D1-zoneA D2-zoneB

------------------------------------------------------------------------

## 9. Plan de travail

1.  Parser → retourne DroneMap
2.  Graphe
3.  Pathfinding simple
4.  Simulation 1 drone
5.  Multi-drones
6.  Optimisation

------------------------------------------------------------------------

## Conclusion

Ne reste pas bloqué sur le parsing. Passe rapidement à : parser → objets
→ graphe → algo → simulation
