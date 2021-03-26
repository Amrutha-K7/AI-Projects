import sys #required for getting command line arguments
import re  #required for parsing the file


def readInputFile(InputfileName): #Parses input file and returns graph
  global graph_distance
  input_fh=open(InputfileName)
  graph={} #initialize empty graph
  for line in input_fh:
     line = line.rstrip('\r') #for old Mac
     line = line.rstrip('\r\n') #for windows
     line = line.rstrip('\n') #for Linux
     if(line=='END OF INPUT'):
         return graph
     else:
         match=re.match('(.*)\s+(.*)\s+(.*)',line)
         if match.group(1) in graph:  # city1 to city2
             graph[match.group(1)].append(match.group(2))
         else:
             graph[match.group(1)] = [match.group(2)]

         # save step cost to separate dictionary
         graph_distance[match.group(1) + match.group(2)] = float(match.group(3));

         #same as above but from city2 to city1
         if match.group(2) in graph:  #city2 to city1
             graph[match.group(2)].append(match.group(1))
         else:
             graph[match.group(2)] = [match.group(1)]

         # save step cost to separate dictionary
         graph_distance[match.group(2)+match.group(1)] = float(match.group(3));

  input_fh.close() #close the file

def parseHeuristicFile(InputHeuristicFileName):
    fh = open(InputHeuristicFileName)
    heuristic_map = {}
    for line in fh:
        line = line.rstrip('\r') #for old Mac
        line = line.rstrip('\r\n') #for windows
        line = line.rstrip('\n') #for Linux
        if line == 'END OF INPUT':
            return heuristic_map
        else:
            match = re.match('(.*)\s+(.*)',line)
            heuristic_map[match.group(1)] = float(match.group(2))
    fh.close()

#data structure to track node related info
class nodeInfo:
    global is_informed_search
    def __init__(self, parent, state, g, f):
        self.parent = parent
        self.state = state
        self.g = g #additive_cost
        self.f = f #f(n)=g(n)+h(n), g(n) is additive_cost, h(n) is heuristic ==> this is relevant if heuristic is provided

    #below ones are required to be customized to define sorting behaviour for fringe
    def __lt__(self, other):
        if not is_informed_search:
            return (self.g < other.g)
        else:
            return (self.f < other.f)

    def __gt__(self, other):
        if not is_informed_search:
            return (self.g > other.g)
        else:
            return (self.f > other.f)

def gen_succesors(source_node, map, heuristic_map): #generating successors
    successors = []
    list_state_cost = map[source_node.state]
    for current_city in list_state_cost:
        additive_cost = source_node.g + graph_distance[source_node.state+current_city]
        if not is_informed_search:
            successors.append(nodeInfo(source_node, current_city, additive_cost, 0))
        else:
            #f(n)=g(n)+h(n), g(n) is additive_cost, h(n) is heuristic
            successors.append(nodeInfo(source_node, current_city, additive_cost, additive_cost + heuristic_map[current_city]))
    return successors

def printRoute(current_node, map):
    global graph_distance
    path = [] # List for saving path
    distance = current_node.g
    
    while 1: #infinite loop until some condition is met
        parent = current_node.parent
        if parent is not None:
            path.append(parent.state + ' to ' + current_node.state + ', ' + str(graph_distance[parent.state+current_node.state]) + ' km')
        current_node = parent
        if current_node==None :
            break

    path.reverse() #revesering the make it display from Parent to goal
    print('distance:' + str(distance) + ' km'+'\nroute:')
    for path_string in path:
        print(path_string)


if(len(sys.argv) == 5):
    is_informed_search=1
    heuristic_filename=sys.argv[4]
    print("\nThis is informed search\n")
else:
    is_informed_search=0
    heuristic_filename=None
    print("\nThis is uninformed search\n")

#all initialization
input_filename=sys.argv[1]
num_expanded_nodes  = 0  # number of nodes expanded = number of nodes popped from fringe
num_generated_nodes = 0  #number of nodes generated=Number of nodes added to fringe
graph_distance = {} #this contains
heuristic_map = {}
fringe = []
closed_set = [] #list used to track explored nodes

graph = readInputFile(input_filename)

if is_informed_search:
    # This would parse heuristic file and returns a hash
    heuristic_map = parseHeuristicFile(heuristic_filename)


if not is_informed_search:
    fringe.append(nodeInfo(None, sys.argv[2], 0, 0))
else:
    fringe.append(nodeInfo(None, sys.argv[2], 0, heuristic_map[sys.argv[2]]))

#increment this everytime node is added to fringe
num_generated_nodes+=1


while len(fringe) > 0:
    #increment expanded nodes everytime node is popped from fringe
    num_expanded_nodes += 1
    current_node = fringe.pop(0)
    if current_node.state == sys.argv[3]:  # state == goal?
        print('nodes expanded:  ' + str(num_expanded_nodes))
        print('nodes generated: ' + str(num_generated_nodes))
        printRoute(current_node, graph)
        sys.exit()
    else:
        if current_node.state not in closed_set:
            closed_set.append(current_node.state)
            successor = gen_succesors(current_node, graph, heuristic_map)
            for succ in successor:
                fringe.append(succ)
                num_generated_nodes += 1
            fringe.sort()

#if above while exits then goal state is not reached
print('nodes expanded:  ' + str(num_expanded_nodes))
print('nodes generated: ' + str(num_generated_nodes)+'\ndistance: infinity\nroute:\nnone')