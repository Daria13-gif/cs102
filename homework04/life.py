import copy
import pathlib
import typing as tp
from random import randint


Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size[0], size[1]

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.cols
        self.cell_height = self.rows

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            # если значение записываем рандомно,
            # то возвращаем список со значениями в каждой ячейке 0 или 1
            return [[randint(0, 1) for _ in range(self.cell_width)]
                    for __ in range(self.cell_height)]
          # если не рандомно, то возвращаем список из нулей
        return [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # находим все соседние клетки + проверяем не ушли ли мы за границы поля
        list_neighbours = []
        if cell[0] - 1 >= 0 and cell[1] - 1 >= 0:
            list_neighbours.append(self.curr_generation[cell[0] - 1][cell[1] - 1])
        if cell[0] - 1 >= 0:
            list_neighbours.append(self.curr_generation[cell[0] - 1][cell[1]])
        if cell[0] - 1 >= 0 and cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.curr_generation[cell[0] - 1][cell[1] + 1])
        if cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.curr_generation[cell[0]][cell[1] + 1])
        if cell[1] - 1 >= 0:
            list_neighbours.append(self.curr_generation[cell[0]][cell[1] - 1])
        if cell[0] + 1 < self.cell_height and cell[1] - 1 >= 0:
            list_neighbours.append(self.curr_generation[cell[0] + 1][cell[1] - 1])
        if cell[0] + 1 < self.cell_height and cell[1] + 1 < self.cell_width:
            list_neighbours.append(self.curr_generation[cell[0] + 1][cell[1] + 1])
        if cell[0] + 1 < self.cell_height:
            list_neighbours.append(self.curr_generation[cell[0] + 1][cell[1]])
        return list_neighbours

    def get_next_generation(self) -> Grid:
        # создаем новое поле из 0
        new_grid = [[0 for _ in range(self.cell_width)] for __ in range(self.cell_height)]
        # обходим все клетки поля
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                # получаем соседей заданной клетки
                list_cells = self.get_neighbours((i, j))
                k = sum(list_cells)
                # если соседей 2 и существо живое или 3, то клетка выживает
                if k == 2 and self.curr_generation[i][j] == 1 or k == 3:
                    new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        # количество поколений увеличиваем на 1
        self.generations += 1
        # в предыдущее поколение записываем нынешнее поколение,
        # а в нынешнее поколение след. поколение
        self.prev_generation, self.curr_generation = \
            copy.deepcopy(self.curr_generation), self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True

        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as file:
            f = file.read().split("\n")
            curr_generation = []
            for i in f:
                a = []
                for j in i:  # идем посторочно и разбиваем нашу строчку на
                    # элементы, превращая их в числа
                    a.append(int(j))
                curr_generation.append(a)
            s = GameOfLife((len(curr_generation),
                            len(curr_generation[0])))
            # создаем объект класса с кол-вом строк и
            # кол-вом столбцов
            s.curr_generation = copy.deepcopy(curr_generation)
            # занчение из файла присваем в переменную curr_generation
            # объекту данного класса
            return s  # возвращаем этот объект

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for i in self.curr_generation:
                # берем каждую строчку их нынешнего поколения и записываем ее в файл
                f.write("".join(map(str, i)) + "\n")

