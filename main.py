import pygame
import sys
import random
import time

from perlin_noise import PerlinNoise
from parametres import *
from cell import Cell
from area import Area


pygame.init()

window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()


def square(x, y):
    return ((x, y), (x + px, y), (x + px, y + px), (x, y + px))


def triangle(x, y):
    return ((x + px // 2, y), (x + px, y + px), (x, y + px))


def circle(x, y):
    return (x + px // 2, y + px // 2), px // 2 - 1


def f_menu():
    global menu_show

    menu_show = 1 - menu_show


def f_grid():
    global grid_show

    grid_show = 1 - grid_show


def generate_forest():
    global trees

    trees = [[0] * (window_size[0] // px) for i in range(window_size[1] // px)]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            k = True
            for a in -2, -1, 0, 1, 2:
                for b in -2, -1, 0, 1, 2:
                    if 0 <= y + a < len(grid) and 0 <= x + b < len(grid[0]):
                        if trees[y + a][x + b] != 0 or grid[y + a][x + b][0] == 1:
                            k = False
            if k:
                if grid[y][x][0] == 4:
                    if random.random() <= forest_tree_chance / 100:
                        trees[y][x] = 1
                elif grid[y][x][0] == 3:
                    if random.random() <= grass_tree_chance / 100:
                        trees[y][x] = 1
                elif grid[y][x][0] == 2:
                    if random.random() <= sand_tree_chance / 100:
                        trees[y][x] = 1


def start_pause():
    global status

    if status.text == processing_text:
        status.text = pause_text
    elif status.text == pause_text:
        status.text = processing_text


def generate_apples():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if trees[y][x]:
                k = 0
                for a in -1, 0, 1:
                    for b in -1, 0, 1:
                        if 0 <= y + a < len(grid) and 0 <= x + b < len(grid[0]):
                            k += apples[y + a][x + b]
                for a in -1, 0, 1:
                    for b in -1, 0, 1:
                        if 0 <= y + a < len(grid) and 0 <= x + b < len(grid[0]):
                            if k < apples_count and apples[y + a][x + b] == 0 and trees[y + a][x + b] == 0:
                                if random.random() <= apples_chance / 100:
                                    apples[y + a][x + b] = 1
                                    k += 1


def ganerate_field():
    global grid
    global trees
    global apples
    global cells

    grid = []
    trees = []
    apples = []
    cells = []
    for y in range(window_size[1] // px):
        grid.append([])
        trees.append([])
        apples.append([])
        for x in range(window_size[0] // px):
            grid[y].append([0, background_color])
            trees[y].append(0)
            apples[y].append(0)

    noise = PerlinNoise(size=(window_size[0] // px, window_size[1] // px))
    noise.generate()

    for y in range(window_size[1] // px):
        for x in range(window_size[0] // px):
            if noise.arr[y][x] >= forest_threshold:
                grid[y][x] = [4, forest_color]
            elif noise.arr[y][x] >= grass_threshold:
                grid[y][x] = [3, grass_color]
            elif noise.arr[y][x] >= sand_threshold:
                grid[y][x] = [2, sand_color]
            elif noise.arr[y][x] >= water_threshold:
                grid[y][x] = [1, water_color]
            else:
                grid[y][x] = [1, deep_water_color]


def add_cell():
    global cells

    k = True
    while k:
        x = random.randint(0, window_size[0] // px - 1)
        y = random.randint(0, window_size[1] // px - 1)

        if grid[y][x][0] != 1:
            for cell in cells:
                if cell.rect.x == x and cell.rect.y == y:
                    break
            else:
                k = False

    cell = Cell(window, window_size, x * px, y * px, px, px)
    cell.color_init()
    cell.genes_init()
    cells.append(cell)


temp = [
    [('Menu(q)', f_menu), ('Grid(w)', f_grid)],
    [('Start/Pause(t)', start_pause)],
    [('Generate forest(e)', generate_forest)],
    [('Field(a)', ganerate_field)],
    [('Add cell(s)', add_cell)]
]

status = Area(
    window=window,
    x=(window_size[0] - size[0]) - 2 * padding[0] - padding[0],
    y=padding[1],
    width=size[0] + 2 * padding[0],
    height=size[1],
    border_radius=border_radius,
    text=pause_text,
    background_color=background_color,
    border_color=background_color
)

menu = Area(
    window=window,
    x=status.rect.x,
    y=status.rect.y + status.rect.height + 2 + padding[1],
    width=size[0] + 2 * padding[0],
    height=len(temp) * (size[1] + padding[1]) + padding[1],
    border_radius=border_radius,
    background_color=background_color,
    border_color=background_color
)

info = Area(
    window=window,
    x=menu.rect.x,
    y=menu.rect.y + len(temp) * (size[1] + padding[1]) + 2 * padding[1],
    width=menu.rect.width,
    height=150,
    border_radius=border_radius,
    background_color=background_color,
    border_color=background_color
)

btns = []

for i in range(len(temp)):
    n = len(temp[i])
    for j in range(n):
        btn = Area(
            window=window,
            x=menu.rect.x + padding[0] + j * ((size[0] - (n - 1) * padding[0]) // n + padding[0]),
            y=menu.rect.y + padding[1] + i * (padding[1] + size[1]),
            width=(size[0] - (n - 1) * padding[0]) // n,
            height=size[1],
            border_radius=border_radius,
            text=temp[i][j][0]
        )
        btn.clicked = temp[i][j][1]
        btns.append(btn)

cell_time = time.time()
apple_time = time.time()

ganerate_field()
generate_forest()
add_cell()
clicked_cell = cells[0]

while True:

    window.fill(background_color)

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pygame.draw.polygon(window, grid[y][x][1], square(x * px, y * px))
            if trees[y][x]:
                pygame.draw.polygon(window, tree_color, square(x * px, y * px))
            if apples[y][x]:
                pygame.draw.circle(window, apples_color, *circle(x * px, y * px))

    for cell in cells:
        cell.draw()

    if grid_show:
        for x in range(0, window_size[0], px):
            pygame.draw.aaline(window, grid_color, (x, 0), (x, window_size[1]))
        for y in range(0, window_size[1], px):
            pygame.draw.aaline(window, grid_color, (0, y), (window_size[0], y))

    if menu_show:
        status.draw()
        info.draw()
        menu.draw()

        for btn in btns:
            btn.draw()

    if status.text == processing_text and time.time() - cell_time >= cell_tick:
        cell0 = []
        for cell in cells:
            cell.tick(grid[cell.rect.y // cell.rect.height][cell.rect.x // cell.rect.width][0])
            cell.forward(grid, trees, apples)
            if cell.hp > 0:
                cell0.append(cell)
            else:
                cell0.append(cell.create_new())
        cells = cell0

        cell_time = time.time()

    if status.text == processing_text and time.time() - apple_time >= apples_tick:
        generate_apples()

        apple_time = time.time()

    if clicked_cell != None:
        info.text = clicked_cell.info()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu_show:
                for btn in btns:
                    if btn.collidepoint(*event.pos):
                        btn.clicked()

            for cell in cells:
                if cell.collidepoint(*event.pos):
                    clicked_cell = cell

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                f_menu()

            if event.key == pygame.K_w:
                f_grid()

            if event.key == pygame.K_e:
                generate_forest()

            if event.key == pygame.K_t:
                start_pause()

            if event.key == pygame.K_a:
                ganerate_field()

            if event.key == pygame.K_s:
                add_cell()

            if event.key == pygame.K_d:
                cells0 = []
                for cell in cells:
                    cells0 += [cell.create_new()]

                cells += cells0

    clock.tick(fps)
    pygame.display.update()
