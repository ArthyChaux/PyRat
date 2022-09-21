MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

import random
def random_move () :
    all_moves = [MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP]
    return random.choice(all_moves)

def move_from_locations (source_location, target_location) :
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

def moves_from_locations (locations) :
    seq_move=[]
    for i in range (len(locations)-1):
        difference = (locations[i+1][0] - locations[i][0], locations[i+1][1] - locations[i][1])
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

visited_locations=[]


def random_move (map,location):
    global visited_locations

    L=list(map[location].keys())
    a=random.choice(L)
    for i in range(len(L)-1,-1,-1):
        if L[i] in visited_locations:
            del L[i]
    if len(L)==0:
        return move_from_locations(location,a)
    else:
        return move_from_locations(location,random.choice(L))

listmouv=[]

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global listmouv
    listmouv=moves_from_locations(find_route (traversal(player_location,maze_map)[1], player_location, pieces_of_cheese[0]))
##
def create_structure () :
    # Create an empty FIFO
    return []

def push_to_structure (structure, element) :
    # Add an element to the FIFO
    return [element]+structure

def pop_from_structure (structure) :
    # Extract an element from the FIFO
    (current_vertex, parent)=structure.pop()
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
    while len(queuing_structure) > 0 :

        # This will return the next vertex to be examined, and the choice of queuing structure will change the resulting order
        (current_vertex, parent) = pop_from_structure (queuing_structure)

        # Tests whether the current vertex is in the list of explored vertices
        if current_vertex not in explored_vertices :

            # Mark the current_vertex as explored
            explored_vertices.append(current_vertex)

            # Update the routing table accordingly
            routing_table[current_vertex] = parent

            # Examine neighbors of the current vertex
            for neighbor in graph[current_vertex] :

              # We push all unexplored neighbors to the queue
                if neighbor not in explored_vertices :
                    queuing_structure = push_to_structure (queuing_structure,(neighbor, current_vertex))

    return explored_vertices, routing_table

def find_route (routing_table, source_location, target_location) :
    route=[target_location]
    while target_location!=source_location:
       target_location=routing_table[target_location]
       route.append(target_location)
    return route [::-1]


##

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global listmouv
    return listmouv.pop()