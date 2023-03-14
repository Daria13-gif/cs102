import copy
import typing as tp
from random import randint

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480,
                 cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = None

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.grid = copy.deepcopy(self.get_next_generation())

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:  # если значение записываем рандомно, то возвращаем
            # список со значениями в каждой ячейке 0 или 1
            return \
                [[randint(0, 1) for _ in range(self.cell_width)] for __ in range(self.cell_height)]
        else:  # если не рандомно, то возвращаем список из нулей
            return [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x in range(self.cell_width):  # проходим по всему полю
            for y in range(self.cell_height):
                # определяем позицию клетки (начиная с верхней левой клетки поля)
                rect = pygame.Rect(x * self.cell_size,
                                   y * self.cell_size, self.cell_size, self.cell_size)
                # если данное значение в поле равно 1,
                # то красим в зеденый, а если 0, то красим в белый
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        # находим все соседние клетки + проверяем не ушли ли мы за границы поля
        list_neighbours = []
        if cell[0] - 1 >= 0 and cell[1] - 1 >= 0:
            list_neighbours.append(self.cell_width * (cell[0] - 1) + cell[1] - 1)
        if cell[0] - 1 >= 0:
            list_neighbours.append(self.cell_width * (cell[0] - 1) + cell[1])
        if cell[0] - 1 >= 0 and cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.cell_width * (cell[0] - 1) + cell[1] + 1)
        if cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.cell_width * (cell[0]) + cell[1] + 1)
        if cell[1] - 1 >= 0:
            list_neighbours.append(self.cell_width * (cell[0]) + cell[1] - 1)
        if cell[0] + 1 < self.cell_height and cell[1] - 1 >= 0:
            list_neighbours.append(self.cell_width * (cell[0] + 1) + cell[1] - 1)
        if cell[0] + 1 < self.cell_height and cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.cell_width * (cell[0] + 1) + cell[1] + 1)
        if cell[0] + 1 < self.cell_height:
            list_neighbours.append(self.cell_width * (cell[0] + 1) + cell[1])
        return list_neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        # создаем новое поле из 0
        new_grid = [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]
        # обходим все клетки поля
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                # получаем соседей заданной клетки
                list_cells = self.get_neighbours((i, j))
                k = 0
                # обходим соседий и  смотрим является ли сосед живым
                for cell in list_cells:
                    # если живой то увеличиваем к на 1
                    if self.grid[cell // self.cell_width][cell % self.cell_width] == 1:
                        k += 1
                # если соседей 2 или 3, то клетка выживает
                if k == 2 or k == 3:
                    new_grid[i][j] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 40)
    game.run()
