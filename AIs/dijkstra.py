 
 

  # Directions possibles
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

# Liste des déplacements à suivre
next_moves = []



############## PYRAT BFS functions ##############

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global next_moves


    # Table qui référence les déplacements à faire pour se rapprocher du joueur pour chaque case
    routing_table = dijkstra(player_location, maze_map)
    
    # Tableau répertoriant les cases où passer pour aller du joueur au fromage
    route = find_route(routing_table, player_location, pieces_of_cheese[0])


    # Tableau répertoriant les deplacements à faire pour arriver au fromage
    next_moves = moves_from_route(route)


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves

    # Récupère le prochain déplacement à faire
    return next_moves.pop()

#################### Dijkstra #####################

import heapq


def dijkstra(start_vertex, maze_map):
    # Initialisation de la routing table et du min_heap
    min_heap = []
    heapq.heappush(min_heap, (0, (start_vertex, None)))

    routing_table = {}
    routing_table[start_vertex] = None

    # Parcours du labyrinthe entier
    while not(min_heap == []):
        distance, tuplee = heapq.heappop(min_heap)
        v, parent = tuplee

        for neighbor in maze_map[v]:
            distance_through_v = distance + maze_map[v][neighbor]

            heapq.heappush(min_heap, (distance_through_v, (neighbor, v)))
            routing_table[neighbor] = v
    
    print(routing_table)
    input()

    return routing_table
    

def find_route(routing_table, source_location, target_location):
    # Renvoie un tableau répertoriant le chemin à suivre pour aller de source_location à target_location
    # De la forme [source_location, ......, target_location]

    route = [target_location]

    while target_location != source_location:
       target_location = routing_table[target_location]
       route.append(target_location)

    return route[::-1]

def moves_from_route(route) :
    # Transforme une route (tableau de cases à suivre) en tableau de déplacements

    moves = []
    for i in range (len(route)-1):
        difference = (route[i+1][0] - route[i][0], route[i+1][1] - route[i][1])
        if difference == (0, -1) :
            moves.append (MOVE_DOWN)
        elif difference == (0, 1) :
            moves.append (MOVE_UP)
        elif difference == (1, 0) :
            moves.append (MOVE_RIGHT)
        elif difference == (-1, 0) :
            moves.append (MOVE_LEFT)
        else :
            raise Exception("Impossible move")
    
    return moves[::-1]
