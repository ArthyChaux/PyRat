 
 
import heapq


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
    global next_moves

    #Construit le meta graph du labyrinthe, avec pour sommets les fromage et le joueur
    meta_graph = build_meta_graph(maze_map, [player_location]+pieces_of_cheese)
    print(meta_graph)

    #Choisis le meilleur parcours de fromage pour le rat à l'aide d'une recherche en greedy
    next_cheeses = greedy(maze_map, player_location, pieces_of_cheese)
    print(next_cheeses)


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves
    global next_cheeses

    #Si on est arrivé au fromage, on va au suivant
    if next_moves == []:
        routing_table = dijkstra(maze_map, player_location)[1]
        route = find_route(routing_table, player_location, next_cheeses.pop(0))
        next_moves = moves_from_route(route)
    
    print(next_moves)
    return next_moves.pop(0)


#################### Dijkstra #####################

def dijkstra(graph, start_vertex):
    q = [(0, start_vertex, [])]
    seen = []

    print(start_vertex)
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

def build_meta_graph (maze_map, vertices):
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

def greedy (graph, initial_vertex, vertices_to_visit) :
    current_vertex = initial_vertex
    visited_verticies = []
    #Initialisation Greedy

    while vertices_to_visit:
    #Tant qu'il y a des fromages dans le labyrinthe
        scores = give_score(graph, current_vertex, vertices_to_visit)
        score_minimal = min(scores.values())
        #La distance du fromage le plus proche du rat

        for vert in scores :
            if scores[vert] == score_minimal :
                visited_verticies.append(vert)
                vertices_to_visit.remove(vert)
                current_vertex = vert
                break
        #Donne dans l'ordre les fromages les plus proche du rat à visiter
    
    return visited_verticies

def give_score (graph, current_vertex, neighbors) :
    scores = {}
    explored_verticies = dijkstra(graph, current_vertex)[0]
    #Initialisation du score

    for neighbor in neighbors :
        scores[neighbor] = explored_verticies[neighbor]
        #Distance de chaque fromages voisins dans Score

    return scores




############## Utilitaries ##############

def moves_from_route(route):
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

def find_route(rooting_table, source_location, target_location):
    route = []
    t = target_location
    while t != source_location :
        route.append(t)
        t = rooting_table[t]
    route.append(t)
    return route
