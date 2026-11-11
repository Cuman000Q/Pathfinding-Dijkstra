# The Goal: Based on the AI version problem, need to make
# so two objects on the same row could kill each other(or one of them)

import math
import time


class AIplayer():
    def __init__(self, name: str, x=0, y=0):

        self.name=name
        self.is_alive=True
        self.x=x
        self.y=y
    
    def find_close_player(self, player_map: list):
        close_player=None
        min_val=float('inf')

        

        for other_players in player_map:
            if other_players==self:
                continue


            distance=math.dist([self.x, self.y], [other_players.x, other_players.y])

            if distance<min_val:
                min_val=distance
                close_player=other_players
        
        return close_player
    
    def move_towards_target(self, target):
        if not target:
            return False
        
        if self.x>target.x:
            self.x-=1
        elif self.x<target.x:
            self.x+=1
        
        if self.y>target.y:
            self.y-=1
        elif self.y<target.y:
            self.y+=1
    
    def is_neighbor(self, player_map: list):

        return abs(self.x- player_map.x)<=1 and abs(self.y- player_map.y)<=1
    

class Grid_world():
    def __init__(self, size=4):
        self.size=size
        self.grid=[[0 for _ in range(size)] for _ in range(size)]
        self.player_list=[]
        self.tick=0
    
    def add_player(self, player: AIplayer):
        self.player_list.append(player)
        print(f"{player.name} has been added")
    
    def update_grid(self):
        self.grid=[[0 for _ in range(self.size)] for _ in range(self.size)]

        if self.player_list:
            for players in self.player_list:
                if 0<=players.x<=self.size and 0<=players.y<=self.size:
                    self.grid[players.y][players.x]=players.name[0]
        else:
            return "No players"
        
        return self.grid
        
        
    def death_touch(self):
        bin=[]
        
        for player in self.player_list:
            if player in bin:
                continue
            
            target=player.find_close_player(self.player_list)

            if not target:
                continue


            if player.is_neighbor(target):
                print(f"{player.name} eleminated {target.name}")
                print(f"{target.name} has been removed")

                bin.append(target)
            else:
                player.move_towards_target(target)
        
        for dead_players in bin:
            if dead_players in self.player_list:
                self.player_list.remove(dead_players)
        
        self.update_grid()
    
    def show_grid(self):
        for row in self.grid:
            print(row)
    
    
    
    def ticks(self):
        self.tick+=1

        self.show_grid()
        self.death_touch()
        self.update_grid()




p1=AIplayer("Zhan")
p2=AIplayer("Alen",6,6)
p3=AIplayer("Leo",4,4)
world=Grid_world(8)

world.add_player(p1)
world.add_player(p2)
world.add_player(p3)

while len(world.player_list)>1:
    print(world.ticks())
    time.sleep(1)
print(world.show_grid())
    
    

print(f"The winners are: {world.player_list[0].name}")

# This version is a bit buggy, the project suggests to make the labels come each other till they are neighbors by horizontal, 
# vertical and diagonal moves. The core mechanics works perfect, but not how it should be.
# First of all, the players are not appearing on the grid before they got eliminated. Some of them eleminated before time to show up on the grid
# Second, the players are moving towards yeach of ther by column and row, but on diagonal they are distantly terminating the other player
# Third, in the columns, the players are "consume" each other even when they are not close to one cell. Need to find the core of this problem




