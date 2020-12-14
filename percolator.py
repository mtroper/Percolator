from collections import deque
import copy
import time
import random

#Remove a vertex from graph efficently
def remove(graph, index):
    v = [v for v in graph.V if v.index == index][0]
    edges = IncidentEdges(graph,v)
    extra_v = set()
    vertices_dict = {}
    #add all vertices to a dict
    for vertex in graph.V:
        vertices_dict[vertex] = 0
    #remove all incident edges
    for e in edges:
        graph.E.remove(e)
    #for every edge that exists add 1 to the value of the vertex
    for edge in graph.E:
        vertices_dict[edge.a] += 1
        vertices_dict[edge.b] += 1
    #remove the vertices that have a value of 0 (lone vertices)
    for key, value in vertices_dict.items():
        if value == 0:
            extra_v.add(key)
    graph.V.remove(v)
    graph.V.difference_update(extra_v)
    return graph

#returns all edges connected to vertex v ing raph
def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

#gets all possible children (graphs) of one vertice removed for a player
def getChildren(graph, player):
  	#all vertices colored player
    vertices = [v for v in graph.V if v.color == player]
    dict = {}
    #for all vertices, return graph with the removed vertex
    for v in vertices:
            x = copy.deepcopy(graph)
            g = remove(x, v.index)
            dict[g] = v.index
    return dict

######################################################################

# ---- helper methods for hardcoding in heuristic and choose color ----

#for graph of length 3, returns color of center node
def get_center_node(graph, player):
  for v in graph.V:
    if v.color == player and len(IncidentEdges(graph,v)) == 2:
      return player
    else:
      return (1-player)

# gets vertexes connected with one edge
# returns list
def singleEdgeVertexes(graph):
    return [vertex for vertex in graph.V if len(IncidentEdges(graph, vertex)) == 1]

# gets vertexes connected with two edges
def doubleEdgeVertexes(graph):
    return [vertex for vertex in graph.V if len(IncidentEdges(graph, vertex)) == 2]
            
# gets vertexes connected with three edges
def tripleEdgeVertexes(graph):
    return [vertex for vertex in graph.V if len(IncidentEdges(graph, vertex)) == 3]

# returns the number of vertices in a graph that are colored
def coloredVertices(graph):
    count = 0
    for vertex in graph.V:
        if vertex.color != -1:
            count += 1
    return count


######################################################################

#returns the best choice out of all the possible graphs
def heuristic(graphs, discovered, player, lost, currentPlayer):    
    weights = {}
    inidices_amount = {}
    weight = 0
    index = 0
    #We weight a state where we win and where we win negative
    for path, lostPlayer in lost.items():
        weight = 100
        if lostPlayer == player:
            weight = -100
        index = list(path)[0]
        #apply the weight of all graphs to the original path they correspond to
        if index in weights:
            inidices_amount[index] += 1
            weights[index] = (weights[index] + weight)
        else:
            inidices_amount[index] = 1
            weights[index] = weight
    
    for g in graphs:
        #Hardcoded cases for when the graph has 2,3 or 4 vertices
        
        #graph has 4 vertices
        if len(g.V) == 4:
            #case 1:
            if len(doubleEdgeVertexes(g)) == 2 and len(singleEdgeVertexes(g)) == 2:
                #coloring 1 (opposite vertexes, whoever goes first wins)
                player_vertex= [vertex for vertex in g.V if vertex.color == player][0]
                opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,player_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,player_vertex))][0]
                if opposite_vertex.color == player:
                    if currentPlayer == player:
                        weight = 100
                    else:
                        weight = -100
                #every other coloring is 2, so we can just say else
                # (whoever goes second wins)
                else:
                    if currentPlayer == player:
                        weight = -100
                    else:
                        weight = 100
            #case 2:
            if len(tripleEdgeVertexes(g)) == 1 and len(singleEdgeVertexes(g)) == 3:
                #whoever holds the center node, or the 3 edged node wins
                center_node = tripleEdgeVertexes(g)[0]
                if center_node.color == player:
                    weight = 100
                else:
                    weight = -100
            #case 3:
            if len(doubleEdgeVertexes(g)) == 4:
                #coloring 1 (opposite vertexes, whoever goes first wins)
                player_vertex= [vertex for vertex in g.V if vertex.color == player][0]
                opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,player_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,player_vertex))][0]
                if opposite_vertex.color == player:
                    if currentPlayer == player:
                        weight = 100
                    else:
                        weight = -100
                #coloring 2 (only other coloring (adjacent), whoever goes second wins)
                else:
                    if currentPlayer == player:
                        weight = -100
                    else:
                        weight = 100
            #case 4:
            if len(doubleEdgeVertexes(g)) == 2 and len(tripleEdgeVertexes(g)) == 2:
                #all colorings first person wins
                if currentPlayer == player:
                    weight = 100
                else:
                    weight = -100
            #case 5:
            if len(doubleEdgeVertexes(g)) == 2 and len(singleEdgeVertexes(g)) == 1 and len(tripleEdgeVertexes(g)) == 1:
                #coloring 1 (whoever has single and center node wins)
                single_node, center_node = singleEdgeVertexes(g)[0], tripleEdgeVertexes(g)[0]
                if single_node.color == center_node.color:
                    if single_node.color == player:
                        weight = 100
                    else:
                        weight = -100
                #coloring 2 (other case, first person wins)
                else:
                    if currentPlayer == player:
                        weight = 100
                    else:
                        weight = -100
            #case 6:
            if len(tripleEdgeVertexes(g)) == 4:
                #all colorings first person wins
                if currentPlayer == player:
                    weight = 100
                else:
                    weight = -100
            #case 7:
            if len(singleEdgeVertexes(g)) == 4:
                #all colorings second person wins
                if currentPlayer == player:
                    weight = -100
                else:
                    weight = 100
    
        #graph has 3 vertices
        if len(g.V) == 3:
            #case 1
            #whoever goes first wins
            if len(g.E) == 3:
                if player == currentPlayer:
                    weight = -100
                else:
                    weight = 100
            #case 2
            else:
                if get_center_node(g, player) == player:
                    weight = 100
                else:
                    weight = -100
        
        #graph has 2 vertices
        #case: o-o
        elif len(g.V) == 2:
            weight = 100
            if player != currentPlayer:
                weight = -100

        # end of hard code
######################################################################
        else:
            #without what we did previously, we weight a state based on how many more vertices we have than the opponent
            weight = (2 * len([v for v in g.V if v.color == player])) - len(g.V)
        
        #apply the weight of all graphs to the original path they correspond to
        index = discovered[g][0]
        if index in weights:
            inidices_amount[index] += 1
            weights[index] = (weights[index] + weight)
        else:
            weights[index] = weight
            inidices_amount[index] = 1
    
    #average the weights out so that for each path the weight is not a sum of all the weights but the average weight
    for index, amount in inidices_amount.items():
        weights[index] = weights[index] / amount
		
    #finding the best weight and the path it corresponds to
    bestIndex = list(weights.keys())[0]
    bestWeight = weights[bestIndex]
    for index, weight in weights.items():
        if weight > bestWeight:
            bestIndex = index
            bestWeight = weight
    return bestIndex
  
  

class PercolationPlayer:
    def ChooseVertexToColor(graph, player):
        g = graph
                
        vertex_to_choose = None
        
        #Hardcoded for when the graph has 4 vertices
        
        #graph has 4 vertices
        # - cases are possible configurations of graphs
        # - determined by number of single, double, and triple edge vertexes
        #    - single edge vertex has one incident edge, double edge vertex has two, etc.
        if len(g.V) == 4:
            #case 1:
            if len(doubleEdgeVertexes(g)) == 2 and len(singleEdgeVertexes(g)) == 2:
                #case 1 (we go first)
                if coloredVertices(g)%2 == 0:
                    #0 vertices colored, this is our first move
                    if coloredVertices(g) == 0:
                        #choose one of the top right vertexes
                        vertex_to_choose = singleEdgeVertexes(g)[0]
                        return vertex_to_choose
                    #2 vertices are colored, this is our second move
                    else:
                        #choose vertex opposite to the vertex we colored, if its colored, then choose random (we lost)
                        player_vertex= [vertex for vertex in g.V if vertex.color == player][0]
                        #opposite vertex should not share any edges
                        opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,player_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,player_vertex))][0]
                        #checks if taken
                        if opposite_vertex.color == 1-player:
                            #if taken return random (we lose)
                            return random.choice([v for v in graph.V if v.color == -1])
                        else:
                            #if not return opposite (we win)
                            return opposite_vertex
                #case 2 (we go second)
                else:
                    #1 vertex colored, this is our first move
                    if coloredVertices(g) == 1:
                        #we want to choose vertex opposite to theres, we can use code above
                        opponent_vertex = [vertex for vertex in g.V if vertex.color == 1-player][0]
                        opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,opponent_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,opponent_vertex))][0]
                        return opposite_vertex
                    #3 vertices colored, this is our second move
                    else:
                        #we can choose any vertex, we win no matter what
                        return random.choice([v for v in graph.V if v.color == -1])
            #case 2:
            if len(tripleEdgeVertexes(g)) == 1 and len(singleEdgeVertexes(g)) == 3:
                #case 1 (we go first)
                if coloredVertices(g)%2 == 0:
                    #0 vertices colored, this is our first move
                    if coloredVertices(g) == 0:
                        #choose center_node, we win no matter what
                        #center node is the one triple edge vertex
                        center_node = tripleEdgeVertexes(g)[0]
                        return center_node
                    #2 vertices are colored, this is our second move
                    else:
                        #since we have the center node, we can just pick randomly now
                        return random.choice([v for v in graph.V if v.color == -1])
                #case 2 (we go second)
                else:
                    #1 vertex colored, this is our first move:
                    if coloredVertices(g) == 1:
                        #let's assume they are dumb and maybe skipped over the center node
                        #if not, we return random, we lose no matter what
                        center_node = tripleEdgeVertexes(g)[0]
                        if center_node.color == -1:
                            return center_node
                        else:
                            return random.choice([v for v in graph.V if v.color == -1])
                    #3 vertices colored, 1 vertice left so we just choose the last vertex
                    else:
                        return random.choice([v for v in graph.V if v.color == -1])
            #case 3:
            if len(doubleEdgeVertexes(g)) == 4:
                #case 1 (we go first)
                if coloredVertices(g)%2 == 0:
                    #0 vertices colored, this is our first move
                    if coloredVertices(g) == 0:
                        #we color any random vertex, it doesn't matter what we choose first
                        return random.choice([v for v in graph.V if v.color == -1])
                    #2 vertices colored, this is our second move
                    else:
                        #we choose the opposite vertex of what we originally chose, we win no matter what if not taken
                        #if taken, we choose random (we lost)
                        #choose vertex opposite to the vertex we colored, if its colored, then choose random (we lost)
                        player_vertex= [vertex for vertex in g.V if vertex.color == player][0]
                        #opposite vertex should not share any edges
                        opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,player_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,player_vertex))][0]
                        #checks if taken
                        if opposite_vertex.color == 1-player:
                            #if taken return random (we lose)
                            return random.choice([v for v in graph.V if v.color == -1])
                        else:
                            #if not return opposite (we win)
                            return opposite_vertex
                #case 2 (we go second)
                else:
                    #1 vertex colored, this is our first move:
                    if coloredVertices(g) == 1:
                        #we choose the vertex opposite to theirs, we win no matter what
                        opponent_vertex = [vertex for vertex in g.V if vertex.color == 1-player][0]
                        opposite_vertex = [vertex for vertex in g.V if len(set(IncidentEdges(g, vertex) + IncidentEdges(g,opponent_vertex))) == len(IncidentEdges(g, vertex)) + len(IncidentEdges(g,opponent_vertex))][0]
                        return opposite_vertex
                    #3 vertices colored, this is our second move:
                    else:
                        #we can choose the last remaining vertex, we win no matter what
                        return random.choice([v for v in graph.V if v.color == -1])
            #case 4: non-optimal state 
            if len(doubleEdgeVertexes(g)) == 2 and len(tripleEdgeVertexes(g)) == 2:
                #case where we go second, if we go first we win no matter what
                if coloredVertices(g)%2 == 1:
                    #1 vertex colored, this is our first move
                    if coloredVertices(g) == 1:
                        #we choose the vertex with the same number of edges as the opponent
                        opponent_vertex = [vertex for vertex in g.V if vertex.color == 1-player][0]
                        if len(IncidentEdges(g, opponent_vertex)) == 3:
                            return [vertex for vertex in tripleEdgeVertexes(g) if vertex.color == -1][0]
                        else:
                            return [vertex for vertex in doubleEdgeVertexes(g) if vertex.color == -1][0]
                    #3 vertexes are colored, we just choose the last one
                    return random.choice([v for v in graph.V if v.color == -1]) 
            #case 5: 
            if len(doubleEdgeVertexes(g)) == 2 and len(singleEdgeVertexes(g)) == 1 and len(tripleEdgeVertexes(g)) == 1:
                #case 1 (we go first)
                if coloredVertices(g)%2 == 0:
                    #0 vertices colored, this is our first move
                    if coloredVertices(g) == 0:
                        #we want to choose the central node, or the node that is connectee to all 3
                        return tripleEdgeVertexes(g)[0]
                    #2 vertices colored, this is our second move
                    else:
                        #we want the single vertex, if taken, we can take either of the double vertexes
                        if singleEdgeVertexes(g)[0].color == -1:
                            return singleEdgeVertexes(g)[0]
                        else:
                            return doubleEdgeVertexes(g)[0]
                #case 2 (we go second)
                else:
                    #1 vertex colored, this is our first move
                    if coloredVertices(g) == 1:
                        #we want to choose the middle node, if its taken, we choose the single node
                        if tripleEdgeVertexes(g)[0].color == -1:
                            return tripleEdgeVertexes(g)[0]
                        else:
                            return singleEdgeVertexes(g)[0]
                    #3 vertices colored, this is our second move
                    else:
                        #we want to choose the last remaining vertex
                        return random.choice([v for v in graph.V if v.color == -1])

            #case 6: no optimal states, if they remove randomly they win
            #case 7: no optimal states, if they remove randomly they win
            
			# end of hard code
######################################################################

        all_verticies = [v for v in graph.V if v.color == -1]
        weights = []
        final_verticies = []
        for v in all_verticies:
            adjacent = False
            weight = 0
            edges = IncidentEdges(graph, v)
            weight += len(edges)
            for e in edges:
                #we want at least one adjact vertex to be our own (very important hence the 1000 weight)
                if not adjacent and (e.a.color == player or e.b.color == player):
                    weight += 1000
                    adjacent = True
                #want adjact to be non colored but not as important
                elif e.a.color == -1 and e.b.color == -1:
                        weight += 10
            final_verticies.append(v)
            weights.append(weight)
        #return best weight
        return final_verticies[weights.index(max(weights))]

######################################################################
      
    def ChooseVertexToRemove(graph, player):
        currentPlayer = player
        frontierFront = deque([graph])
        frontierBack = deque([])
        discovered = {graph: []}
        lost = {}
        t1 = time.time()
        index = 0
        #as long as we stay in time limit we can keep searching
        while 0.4 > (time.time() - t1):
            #searching a depth in a tree
            while (frontierFront and (0.4 > (time.time() - t1))):
                #BFS like algorithm
                #remove a graph from frotier
                currentGraph = frontierFront.popleft()
                #get it's children
                graphs = getChildren(currentGraph, currentPlayer)
                for key, value in graphs.items():
                    #for each child make its path to get there the path of parent plus the removed vertex
                    path = discovered[currentGraph].copy()
                    path.append(value)
                    #if the state is a state where a player loses add to lost dict
                    if len([v for v in key.V if v.color == 1 - currentPlayer]) == 0:
                        lost[tuple(path)] = 1 - currentPlayer
                    else:
                    #if its not a losing state add it to frontier so its children can be serached in next depth
                        frontierBack.append(key)
                        discovered[key] = path
            #swap fronteirFront with fronteriBack so it contains all the children
            frontierFront = frontierBack.copy()
            #remove fronteirBack so its ready for new children
            frontierBack = deque([])
            #change player
            currentPlayer = 1 - currentPlayer
            #choose best move for each depth
            index = heuristic(list(frontierFront), discovered, player, lost, currentPlayer)
        #return best move when time runs out
        return [vertex for vertex in graph.V if vertex.index == index][0]
