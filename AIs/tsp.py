 
 
import copy


# Directions possibles
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

# Liste des déplacements à suivre
next_moves = []
next_cheeses = []



############## PYRAT TSP functions ##############

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global next_cheeses

    #Construit le meta graph du labyrinthe, avec pour sommets les fromage et le joueur
    meta_graph = build_meta_graph(maze_map, [player_location]+pieces_of_cheese)
    print(meta_graph)

    #Choisis le meilleur parcours de fromage pour le rat à l'aide d'une recherche exhaustive
    next_cheeses = exhaustive_search(meta_graph, player_location, pieces_of_cheese)
    print(next_cheeses)

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves
    global next_cheeses

    #Si on est arrivé au fromage, on va au suivant
    if next_moves == []:
        routing_table = dijkstra(maze_map, player_location)[1]
        route = find_route(routing_table, player_location, next_cheeses.pop(0))
        next_moves = moves_from_route(route)
    
    return next_moves.pop()


#################### Dijkstra #####################

import heapq

def dijkstra(graph, start_vertex):
    q = [(0, start_vertex, [])]
    seen = []
    #Dictionnaire des distances par rapport à start_vertex
    distances = {start_vertex: 0}
    #Routing table
    routing_table = {}

    while q:
        (cost, v, path) = heapq.heappop(q)

        if v not in seen:
            seen.append(v)
            path = path + [v]

            for neighbor in graph[v]:
                if neighbor in seen:
                    continue

                registered = distances.get(neighbor, None)
                calculated = cost + graph[v][neighbor]

                if registered is None or calculated < registered:
                    distances[neighbor] = calculated
                    routing_table[neighbor] = v
                    heapq.heappush(q, (calculated, neighbor, path))

    return distances, routing_table


#################### Meta graph #####################

def build_meta_graph (maze_map, vertices) :
    #Initialisation du graphe
    meta_graph = {}

    #Pour chaque sommet
    for v in vertices:
        meta_graph[v] = {}

        #On récupère la liste des distances aux autres sommets
        distances = dijkstra(maze_map, v)[0]

        #On choisis chaque couples de distance entre v et les autres sommets
        for v1 in distances:
            #On les ajoute au meta graph
            if v1 in vertices and v1 != v:
                meta_graph[v][v1] = distances[v1]
    
    return meta_graph


def exhaustive_search(meta_graph, player_location, pieces_of_cheese):
    best = 100000
    best_path = []

    #Initialisation des variables de construction de chemin
    path = []
    weight = 0
    remaining_cheeses = pieces_of_cheese

    def bruteforce(remaining_cheeses, vertex, path, weight, meta_graph):
        #On met ces variables en non local pour pouvoir les appeler dans les 2 fonctions
        nonlocal best_path
        nonlocal best

        #Si le chemin est plus court, on le sauvegarde
        if remaining_cheeses == []:
            if weight < best:
                best = weight
                best_path = path

        #On construit tous les chemins
        else:
            #Construit chaque chemin, en parcourant les fromages dans des sens différents
            for i in remaining_cheeses:
                C = copy.deepcopy(remaining_cheeses)
                C.remove(i)
                bruteforce(C, i, path+[i], weight + meta_graph[vertex][i], meta_graph)
    
    #Garde le best_path en parcourant tous les chemins possible
    bruteforce(remaining_cheeses, player_location, path, weight, meta_graph)
    return best_path

############## Utilitaries ##############

def moves_from_route(route) :
    seq_move = []
    for i in range (len(route)-1):
        difference = (route[i+1][0] - route[i][0], route[i+1][1] - route[i][1])
        if difference == (0, -1) :
            seq_move.append (MOVE_DOWN)
        elif difference == (0, 1) :
            seq_move.append (MOVE_UP)
        elif difference == (1, 0) :
            seq_move.append (MOVE_RIGHT)
        elif difference == (-1, 0) :
            seq_move.append (MOVE_LEFT)
        else :
            raise Exception("Impossible move")
    return seq_move[::-1]


def find_route(routing_table, source_location, target_location) :
    route = [target_location]

    while target_location != source_location:
        target_location = routing_table[target_location]
        route.append(target_location)

    return route [::-1]


