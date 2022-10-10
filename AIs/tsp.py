MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

import random

import copy

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
##  

def find_route (routing_table, source_location, target_location) :
    route=[target_location]
    while target_location!=source_location:
        target_location=routing_table[target_location]
        route.append(target_location)
    return route [::-1]

##

import heapq
priority_queue = []

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



##

def build_meta_graph (maze_map, locations) :
#On crée un dictionaire
    meta_graph={}
#On parcourt chaque élément de la liste locations
    for loc in locations:
#On crée un dictionnaire vide associé à la clé (lieu)
        meta_graph[loc]={}
#On récupère la liste distances contenant des listes de 2 éléments [voisin,distance]
        distances=dijkstra(maze_map, loc)[3]
#On parcourt chaque liste de 2 éléments de la liste distances
        for x in distances:
#On ajoute dans le dictionnaire les lieux des pièces de fromages et leur distance associés à la clé
            if x[0] in locations and x[0]!=loc:
                meta_graph[loc][x[0]]=x[1]
    return meta_graph



def exhaustive_search(graph,pieces_of_cheese,player_location):
    remaining=pieces_of_cheese
    best=100000
    vertex=player_location
#On initialise la liste qui contiendra les différents chemins
    path=[player_location]
#On initialise la longueur du chemin à 0
    weight=0
#On créé la liste qui contiendra le meilleur chemin
    best_path=[]

def bruteforce(remaining, vertex, path, weight, graph):
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
            C=copy.deepcopy(remaining)
            C.remove(i)
        if weight + graph[vertex][i]<best:
            bruteforce(C, i, path+[i], weight + graph[vertex][i],graph)
            bruteforce(remaining,vertex,path,weight,graph)
    print (best_path)
    return best_path


listmouv=[]

def preprocessing (maze_map, maze_width, maze_height, player_location, opponent_location, pieces_of_cheese, time_allowed) :
    global listmouv
    global bestpath
    bestpath=exhaustive_search(build_meta_graph (maze_map, [player_location]+pieces_of_cheese),pieces_of_cheese,player_location)


i=1

def turn (maze_map, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed) :
    global listmouv
    global bestpath
    global i
#on parcourt notre liste bestpath
    if i!=(len(bestpath)+1):
#dès qu'on se déplace d'une case à l'autre, on change de lieu d'arrivée
        if listmouv==[]:
            listmouv=moves_from_locations(find_route (dijkstra(maze_map, player_location)[2], player_location, bestpath[i]))
            i+=1
    return listmouv.pop()