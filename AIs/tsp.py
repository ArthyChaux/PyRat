 
 
import random
import copy


# Directions possibles
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

# Liste des déplacements à suivre
next_moves = []
bestpath = []



############## PYRAT TSP functions ##############

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global bestpath

    #Construit le meta graph du labyrinthe, avec pour sommets les fromage et le joueur
    meta_graph = build_meta_graph(maze_map, [player_location]+pieces_of_cheese)
    #Choisis le meilleur chemin pour le rat à l'aide d'une recherche exhaustive
    bestpath = exhaustive_search(meta_graph, pieces_of_cheese, player_location)

i = 1
def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves
    global bestpath
    global i

    #on parcourt notre liste bestpath
    if i != (len(bestpath)+1):
#dès qu'on se déplace d'une case à l'autre, on change de lieu d'arrivée
        if next_moves == []:
            a = dijkstra(maze_map, player_location)[1]
            route = find_route (a, player_location, bestpath[i])
            next_moves = moves_from_route(route)
            i += 1
    
    return next_moves.pop()


#################### Dijkstra #####################

import heapq
priority_queue = []

def dijkstra(graph, start_vertex):
    #Initialisation
    explored_vertices = []
    distances = {(0,0) : 0}
    routing_table = {}
    min_heap = priority_queue
    heapq.heappush(min_heap, (start_vertex, 0))

    #L contient les lieux auxquels une distance est conjointe dans le dictionnaire de distances
    L = []
    #distance_meta contiendra toutes les distances par rapport à start_vertex
    distance_meta = []

    # algorithm loop
    while len(min_heap)>0:
        v, distance = heapq.heappop(min_heap)
        distance_meta.append([v, distance])

        if v not in explored_vertices:
            explored_vertices.append(v)
            d=distance

            for neighbor in graph[v]:
                if neighbor not in explored_vertices:
                    distance_through_v = distance + graph[v][neighbor]
                    heapq.heappush(min_heap, (neighbor, distance_through_v))

                    if neighbor in L and distance_through_v < distances[neighbor]:
                        distances[neighbor]=distance_through_v
                        routing_table[neighbor]=v
                    elif neighbor not in L:
                        distances[neighbor]=distance_through_v
                        routing_table[neighbor]=v
                    
                    L.append(neighbor)
    
    return distances, routing_table, distance_meta


#################### Meta graph #####################

def build_meta_graph (maze_map, vertices) :
    #Initialisation du graphe
    meta_graph = {}

    #Pour chaque sommet
    for v in vertices:
        meta_graph[v] = {}

        #On récupère la liste des distances aux autres sommets
        distances = dijkstra(maze_map, v)[2]

        #On choisis chaque couples de distance entre v et les autres sommets
        for (v1, d) in distances:
            #On les aujoute au meta graph
            if v1 in vertices and v1 != v:
                meta_graph[v][v1] = d
    
    return meta_graph


def exhaustive_search(meta_graph, pieces_of_cheese, player_location):
    remaining = pieces_of_cheese
    best = 100000
    vertex = player_location
#On initialise la liste qui contiendra les différents chemins
    path = [player_location]
#On initialise la longueur du chemin à 0
    weight = 0
#On créé la liste qui contiendra le meilleur chemin
    best_path = []

    def bruteforce(remaining, vertex, path, weight, meta_graph):
        #On met ces variables en non local pour pouvoir les appeler dans les 2 fonctions
        nonlocal best_path
        nonlocal best
    #dès que le chemin a visité tout les lieux, on regarde si c'est le plus court chemin
        if remaining ==[]:
            if weight < best:
                best = weight
                best_path = path
    #tant qu'il reste des lieux à visiter, on utilise le recursif
        else:
            for i in remaining:
                C = copy.deepcopy(remaining)
                C.remove(i)
                if weight + meta_graph[vertex][i]<best:
                    bruteforce(C, i, path+[i], weight + meta_graph[vertex][i], meta_graph)
    
    bruteforce(remaining,vertex,path,weight,meta_graph)
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


