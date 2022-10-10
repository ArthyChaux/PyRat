 
 

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

    # Tableau répertoriant les cases où passer pour aller du joueur au fromage
    route = dijkstra(maze_map, player_location, pieces_of_cheese[0])

    # Tableau répertoriant les deplacements à faire pour arriver au fromage
    next_moves = moves_from_route(route)


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves

    # Récupère le prochain déplacement à faire
    return next_moves.pop()

#################### Dijkstra #####################

import heapq


def dijkstra(maze_map, start_vertex, end_vertex):
    q = [(0, start_vertex, [])]
    seen = []
    mins = {start_vertex: 0}

    while q:
        (cost, v, path) = heapq.heappop(q)

        if v not in seen:
            seen.append(v)
            path = path + [v]

            if v == end_vertex:
                return path

            for neighbor in maze_map[v]:
                if neighbor in seen:
                    continue

                registered = mins.get(neighbor, None)
                calculated = cost + maze_map[v][neighbor]

                if registered is None or calculated < registered:
                    mins[neighbor] = calculated
                    heapq.heappush(q, (calculated, neighbor, path))

    return (float("inf"), [])


############## Utilitaries ##############

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
