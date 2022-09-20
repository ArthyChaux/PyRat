def create_structure ():
    return []

def push_to_structure (structure, element) :
    return [element]+structure

def pop_from_structure (structure) :
    (current_vertex, parent)=structure.pop()
    return (current_vertex, parent)

visited = [] # List for visited nodes.
queue = []     #Initialize a queue

def traversal(start_vertex, graph, visited, node): #function for BFS
    queuing_structure=current_structure
    
    while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        print (m, end = " ") 
        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


Graph=(V,E)