def create_structure ():
    return []

def push_to_structure (structure, element) :
    return [element]+structure

def pop_from_structure (structure) :
    (current_vertex, parent)=structure.pop()
    return (current_vertex, parent)

visited = [] # List for visited nodes.
queue = []     #Initialize a queue

def traversal (start_vertex, graph) :
    # First we create either a LIFO or a FIFO
    queuing_structure = new_queuing_structure() 
    # Add the starting vertex with None as parent
    queuing_structure.push((start_vertex, None))
    # Initialize the outputs 
    explored_vertices = [] 
    routing_table = {} 
    # Iterate while some vertices remain
    while len(queuing_structure) > 0 :
    
        # This will return the next vertex to be examined, and the choice of queuing structure will change the resulting order
        (current_vertex, parent) = queuing_structure.pop() 
    
        # Tests whether the current vertex is in the list of explored vertices
        if current_vertex not in explored_vertices :
            # Mark the current_vertex as explored
            explored_vertices.append(current_vertex) 
       
            # Update the routing table accordingly
            routing_table[current_vertex] = parent 
       
            # Examine neighbors of the current vertex
            for neighbor in neighbors(graph, current_vertex) :
              # We push all unexplored neighbors to the queue
                if neighbor not in explored_vertices :              
                    queuing_structure.push((neighbor, current_vertex))
              
    return explored_vertices, routing_table


def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    
    # Nothing to do here
    pass


def find_route (routing_table, source_location, target_location):
    route=[target_location]
    while target_location!=source_location:
        target_location=routing_table[target_location]
        route.append(target_location)
return route[::-1]


def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global listmouv
    return listmouv.pop()