



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
    routing_table = traversal(player_location, maze_map)[1]
    
    # Tableau répertoriant les cases où passer pour aller du joueur au fromage
    route = find_route(routing_table, player_location, pieces_of_cheese[0])

    # Tableau répertoriant les deplacements à faire pour arriver au fromage
    next_moves = moves_from_route(route)


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global next_moves

    # Récupère le prochain déplacement à faire
    return next_moves.pop()


############## Utilitaries ##############

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


############## FIFO Implementation ##############

def create_structure () :
    # Create an empty FIFO
    return []

def push_to_structure (structure, element) :
    # Add an element to the FIFO
    return [element] + structure

def pop_from_structure (structure) :
    # Extract an element from the FIFO
    (current_vertex, parent) = structure.pop()
    return (current_vertex, parent)

def traversal (start_vertex, graph) :
    # BFS traversal
    # First we create either a LIFO or a FIFO
    queuing_structure = create_structure()

    # Add the starting vertex with None as parent
    queuing_structure = push_to_structure (queuing_structure,(start_vertex, None))

    # Initialize the outputs
    explored_vertices = []
    routing_table = {}

    # Iterate while some vertices remain
    while len(queuing_structure) > 0:

        # This will return the next vertex to be examined, and the choice of queuing structure will change the resulting order
        (current_vertex, parent) = pop_from_structure (queuing_structure)

        # Tests whether the current vertex is in the list of explored vertices
        if current_vertex not in explored_vertices:
            # Mark the current_vertex as explored
            explored_vertices.append(current_vertex)
            # Update the routing table accordingly
            routing_table[current_vertex] = parent

            # Examine neighbors of the current vertex
            for neighbor in graph[current_vertex]:
              # We push all unexplored neighbors to the queue
                if neighbor not in explored_vertices:
                    queuing_structure = push_to_structure(queuing_structure,(neighbor, current_vertex))

    return explored_vertices, routing_table