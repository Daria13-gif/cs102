from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


# функция создает и возвращает сетку размером rows строк на cols столбцов. (по умолчанию она 15 на 15)
def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    # возвращаем двумерный список, где каждый элемент является строкой или целым числом, объединенными в единый список.
    return [["■"] * cols for _ in range(rows)]


# функция принимает два аргумента: grid - существующую сетку и coord - кортеж с двумя целыми числами,
# представляющими координаты в сетке.
def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    # проверяем, если элемент сетки в заданных координатах (coord[0], coord[1]) не является пробелом (" "),
    # то заменяет его на пробел (" "). Это предполагает, что символ "■" (квадрат) в данной позиции будет удален.
    if grid[coord[0]][coord[1]] != " ":
        grid[coord[0]][coord[1]] = " "
    # Если элемент сетки в заданных координатах - пробел (" "), то
    # Если следующий столбец меньше, чем длина строки в сетке минус 1 (len(grid[0]) - 1),
    # то заменяет элемент в следующем столбце на пробел (" ").
    elif coord[1] + 1 < len(grid[0]) - 1:
        grid[coord[0]][coord[1] + 1] = " "
    # Если предыдущая строка больше 1, то заменяет элемент в предыдущей строке на пробел (" ").
    elif coord[0] - 1 > 1:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


# создаем лабиринт
def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    # оздается сетка с размерами rows строк на cols столбцов, используя функцию create_grid
    grid = create_grid(rows, cols)
    # пустой список empty_cells, который будет содержать координаты пустых ячеек в сетке
    # (т.е., тех ячеек, которые будут доступными проходами в лабиринте).
    empty_cells = []
    # Двойным циклом по строкам и столбцам сетки (через enumerate) проходим по каждой ячейке.
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            # Если координаты текущей ячейки (x, y) обе нечетные, то текущая ячейка становится проходом
            # (значение меняется с "■" на пробел " ").
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                # Координаты текущей ячейки добавляются в список empty_cells,
                # чтобы в дальнейшем использовать эти координаты для генерации лабиринта.
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    # Создается список random_action с двумя значениями: -1 и 1.
    # Это используется для случайного выбора действия в генерации лабиринта.
    random_action = [-1, 1]
    # Для каждой нечетной строки (row_cor) и нечетного столбца (col_cor) в сетке,
    # выбирается случайное действие (-1 или 1).
    for row_cor in range(1, rows - 1, 2):
        for col_cor in range(1, cols - 1, 2):
            action = choice(random_action)
            # Если выбрано действие 1, то
            if action == 1:
                # Если row_cor находится на верхней границе (равен 1), то проверяется, что col_cor + 1
                # не выходит за правую границу (равен cols - 1). Если это так, то действие пропускается (continue).
                if row_cor == 1:
                    if col_cor + 1 == cols - 1:
                        continue
                    remove_wall(grid, (row_cor, col_cor + 1))
                # если col_cor + 1 меньше cols - 1, то стена между текущей ячейкой и ячейкой справа от нее удаляется.
                elif col_cor + 1 < cols - 1:
                    remove_wall(grid, (row_cor, col_cor + 1))
                elif col_cor - 1 <= cols - 1:
                    remove_wall(grid, (row_cor - 1, col_cor))
            # Если выбрано действие -1, то
            else:
                # Если row_cor находится на верхней границе (равен 1), то проверяется, что col_cor + 1
                # не выходит за правую границу (равен cols - 1). Если это так, то действие пропускается (continue).
                if row_cor == 1:
                    if col_cor + 1 == cols - 1:
                        continue
                    remove_wall(grid, (row_cor, col_cor + 1))
                # Иначе, если row_cor + 1 меньше rows - 1, то стена между текущей ячейкой и ячейкой выше нее удаляется.
                elif row_cor + 1 <= rows - 1:
                    remove_wall(grid, (row_cor - 1, col_cor))

    # Этот блок выполняется, если установлен флаг random_exit.
    if random_exit:
        # генерируются случайные координаты x_in, x_out, y_in и y_out в пределах границ сетки.
        # При этом внимание уделяется тому, чтобы точка входа и точка выхода не находились на углах лабиринта.
        # Точки входа и выхода обозначаются символом "X" в сетке.
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    # генерируются случайные координаты x_in, x_out, y_in и y_out в пределах границ сетки.
    # При этом внимание уделяется тому, чтобы точка входа и точка выхода не находились на углах лабиринта.
    # Точки входа и выхода обозначаются символом "X" в сетке.
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    # функция возвращает сгенерированный лабиринт в виде двумерного списка, в котором символы "■" представляют стены,
    # символы " " представляют проходы, а символы "X" обозначают точки входа и выхода из лабиринта.
    return grid


# функция используется для определения координат точек входа и выхода из лабиринта на основе переданной сетки. 
def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    # пустой список ans, который будет содержать координаты точек входа и выхода из лабиринта.
    ans = []
    # Вычисляются количество строк и столбцов в сетке и сохраняются в переменных rows и columns.
    rows = len(grid) - 1
    columns = len(grid[0]) - 1

    # поиск точек входа и выхода:
    # проверяются все ячейки в верхней строке сетки (строка 0). Если какая-либо из них содержит символ "X",
    # то координата этой ячейки добавляется в список ans. Таким образом, мы ищем точки входа в лабиринт.
    for i in range(columns):
        if grid[0][i] == "X":
            ans.append((0, i))
    # проверяются все ячейки в левом столбце сетки (столбец 0). Если какая-либо из них содержит символ "X",
    # то соответствующая координата добавляется в список ans.
    for i in range(rows):
        if grid[i][0] == "X":
            ans.append((i, 0))

    # если в списке ans есть не менее двух координат, выполняется дополнительная проверка:
    if len(ans) != 2:
        for i in range(columns):
            if grid[rows][i] == "X":
                ans.append((rows, i))
        for i in range(rows):
            if grid[i][columns] == "X":
                ans.append((i, columns))
    # Если в списке ans есть более одной координаты, то проверяется их порядок, чтобы убедиться,
    # что первая точка (вход) находится левее и выше второй точки (выхода).
    # Если это не так, то координаты переставляются местами, чтобы исправить порядок.
    if len(ans) > 1:
        if ans[0][1] > ans[1][1]:
            ans[0], ans[1] = ans[1], ans[0]
        if ans[0][0] > ans[1][0]:
            ans[0], ans[1] = ans[1], ans[0]

    # возвращается список ans, который содержит координаты точек входа и выхода из лабиринта.
    return ans


# Функция make_step принимает сетку grid и число k
def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    # список moves, который содержит все возможные шаги влево, вправо, вверх и вниз.
    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    # список to_visit, который будет содержать координаты ячеек, которые нужно посетить на следующем шаге.
    # Каждая координата представляется кортежем (i, j, k + 1), где (i, j) - координаты ячейки,
    # а k + 1 - значение, на которое нужно увеличить k при проходе через эту ячейку.
    to_visit = []

    # проходимся по всей сетке:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Если значение в текущей ячейке равно k, то добавляем (i, j, k + 1) в список to_visit.
            # Это означает, что на следующем шаге мы будем искать ячейки со значением k + 1
            # и таким образом расширять маршрут.
            if grid[i][j] == k:
                to_visit.append((i, j, k + 1))
    # пока список to_visit не станет пустым:
    while to_visit != []:
        # Извлекаем первый элемент (i, j, k) из to_visit.
        i, j = to_visit[0][0], to_visit[0][1]
        # Для каждого направления из списка moves проверяем, можно ли сделать шаг:
        for x, y in moves:
            # Проверяем, что новые координаты (i + x, j + y) остаются в пределах сетки (0 <= i + x < len(grid)
            # и 0 <= j + y < len(grid[0])).
            if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
                # Проверяем, что значение в новой ячейке grid[i + x][j + y] равно 0, что означает,
                # что это проход (пустая ячейка).
                if grid[i + x][j + y] == 0:
                    # Если условия выполняются, то обновляем значение в ячейке grid[i + x][j + y] на k
                    # и добавляем новую координату (i + x, j + y, k) в список to_visit.
                    grid[i + x][j + y] = to_visit[0][2]
        to_visit.pop(0)
    # функция возвращает обновленную сетку grid.
    return grid


# Функция shortest_path принимает сетку grid и координаты точки выхода exit_coord
def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    # Извлекаем координаты x и y из exit_coord.
    x = exit_coord[0]
    y = exit_coord[1]
    # Получаем значение k из сетки grid в координатах (x, y).
    # Это значение будет равно длине кратчайшего пути от точки входа до точки выхода.
    k = grid[x][y]
    # список moves, который содержит все возможные шаги влево, вправо, вверх и вниз.
    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    # список way, который будет содержать координаты точек пути от выхода к входу.
    # Начинает с добавления координат (x, y) в список way.
    way = []
    way.append((x, y))
    # до тех пор, пока k не станет равным 1 (пока не достигнута точка входа):
    while k != 1:
        # Для каждого направления из списка moves проверяем, можно ли сделать шаг:
        for a, b in moves:
            # Проверяем, что новые координаты (x + a, y + b) остаются в пределах сетки (0 <= x + a < len(grid)
            # и 0 <= y + b < len(grid[0])).
            if 0 <= x + a < len(grid) and 0 <= y + b < len(grid[0]):
                # Извлекает значение temp из сетки в новых координатах (x + a, y + b).
                # temp - это временная переменная, в которой проверяется,
                # можно ли сделать шаг при поиске кратчайшего пути в функции shortest_path.
                temp = grid[x + a][y + b]
                # Если temp является целым числом и это число меньше k, то обновляет x и y на новые
                # координаты (x + a, y + b), добавляет их в список way и обновляет k на значение temp.
                if isinstance(temp, int):
                    if temp < int(k):
                        x, y = x + a, y + b
                        way.append((x, y))
                        k = grid[x][y]

    # проходим по всей сетке и заменяет все значения, которые не являются стенами ("■"), на пробелы (" ").
    for i in range(len(grid) - 1):
        for j in range(len(grid[0])):
            if grid[i][j] != "■":
                grid[i][j] = " "

    # Возвращаем список way, который представляет собой координаты точек пути от выхода к входу,
    # или None, если путь не найден (если k не стал равным 1).
    return way


# Функция принимает сетку grid и координату coord, и возвращает булевое значение,
# указывающее, находится ли точка выхода (coord) внутри или за пределами окружения стен лабиринта.
def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    # инициализируется переменная ans с значением False, которое будет возвращено в конце функции.
    ans = False

    # производится проверка различных условий для определения,
    # находится ли точка coord внутри или за пределами лабиринта.
    # Если coord равно одной из четырех угловых точек сетки,
    # то ans устанавливается в True, так как точка находится на грани лабиринта.
    if (
        coord == (0, 0)
        or coord == (len(grid) - 1, len(grid[0]) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (0, len(grid[0]) - 1)
    ):
        ans = True
    # если coord находится на верхней грани (строка 0), и ячейка под ней (grid[1][coord[1]])
    # не является проходом (" "), то ans устанавливается в True, так как точка находится на грани лабиринта.
    # Аналогичные проверки выполняются для левой грани, правой грани и нижней грани лабиринта.
    elif coord[0] == 0:
        if grid[1][coord[1]] != " ":
            ans = True

    elif coord[1] == 0:
        if grid[coord[0]][1] != " ":
            ans = True

    elif coord[0] == len(grid) - 1:
        if grid[len(grid) - 2][coord[1]] != " ":
            ans = True

    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][len(grid[0]) - 2] != " ":
            ans = True
    # возвращаем значение ans, которое будет True, если точка выхода находится внутри лабиринта,
    # и False, если точка выхода находится на грани лабиринта.
    return ans


# Функция принимает сетку grid и выполняет решение лабиринта, возвращая обновленную сетку и кратчайший путь.
def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    # получаем координаты всех точек выхода из лабиринта с помощью функции get_exits.
    exits = get_exits(grid)
    # Если количество точек выхода меньше 2, то возвращается сетка и одна из точек выхода как решение.
    if len(exits) < 2:
        return grid, exits[0]
    # если в лабиринте есть две точки выхода, то выполняется проверка для каждой из них с использованием функции encircled_exit.
    # Если хотя бы одна из точек выхода находится внутри лабиринта, то возвращается None, None,
    # что указывает на то, что лабиринт не решаем.
    else:
        for exit in exits:
            if encircled_exit(grid, exit):
                return None, None  # type: ignore
    # В противном случае, выбирается одна точка входа enter и одна точка выхода exit из списка exits.
    enter = exits[0]
    exit = exits[1]
    # проверяется, находятся ли точки входа и выхода на соседних ячейках.
    # Если это так, то возвращается сетка и обратно отсортированный список точек выхода,
    # что означает, что лабиринт уже решен.
    if exit[1] - enter[1] == 1 and exit[0] - enter[0] == 0:
        return grid, exits[::-1]
    elif exit[1] - enter[1] == 0 and exit[0] - enter[0] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 0 and exit[1] - enter[1] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 1 and exit[1] - enter[1] == 0:
        return grid, exits[::-1]

    # В противном случае, точка входа enter помечается значением 1 (grid[exits[0][0]][exits[0][1]] = 1).
    # Затем сетка обновляется, заменяя все пробелы (" ") и символы "X" на 0.
    grid[exits[0][0]][exits[0][1]] = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " ":
                grid[i][j] = 0
            elif grid[i][j] == "X":
                grid[i][j] = 0

    # Выполняется поиск кратчайшего пути в лабиринте с помощью функции make_step и shortest_path.
    # Итерации продолжаются до тех пор, пока значение в точке выхода exit не станет равным 1.
    k = 1
    while grid[exits[1][0]][exits[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1

    # Найденный кратчайший путь сохраняется в переменной path.
    # Возвращается сетка grid после поиска пути и сам путь path.
    path = shortest_path(grid, exits[1])

    return grid, path


# функция принимает сетку grid и кратчайший путь path
# и обновляет сетку, добавляя символы "X" в ячейки, через которые проходит кратчайший путь.
def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    # если существует кратчайший путь
    if path:
        # проходим по всем ячейкам сетки grid
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                # если находится текущая координата (i, j) в списке path.
                if (i, j) in path:
                    # значение в соответствующей ячейке сетки grid[i][j] обновляется на символ "X".
                    # Это означает, что ячейка принадлежит кратчайшему пути, и она будет обозначена символом "X".
                    grid[i][j] = "X"
    # функция возвращает обновленную сетку grid, в которой ячейки,
    # принадлежащие кратчайшему пути, помечены символом "X".
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
