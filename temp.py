import random


class Seeds:
    def __init__(self, min0=5, max0=7):
        self.min0 = min0
        self.max0 = max0
        self.seeds = []
        self.create()

    def create(self):
        degree = random.randint(self.min0, self.max0)
        for i in range(degree):
            self.seeds += [Seed(degree=i + 1)]

    def f(self, x, y):
        z = 0
        for i in range(len(self.seeds)):
            z += self.seeds[i].f(x, y)
        z /= len(self.seeds)

        return int(z)


class Seed:
    def __init__(self, min0=-10, max0=10, degree=4):
        self.min0 = min0
        self.max0 = max0
        self.degree = degree
        self.kx = []
        self.ky = []
        self.kxy = []
        self.k = 0
        self.create()

    def create(self):
        self.kx = [0] * self.degree
        self.ky = [0] * self.degree
        self.kxy = [[0] * self.degree for i in range(self.degree)]

        self.k = random.randint(self.min0, self.max0)

        for i in range(self.degree):
            self.kx[i] = random.randint(self.min0, self.max0)
            if random.random() <= 0.5:
                self.kx[i] = 0
            self.ky[i] = random.randint(self.min0, self.max0)
            if random.random() <= 0.5:
                self.ky[i] = 0

        for i in range(self.degree):
            for j in range(self.degree):
                self.kxy[i][j] = random.randint(self.min0, self.max0)
                if random.random() <= 0.7:
                    self.kxy[i][j] = 0

    def to_str(self):
        seed = f'{self.degree}:'
        seed += ':'.join(list(map(str, self.kx))) + ':'
        seed += ':'.join(list(map(str, self.ky))) + ':'
        for i in range(self.degree):
            seed += ':'.join(list(map(str, self.kxy[i]))) + ':'

        seed += f'{self.k}'

        return seed

    def from_str(self, seed):
        seed = list(map(int, seed.split(':')))
        self.degree = seed[0]
        self.k = seed[-1]
        self.kx = seed[1: 1 + self.degree]
        self.ky = seed[1 + self.degree: 1 + 2 * self.degree]
        self.kxy = []
        for i in range(self.degree):
            self.kxy += [seed[1 + 2 * self.degree + i * self.degree: 1 + 3 * self.degree + i * self.degree]]

    def f(self, x, y):
        z = self.k

        for i in range(self.degree):
            z += self.kx[i] * (x ** (i + 1))
            z += self.ky[i] * (y ** (i + 1))

        for i in range(self.degree):
            for j in range(self.degree):
                z += self.kxy[i][j] * (x ** (i + 1)) * (y ** (j + 1))

        return int(z)

    def print(self):
        s = ''
        for i in range(len(self.kx)):
            if self.kx[i] != 0:
                s += f'{int(self.kx[i])}x^{i + 1} + '

        for i in range(len(self.ky)):
            if self.ky[i] != 0:
                s += f'{int(self.ky[i])}y^{i + 1} + '

        for i in range(len(self.kxy)):
            for j in range(len(self.kxy[0])):
                if self.kxy[i][j] != 0:
                    s += f'{int(self.kxy[i][j])}x^{i + 1}y^{j + 1} + '

        s += f'{int(self.k)}'

        print(s)


def format(data):
    data = data.replace('\n', '')
    data = data.replace(', ', ',')

    index = 0
    tabs = 0

    for i in data[::]:
        if i == '{':
            tabs += 1
            data = data[:index] + '{\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == ',':
            data = data[:index] + ',\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == '}':
            tabs -= 1
            data = data[:index] + '\n' + tabs * \
                4 * ' ' + '}' + data[index + 1:]
            index += 1 + tabs * 4
        if i == '[':
            tabs += 1
            data = data[:index] + '[\n' + tabs * 4 * ' ' + data[index + 1:]
            index += 1 + tabs * 4
        if i == ']':
            tabs -= 1
            data = data[:index] + '\n' + tabs * \
                4 * ' ' + ']' + data[index + 1:]
            index += 1 + tabs * 4
        index += 1

    data = data.replace("'", '"')

    return data


def save(name=1):
    with open(f'{sys.path[0]}\\{name}.json', 'w', encoding='utf-8') as file:
        data = {'grid': grid}
        data = str(data)
        data = format(data)
        file.write(data)


def load(name=1):
    with open(f'{sys.path[0]}\\{name}.json', 'r', encoding='utf-8') as file:
        data = file.read()
        data = eval(data)
        global grid
        grid = data['grid']


def fill_grass():
    global grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x][0] == 0:
                grid[y][x] = ['grass', f_color(grass_color)]


def re_color():
    global grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            match grid[y][x][0]:
                case 'water':
                    grid[y][x][1] = f_color(water_color)
                case 'grass':
                    grid[y][x][1] = f_color(grass_color)
                case 'sand':
                    grid[y][x][1] = f_color(sand_color)


def f_color(color):
    color = [*color]
    alpha = random.uniform(0.85, 1.2)
    for i in range(len(color)):
        color[i] = int(alpha * color[i])
        color[i] = max(color[i], 0)
        color[i] = min(color[i], 255)

    return color


def normalize(x, max0, min0, max1=1, min1=0):
    return (max1 - min1) * (x - min0) / (max0 - min0) + min1
