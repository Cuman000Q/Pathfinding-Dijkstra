class Node():
    def __init__(self, name: str):
        self.name=name
        self.g= float('inf') # undefined g-score value, since we don't know
        self.parent_node= None # a link to the previous node to make a story
    
    def __lt__(self, other):
        return self.g< other.g # sorting by the lowest cost
    
    def __eq__(self, other):
        return self.name==other.name # sorting if names are equal
    
    def __hash__(self):
        return hash(self.name) # without calling the attribute of node, call for a self automatically input the node name
    
    def __repr__(self):
        return f"Node {self.name}, cost= {self.g}"


class Dijkstra_algorithm():
    # Rule 1 we are using the stack method, create a list of to-do- so it adds the nodes and done_list which adds listen that has been read
    # Rule 2 while looping the algorithm always sorting(by the lowest score, since it happens automatically)
    # Rule 3 setting the selg.g=0, since the first node does not have a connection to itself

    def __init__(self):
        self.count_path=0

    def find_cheapest_path(self, start_node: Node, final_node: Node, graph: dict):
        to_do_nodes=[]
        done_nodes=set()

        to_do_nodes.append(start_node)
        start_node.g=0

        while len(to_do_nodes)>0:
            to_do_nodes.sort()

            current=to_do_nodes.pop(0) # extracting the node from the list
            done_nodes.add(current) # adding it to the trash bin

            if current==final_node: # in case if we find a final node
                path=[] # making a path list, to recreate the path of the nodes

                while current is not None:
                    path.append(current) # adding the current node to the path
                    current=current.parent_node # assigning it the previous nodes
                
                return path[::-1]
            
            for neighbor, cost in graph.get(current, []):
                if neighbor in done_nodes:
                    continue

                tentative_g=current.g + cost # we are finding the cost of all the path

                if tentative_g<neighbor.g: # if the calculated overall cost is less than neighbor cost
                    neighbor.g=tentative_g # assign the overall cost to neighbor cost
                    neighbor.parent_node=current # assign the neighbor.parent_node variable a current node for a story, a link in other words

                    if neighbor not in to_do_nodes:
                        to_do_nodes.append(neighbor)
        
        return None

    
node_A=Node("A")
node_B=Node("B")
node_C=Node("C")
node_D=Node("D")

network = {
    node_A: [(node_B, 5), (node_C, 1)],
    node_B: [(node_D, 2)],
    node_C: [(node_B, 1), (node_D, 7)],
    node_D: []  # Destination node has no outgoing pathways
}

solver=Dijkstra_algorithm()

print(solver.find_cheapest_path(node_A, node_D, network))