import sys
sys.path.append(f'{sys.path[0]}\\..\\project_ai')

from core import *
import pygame
import random
import string


class Cell:
    def __init__(self, window, window_size, x, y, width, height,
                 border_color=(40, 40, 40),
                 border=2
                 ):

        self.window = window
        self.window_size = window_size
        self.rect = pygame.Rect(x, y, width, height)
        self.border_color = border_color
        self.border = border

        self.evolution = 0
        self.parent = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        self.save_coords = (self.rect.x // self.rect.width, self.rect.y // self.rect.height)

        self.max_hp = [0, 20, 100]
        self.max_food = [0, 20, 100]
        self.max_water = [0, 20, 100]
        self.max_energy = [0, 20, 100]
        self.max_underwater_time = [0, 3, 5]

        self.ai = FullConnected(size=[5 + 5 + 3 + 2 + 3 * (self.window_size[0] // self.rect.width) * (self.window_size[1] // self.rect.height), 16, 4, 4])

    def color_init(self):
        color = []
        for i in range(3):
            alpha = random.randint(0, 2)
            if alpha == 0:
                color += [random.randint(0, 63)]
            elif alpha == 1:
                color += [random.randint(64, 191)]
            elif alpha == 2:
                color += [random.randint(192, 255)]

        self.color = tuple(color)

    def genes_init(self):
        self.max_hp[0] = random.randint(self.max_hp[1], self.max_hp[2])
        self.max_food[0] = random.randint(self.max_food[1], self.max_food[2])
        self.max_water[0] = random.randint(self.max_water[1], self.max_water[2])
        self.max_energy[0] = random.randint(self.max_energy[1], self.max_energy[2])
        self.max_underwater_time[0] = random.randint(self.max_underwater_time[1], self.max_underwater_time[2])

        self.hp = self.max_hp[0]
        self.food = self.max_food[0]
        self.water = self.max_water[0]
        self.energy = self.max_energy[0]
        self.underwater_time = self.max_underwater_time[0]

        self.cons_food = random.randint(5, 9)
        self.cons_water = random.randint(5, 9)
        self.cons_energy = random.randint(5, 9)

    def add_food(self, add_food=0):
        self.food += add_food
        self.hp += 0.2 * add_food
        self.energy += 0.1 * add_food

        if self.food > self.max_food[0]:
            over_food = self.food - self.max_food[0]
            self.hp += 0.02 * over_food
            self.energy += 0.01 * over_food

            self.food = self.max_food[0]

    def add_water(self, add_water=0):
        self.water += add_water
        self.energy += 0.1 * add_water

        if self.water > self.max_water[0]:
            over_water = self.water - self.max_water[0]
            self.energy += 0.01 * over_water

            self.water = self.max_water[0]

    def add_energy(self, add_energy=0):
        self.energy += add_energy

        if self.energy > self.max_energy[0]:
            self.energy = self.max_energy[0]

    def tick_food(self):
        self.food -= self.cons_food
        if self.food < 0:
            self.energy += 1 * self.food
            self.hp += 0.2 * self.food
            self.hp = round(self.hp, 2)
            self.food = 0
        self.food = round(self.food, 2)

    def tick_water(self):
        self.water -= self.cons_water
        if self.water < 0:
            self.energy += 2 * self.water
            self.hp += 0.2 * self.water
            self.hp = round(self.hp, 2)
            self.water = 0
        self.water = round(self.water, 2)

    def tick_energy(self):
        self.energy -= self.cons_energy
        if self.energy < 0:
            self.hp += 0.2 * self.energy
            self.hp = round(self.hp, 2)
            self.energy = 0
        self.energy = round(self.energy, 2)

    def tick(self, grid):
        self.tick_food()
        self.tick_water()
        self.tick_energy()

        if self.food <= 0:
            self.hp = max(self.hp - 2, 0)
        if self.water <= 0:
            self.hp = max(self.hp - 2, 0)
        if self.energy <= 0:
            self.hp = max(self.hp - 2, 0)

        if grid == 1:
            self.underwater_time = max(self.underwater_time - 1, 0)
        else:
            self.underwater_time = self.max_underwater_time[0]

        if self.underwater_time == 0:
            self.hp = max(self.hp - 2, 0)

    def create_new(self):
        cell0 = self.__class__(self.window, self.window_size, self.save_coords[0], self.save_coords[1], self.rect.width, self.rect.height)
        cell0.evolution = self.evolution + 1
        cell0.parent = self.parent
        cell0.genes_init()

        cell0.max_hp = self.max_hp
        cell0.max_food = self.max_food
        cell0.max_water = self.max_water
        cell0.max_energy = self.max_energy

        chance = 0.25

        if random.random() <= chance:
            cell0.max_hp[0] = random.randint(int(cell0.max_hp[0] * 0.9 - 1), int(cell0.max_hp[0] * 1.1 + 1))
        if random.random() <= chance:
            cell0.max_food[0] = random.randint(int(cell0.max_food[0] * 0.9 - 1), int(cell0.max_food[0] * 1.1 + 1))
        if random.random() <= chance:
            cell0.max_water[0] = random.randint(int(cell0.max_water[0] * 0.9 - 1), int(cell0.max_water[0] * 1.1 + 1))
        if random.random() <= chance:
            cell0.max_energy[0] = random.randint(int(cell0.max_energy[0] * 0.9 - 1), int(cell0.max_energy[0] * 1.1 + 1))

        cell0.hp = self.max_hp[0]
        cell0.food = self.max_food[0]
        cell0.water = self.max_water[0]
        cell0.energy = self.max_energy[0]

        for i in range(len(cell0.ai.w) - 1):
            for j in range(len(cell0.ai.w[i + 1])):
                for l in range(len(cell0.ai.w[i])):
                    if random.random() <= 0.01:
                        cell0.ai.w[i][l][j] = random.uniform(0.9, 1.1) * cell0.ai.w[i][l][j] + random.uniform(-1, 1)
                if random.random() <= 0.01:
                    cell0.ai.bias[i][j] = random.uniform(0.9, 1.1) * cell0.ai.bias[i][j] + random.uniform(-1, 1)

        color = [*self.color]
        for i in range(len(color)):
            color[i] = int(random.uniform(0.8, 1.2) * color[i] + random.uniform(-50, 50))
            color[i] = max(min(color[i], 255), 0)
        cell0.color = tuple(color)

        return cell0

    def forward(self, grid, trees, apples):
        inp = [
            self.hp, self.food, self.water, self.energy, self.underwater_time,
            self.max_hp[0], self.max_food[0], self.max_water[0], self.max_energy[0], self.max_underwater_time[0],
            self.cons_food, self.cons_water, self.cons_energy,
            self.rect.x // self.rect.width, self.rect.y // self.rect.height
        ]
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                inp.append(grid[y][x][0])
                inp.append(trees[y][x])
                inp.append(apples[y][x])

        self.ai.forward(inp)

        if grid[self.rect.y // self.rect.height][self.rect.x // self.rect.width][0] != 1:
            self.save_coords = (self.rect.x, self.rect.y)

        res = self.ai.x[-1]
        max0 = max(res)
        if res[0] == max0:
            self.rect.y -= self.rect.height
        elif res[1] == max0:
            self.rect.x += self.rect.width
        elif res[2] == max0:
            self.rect.y += self.rect.height
        elif res[3] == max0:
            self.rect.x -= self.rect.width

        self.rect.x = max(min(self.rect.x, self.window_size[0] - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y, self.window_size[1] - self.rect.height), 0)

        if apples[self.rect.y // self.rect.height][self.rect.x // self.rect.width]:
            apples[self.rect.y // self.rect.height][self.rect.x // self.rect.width] = 0
            self.add_food(10)

        if grid[self.rect.y // self.rect.height][self.rect.x // self.rect.width]:
            self.add_energy(5)

        k = False
        for a in -1, 0, 1:
            for b in -1, 0, 1:
                y = self.rect.y // self.rect.height + a
                x = self.rect.x // self.rect.width + b
                y = max(min(y, self.window_size[1] // self.rect.height - 1), 0)
                x = max(min(x, self.window_size[0] // self.rect.width - 1), 0)
                if grid[y][x]:
                    k = True
        if k:
            self.add_water(5)

    def info(self):
        s = f'hp = {self.hp}/{self.max_hp[0]} ({self.max_hp[1]}-{self.max_hp[2]})\n'
        s += f'food = {self.food}/{self.max_food[0]} ({self.max_food[1]}-{self.max_food[2]}) : {self.cons_food}\n'
        s += f'water = {self.water}/{self.max_water[0]} ({self.max_water[1]}-{self.max_water[2]}) : {self.cons_water}\n'
        s += f'energy = {self.energy}/{self.max_energy[0]} ({self.max_energy[1]}-{self.max_energy[2]}) : {self.cons_energy}\n'
        s += f'underwater_time = {self.underwater_time}/{self.max_underwater_time[0]} ({self.max_underwater_time[1]}-{self.max_underwater_time[2]})\n'
        s += f'parent = {self.parent}\n'
        s += f'evolution = {self.evolution}\n'
        s += f'save_coords = {self.save_coords}'

        return s

    def draw_border(self):
        pygame.draw.rect(self.window, self.border_color, self.rect, self.border)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)
        self.draw_border()

    def collidepoint(self, x, y):
        if self.rect.x <= x <= self.rect.x + self.rect.width:
            if self.rect.y <= y <= self.rect.y + self.rect.height:
                return True
        return False
