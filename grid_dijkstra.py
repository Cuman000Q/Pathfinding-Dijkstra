# Consists of Class Node, class Dijkstra_algorithm, player and a Free grid
import random
import time


class Node():
    def __init__(self, name: str, x: int, y: int):
        self.name=name
        self.x=x
        self.y=y
        self.g=float('inf') # undefined cost of the node
        self.parent_node=None # undefined link to the previous node
    
    def __lt__(self, other_node):
        return self.g< other_node.g
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other_node):
        return self.name==other_node.name
    
    def __repr__(self):
        return f"Node: {self.name} cost= {self.g}"
    
class Dijkstra_algorithm():
    def __init__(self, start_node: Node, final_node: Node, graph: dict):
        self.start_node=start_node
        self.final_node=final_node
        self.graph=graph
    
    def find_cheapest_path(self):
        to_process_nodes=[] # using a stack method to make it efficient
        processed_nodes=set()

        to_process_nodes.append(self.start_node)
        self.start_node.g=0 # The first golden rule of Dijkstra's algorithm. To set the initial cost at 0
        while len(to_process_nodes)>0:
            to_process_nodes.sort() # sorting during the cycle. The second golden rule of Dijkstra's algorithm
            current_node=to_process_nodes.pop(0) # popping up the node

            processed_nodes.add(current_node) # putting in the processed_nodes set(works same as bin)

            if current_node.x==self.final_node.x and current_node.y==self.final_node.y:
                path=[] # path variable to recreate the path of nodes

                while current_node is not None:
                    path.append((current_node.x, current_node.y)) # adding to the path variable to recreate
                    current_node=current_node.parent_node # making the link to the previous node link
                
                return path[::-1]
            
            for neighbor_node, cost in self.graph.get(current_node, []):
                if neighbor_node in processed_nodes:
                    continue # searching for other nodes that are not wasted

                tentative_g=current_node.g + cost # calculating the whole path cost

                if tentative_g< neighbor_node.g: # if the calculated path costs less than neighbor_node cost
                    neighbor_node.g=tentative_g # then the new cost of neighbor_node is tentative_g
                    neighbor_node.parent_node=current_node # and neighbor_node previous node becomes the current_node

                    if neighbor_node not in to_process_nodes:
                        to_process_nodes.append(neighbor_node)
        
        return None # in case if there is only one node, return None
    
class Agent():
    def __init__(self, name: str, x: int, y: int):
        self.agent_name=name
        self.x=x
        self.y=y
    
    def is_neighbor(self, target):
        return abs(self.x - target.x) and abs(self.y - target.y)


class FGW(): # The abbriviation of Free_Grid_World
    def __init__(self, width: int, height: int, agent_nums= 1):
        self.width_map=width
        self.height_map=height
        self.agent_nums=agent_nums
        self.agent_population=[]
        self.grid=[]
        self.target_position=None
    
    def generate_agents(self):
        for i in range(self.agent_nums):
            x= random.randint(0, self.width_map-1)
            y=random.randint(0, self.height_map-1)

            agent=Agent(f"Agent_{i}", x, y)
            self.agent_population.append(agent)
        
        self.target_position= (random.randint(0, self.width_map-1), random.randint(0, self.height_map-1))
    
    def building_graph(self) -> dict:
        nodes_dict={} # creating a dictionary for nodes

        for x in range(self.width_map): # parsing through width
            for y in range(self.height_map): # parsing through height
                nodes=Node(f"Node_{x}_{y}", x, y) # making the nodes
                nodes_dict[(x,y)]=nodes # with the key of tuples (x,y) we are assingning them the node value

        graph={}

        for (x,y), node in nodes_dict.items():
            graph[node]=[]

            for dx, dy in [(0,0), (0,1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1)]:
                nx, ny = x+dx, y+dy # mechanism for a neighboring node

                if 0<=nx<self.width_map and 0<=ny<self.height_map: # if the neighbor node is on the grid
                    neighbor_node=nodes_dict[(nx, ny)] # we are making the neighbor_node as a key 
                    
                cost=1.414 if dx!=0 and dy!=0 else 1

                graph[node].append((neighbor_node, cost))
        return graph, nodes_dict
    
    def updating_grid(self):
        self.grid=[["." for _ in range(self.height_map)] for _ in range(self.width_map)]

        if self.target_position:

            tx, ty=self.target_position
            self.grid[ty][tx]=1
        
        for agent in self.agent_population:
            self.grid[agent.y][agent.x]=agent.name[0]

            if agent.x==tx and agent.y==ty:
                print(f"The agent {agent.name} has reached its target")
                print("Finishing the simulation...")
                break
    
    def move_with_dijkstra(self):
        graph, node_dict= self.building_graph()

        for agent in self.agent_population:
            start_node=node_dict[(agent.x, agent.y)]
            final_node=node_dict[self.target_position]

            solver=Dijkstra_algorithm(start_node, final_node, graph)

            path= solver.find_cheapest_path()

            if path and len(path)>1:
                next_x, next_y=path[1]
                agent.x=next_x
                agent.y=next_y