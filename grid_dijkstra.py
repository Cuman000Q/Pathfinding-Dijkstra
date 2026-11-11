# Consists of Class Node, class Dijkstra_algorithm, player and a Free grid
#
# Agents are placed at random cells of a free grid (no walls) together with a random
# target. Every tick each agent runs Dijkstra's algorithm from its own cell to the target
# and takes one step along the cheapest path. Straight moves cost 1, diagonal moves 1.414.
# The simulation ends when the first agent reaches the target.
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
        to_process_nodes=[] # list of nodes waiting to be processed
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

        return None # no path to the target

class Agent():
    def __init__(self, name: str, x: int, y: int):
        self.agent_name=name
        self.x=x
        self.y=y

    def is_on_target(self, target_position):
        return (self.x, self.y)==target_position


class FGW(): # The abbreviation of Free_Grid_World
    # all 8 directions: right, left, down, up and the 4 diagonals
    DIRECTIONS=[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, width: int, height: int, agent_nums= 1):
        self.width_map=width
        self.height_map=height
        self.agent_nums=agent_nums
        self.agent_population=[]
        self.grid=[]
        self.target_position=None
        self.tick=0

    def generate_agents(self):
        self.target_position= (random.randint(0, self.width_map-1), random.randint(0, self.height_map-1))

        for i in range(self.agent_nums):
            x= random.randint(0, self.width_map-1)
            y=random.randint(0, self.height_map-1)

            agent=Agent(f"Agent_{i}", x, y)
            self.agent_population.append(agent)

    def building_graph(self):
        nodes_dict={} # creating a dictionary for nodes

        for x in range(self.width_map): # parsing through width
            for y in range(self.height_map): # parsing through height
                nodes=Node(f"Node_{x}_{y}", x, y) # making the nodes
                nodes_dict[(x,y)]=nodes # with the key of tuples (x,y) we are assigning them the node value

        graph={}

        for (x,y), node in nodes_dict.items():
            graph[node]=[]

            for dx, dy in self.DIRECTIONS:
                nx, ny = x+dx, y+dy # mechanism for a neighboring node

                if 0<=nx<self.width_map and 0<=ny<self.height_map: # only if the neighbor node is on the grid
                    neighbor_node=nodes_dict[(nx, ny)]
                    cost=1.414 if dx!=0 and dy!=0 else 1 # diagonal moves cost more
                    graph[node].append((neighbor_node, cost))
        return graph, nodes_dict

    def updating_grid(self):
        # rows = height (y), columns = width (x)
        self.grid=[["." for _ in range(self.width_map)] for _ in range(self.height_map)]

        if self.target_position:
            tx, ty=self.target_position
            self.grid[ty][tx]="X"

        for agent in self.agent_population:
            self.grid[agent.y][agent.x]=agent.agent_name[-1] # agent number on the map

    def show_grid(self):
        for row in self.grid:
            print(" ".join(row))

    def winner(self):
        for agent in self.agent_population:
            if agent.is_on_target(self.target_position):
                return agent
        return None

    def move_with_dijkstra(self):
        for agent in self.agent_population:
            # a fresh graph for every agent, because Dijkstra writes costs (g) and links
            # (parent_node) into the nodes, and they must not leak from one agent to another
            graph, node_dict= self.building_graph()
            start_node=node_dict[(agent.x, agent.y)]
            final_node=node_dict[self.target_position]

            solver=Dijkstra_algorithm(start_node, final_node, graph)

            path= solver.find_cheapest_path()

            if path and len(path)>1:
                next_x, next_y=path[1] # path[0] is the current cell, path[1] is the next step
                agent.x=next_x
                agent.y=next_y

    def run(self, delay=0.5):
        self.generate_agents()
        print(f"Target X at {self.target_position}")
        for agent in self.agent_population:
            print(f"{agent.agent_name} starts at ({agent.x}, {agent.y})")

        self.updating_grid()
        print("\n--- Start ---")
        self.show_grid()

        while self.winner() is None:
            self.tick+=1
            self.move_with_dijkstra()
            self.updating_grid()
            print(f"\n--- Tick {self.tick} ---")
            self.show_grid()
            time.sleep(delay)

        print(f"\nThe agent {self.winner().agent_name} has reached its target in {self.tick} ticks")
        print("Finishing the simulation...")


if __name__ == "__main__":
    world=FGW(width=10, height=8, agent_nums=3)
    world.run()
