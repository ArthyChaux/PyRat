#Le but de cet algorithme Greedy est de toujours se diriger vers le fromage le plus proche
#Il n'est pas optimal mais sa complexité plus faible que celle du TSP lui permet de fonctionner

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


import random
import heapq
priority_queue = []


def move_from_locations (source_location, target_location) :
    #Renvoie en fonction du trajet voulu le déplacement à faire
    difference = (target_location[0] - source_location[0], target_location[1] - source_location[1])
    if difference == (0, -1) :
        return MOVE_DOWN
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (-1, 0) :
        return MOVE_LEFT
    else :
        raise Exception("Impossible move")


def create_structure():
    return []


def dijkstra(start_vertex, graph):
    #Initialisation de l'algorithme de Djikstra
    structure = create_structure()
    heapq.heappush(structure, (0,start_vertex, None))
    explored_vertices = {}
    rooting_table = {}

    #Tant qu'il reste des noeuds inexplorés
    while len(structure) > 0 :
        #On récupère un noeud inexploré
        (distance, current_vertex, parent) = heapq.heappop(structure)

        if current_vertex not in explored_vertices:
            #On enregistre le noeud inexploré dans les tables à sauvegarder
            explored_vertices[current_vertex] = distance
            rooting_table[current_vertex] = parent

            #On enregistre les voisins inexplorés du noeud pour les explorer
            for neighbor in graph[current_vertex]:
                if neighbor not in explored_vertices:
                    newdistance = distance + graph[current_vertex][neighbor]
                    heapq.heappush(structure, (newdistance ,neighbor, current_vertex))
    
    return explored_vertices, rooting_table


def find_route(rooting_table, source_location, target_location):
    route = []
    t = target_location
    while t != source_location :
        route.append(t)
        t = rooting_table[t]
    route.append(t)
    return route

def moves_from_locations(locations):
    #Renvoie en fonction du trajet voulu les déplacements à faire
    moves = []

    for i in range(len(locations)-1) :
        moves.append(move_from_locations(locations[i],locations[i+1]))
    return moves

moves = []


def build_meta_graph (maze_map, pieces_of_cheese,player_location) :
    meta_graph = {}
    meta_graph2 = {}
    #meta_graph[player_location] = 0
    for cheese1 in pieces_of_cheese :
        if cheese1 != player_location :
            explored_vertices, rooting_table = dijkstra(player_location, maze_map)
            meta_graph[(player_location, cheese1)] = explored_vertices[cheese1]
        for cheese2 in pieces_of_cheese :
                explored_vertices, rooting_table = dijkstra(cheese1, maze_map)
                meta_graph[(cheese1,cheese2)] = explored_vertices[cheese2]
    for E1 in meta_graph :
        ver_dist = {}
        for E2 in meta_graph :
                if E2[0] == E1[0] :
                    ver_dist[E2[1]]= meta_graph[E2]
        meta_graph2[E1[0]] = ver_dist
    return meta_graph2


def give_score (graph, current_vertex, neighbors) :
    scores = {}
    explored_verticies = dijkstra(current_vertex,graph)[0]
    #Initialisation tableau Score
    for neighbor in neighbors :
        scores[neighbor] = explored_verticies[neighbor]
        #pour chaque fromages, on calcule la distance qui sépare le rat du fromage pour la stocker dans Score
    return scores

def greedy (graph, initial_vertex, vertices_to_visit) :
    current_vertex = initial_vertex
    visited_verticies = []
    #Initialisation Greedy
    while vertices_to_visit :
        scores = give_score(graph,current_vertex,vertices_to_visit)
        score_minimal = min(scores.values())
        #Distance du fromage le plus proche du rat
        for vert in scores :
            if scores[vert] == score_minimal :
                visited_verticies.append(vert)
                vertices_to_visit.remove(vert)
                current_vertex = vert
                break
    #On va à chaque fois au fromage le plus proche jusqu'à ce qu'il n'y ai plus de fromage
    return visited_verticies


def meta_graph_route_to_route(localisations,maze_map) :
    route2 = []
    route = []
    for i in range(len(localisations)-1):
        explored_vertices1, rooting_table1 = dijkstra(localisations[i], maze_map)
        route = find_route(rooting_table1, localisations[i], localisations[i+1])[:-1]
        route.reverse()
        route2 = route2 + route
    return  [localisations[0]] + route2


def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global moves
    meta_graph = build_meta_graph(maze_map, pieces_of_cheese,player_location)
    chemin = [player_location] + greedy(maze_map,player_location,pieces_of_cheese)
    print(chemin)
    route = meta_graph_route_to_route(chemin,maze_map)
    moves = moves_from_locations(route)


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global moves
    if moves :
         return moves.pop(0)