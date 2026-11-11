# The Goal: Based on the AI version problem, need to make
# so two objects on the same row could kill each other(or one of them)
#
# Every player chases the closest player still alive, one step per tick
# (horizontal, vertical or diagonal). A player that starts its turn next to
# its target (including diagonally) eliminates it. Last player standing wins.

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
            if other_players==self or not other_players.is_alive: # dead players can't be targets
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
        return True

    def is_neighbor(self, target):
        # neighbors = the 8 cells around the player (horizontal, vertical and diagonal)
        return abs(self.x- target.x)<=1 and abs(self.y- target.y)<=1


class Grid_world():
    def __init__(self, size=4):
        self.size=size
        self.grid=[["." for _ in range(size)] for _ in range(size)]
        self.player_list=[]
        self.tick=0

    def add_player(self, player: AIplayer):
        self.player_list.append(player)
        print(f"{player.name} has been added at ({player.x}, {player.y})")
        self.update_grid() # show the player on the grid right away

    def update_grid(self):
        self.grid=[["." for _ in range(self.size)] for _ in range(self.size)]

        for players in self.player_list:
            if 0<=players.x<self.size and 0<=players.y<self.size: # < size, the last index is size-1
                self.grid[players.y][players.x]=players.name[0]

        return self.grid

    def death_touch(self):
        bin=[]

        for player in self.player_list:
            if not player.is_alive: # eliminated earlier in this tick, can't act anymore
                continue

            target=player.find_close_player(self.player_list)

            if not target:
                continue

            if player.is_neighbor(target):
                print(f"{player.name} eliminated {target.name}")
                target.is_alive=False
                bin.append(target)
            else:
                player.move_towards_target(target)

        for dead_players in bin:
            if dead_players in self.player_list:
                self.player_list.remove(dead_players)
                print(f"{dead_players.name} has been removed")

    def show_grid(self):
        for row in self.grid:
            print(" ".join(row))

    def ticks(self):
        self.tick+=1
        print(f"\n--- Tick {self.tick} ---")

        self.death_touch()
        self.update_grid() # update first, so the grid shows what just happened
        self.show_grid()


if __name__ == "__main__":
    p1=AIplayer("Zhan")
    p2=AIplayer("Alen",6,6)
    p3=AIplayer("Leo",4,4)
    world=Grid_world(8)

    world.add_player(p1)
    world.add_player(p2)
    world.add_player(p3)

    print("\n--- Start ---")
    world.show_grid()

    while len(world.player_list)>1:
        world.ticks()
        time.sleep(1)

    if world.player_list:
        print(f"\nThe winner is: {world.player_list[0].name}")
    else:
        print("\nNo one survived")

# Fixed in this version (the bugs noted in version 1):
# - Players appear on the grid from the start: the grid is updated when a player is added.
# - The "distant" eliminations were a display problem: the grid was printed BEFORE the moves
#   of the tick, so it showed the previous positions. Now the grid is printed after the moves.
# - update_grid checked 0 <= x <= size, which allowed an index outside the grid. Now it is < size.
# - Eliminated players could still be chosen as targets during the same tick. Now they can't.
