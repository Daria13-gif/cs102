import pathlib
import typing as tp
from math import ceil
from random import randint

T = tp.TypeVar("T")


# Эта функция принимает один аргумент path, который может быть строкой или объектом
# pathlib.Path и представляет собой путь к файлу, содержащему Sudoku.
def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    # Путь path преобразуется в объект pathlib.Path
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    # вызывается функция create_grid(puzzle), которая создает и возвращает сетку Sudoku
    # на основе считанной головоломки, и эта сетка возвращается в качестве результата.
    return create_grid(puzzle)


#  функция принимает один аргумент puzzle, который представляет собой строку, содержащую головоломку Sudoku.
def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
# Внутри функции создается список digits, который содержит все цифры и точки из строки puzzle. 
    # Это делается с помощью генератора списков и проверки наличия символа в допустимых символах для Sudoku
    digits = [c for c in puzzle if c in "123456789."]
# Далее вызывается функция group(digits, 9), которая группирует цифры и точки в список списков (сетку) 
    # размером 9x9 и возвращает эту сетку в качестве результата.
    grid = group(digits, 9)
    return grid


# функция принимает один аргумент grid, который представляет собой сетку Sudoku в виде списка списков строк.
def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    # width устанавливает ширину каждой ячейки в выводе (2 символа)
    width = 2
    # создается строка line, которая представляет собой строку разделителя между блоками в головоломке Sudoku.
    line = "+".join(["-" * (width * 3)] * 3)
    # Этот цикл проходит через каждую строку в сетке Sudoku (всего 9 строк)
    for row in range(9):
        # происходит формирование строки для вывода текущей строки сетки.
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        # выражение проверяет, является ли row (номер текущей строки) равным 2 или 5. 
        # Если это так, то это означает, что нужно добавить строку-разделитель line между блоками Sudoku.
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    # Создаются два пустых списка: sp и grouped. sp будет использоваться для временного хранения элементов, 
    # которые будут добавлены в каждую группу, а grouped будет содержать список из сгруппированных списков.
    sp = []
    grouped = []
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    # Этот цикл перебирает диапазон индексов от 0 до ceil(int(len(values)) / n) - 1.
    # Здесь len(values) определяет общее количество элементов в исходном списке values, 
    # и ceil(int(len(values)) / n) определяет количество групп, которые будут созданы.
    for j in range(ceil(int(len(values)) / n)):
        for i in range(n):
            # элементы из values добавляются в список sp
            sp.append(values[0])
            # После добавления элемента в sp, он удаляется из values с помощью values = values[1:], 
            # чтобы следующий элемент был взят на следующей итерации.
            values = values[1:]
        # добавление в список
        grouped.append(sp)
        # sp очищается, чтобы быть готовым к добавлению элементов следующей группы.
        sp = []

    # функция возвращает список grouped, который содержит сгруппированные списки элементов.
    return grouped


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    # функция возвращает строку, которая находится внутри сетки grid по индексу,
    # указанному в pos[0]. pos[0] - это первый элемент кортежа pos и представляет номер строки, 
    # которую мы хотим получить из сетки.
    return grid[pos[0]]


# функция принимает два аргумента: grid, который должен быть списком списков строк, и pos, 
# который должен быть кортежем из двух целых чисел. Функция возвращает список строк.
# sp = [] - Это создание пустого списка sp, который будет содержать значения из заданного столбца.
def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    sp = []
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    for i in grid:
        # извлекаем значение из текущей строки i, используя индекс pos[1]. pos[1] - это второй
        # элемент кортежа pos и представляет собой номер столбца, который мы хотим получить из сетки. 
        # Полученное значение добавляется в список sp
        sp.append(i[pos[1]])
    return sp


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    # block_size - указывает на размер блока в сетке
    block_size = 3
    # создание пустого списка index, который будет содержать значения из заданного блока
    index = []
    # вычисляется номер строки (row), в которой находится блок, содержащий позицию pos
    row = (pos[0] // block_size) * block_size  # строчка
    # вычисляется номер столбца (col), в котором находится блок, содержащий позицию pos
    col = (pos[1] // block_size) * block_size  # колонка
    # условные проверки используются, чтобы гарантировать, что номер строки и столбца не меньше нуля. 
    # Если они меньше нуля, то они будут установлены в ноль, чтобы не выходить за пределы сетки.
    if row < 0:
        row = 0
    if col < 0:
        col = 0
    # перебор строчек в коде
    for i in range(row, row + block_size):
        # расширяем список index значениями из блока
        # grid[i][col : col + block_size] представляет собой срез сетки, который выбирает значения из блока, 
        # начиная с указанной строки i и столбца col, и заканчивая соответствующими значениями в пределах блока
        index.extend(grid[i][col : col + block_size])
    return index


# функция принимает аргумент grid - двумерный список строк (сетку), и возвращает координаты
# первой пустой (содержащей символ ".") позиции в этой сетке. Если все позиции заполнены (нет пустых), 
# функция возвращает None
def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # выражение проверяет, является ли значение в текущей позиции grid[i][j] равным "." 
            # (то есть, является ли позиция пустой).
            if grid[i][j] == ".":
                # функция возвращает кортеж с координатами этой пустой позиции, где i - номер строки, а j - номер столбца.
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    # создание пустого списка stolbec, который будет использоваться для хранения всех значений в заданном столбце
    stolbec = []
    # список values, который содержит все возможные значения, которые могут быть размещены в сетке.
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # вызов функции get_row, которая возвращает список значений в строке, содержащей позицию pos
    stroka = get_row(grid, pos)
    # вызов функции get_block, которая возвращает список значений в блоке, содержащем позицию pos
    block = get_block(grid, pos)
    # цикл добавляет все значения из заданного столбца (полученного из pos[1]) в список stolbec.
    for i in range(len(grid)):
        stolbec.append(grid[i][pos[1]])
    # Далее следуют циклы for, которые перебирают значения в stroka, stolbec и block.
    # В каждом цикле проверяется, если значение присутствует в списке values, и если оно есть,
    # то оно удаляется из этого списка. Это происходит для того, чтобы исключить из возможных значений те,
    for i in range(len(stroka)):
        if stroka[i] in values:
            values.remove(stroka[i])
    for i in range(len(stolbec)):
        if stolbec[i] in values:
            values.remove(stolbec[i])
    for i in range(len(block)):
        if block[i] in values:
            values.remove(block[i])
    return set(values)


def solve(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    """Поиск решения для указанного пазла.

    Как решать Судоку?
    1. Найти свободную позицию
    2. Найти все возможные значения, которые могут находиться на этой позиции
    3. Для каждого возможного значения:
        3.1. Поместить это значение на эту позицию
        3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # функция вызывает функцию find_empty_positions для поиска первой пустой позиции в сетке grid.
    # Если такая позиция не найдена (pos is None), это означает, что сетка полностью заполнена, 
    # и функция завершает выполнение, возвращая исходную сетку
    pos = find_empty_positions(grid)
    if pos is None:
        return grid
    else:
        # функция вызывает find_possible_values для поиска всех возможных значений, 
        # которые можно разместить в текущей пустой позиции pos.
        values = find_possible_values(grid, pos)
        # Если список values пуст (нет возможных значений для размещения в данной позиции), это означает, 
        # что предыдущие шаги привели к неверному решению, и функция завершает выполнение, возвращая исходную сетку.
        if len(values) == 0:
            return grid
        for i in values:
            # Значение i устанавливается в пустую позицию pos в сетке, 
            # чтобы попробовать это значение для решения задачи.
            grid[pos[0]][pos[1]] = i
            # функция solve вызывается рекурсивно для попытки решения 
            # головоломки с установленным значением i в пустой позиции pos.
            grid = solve(grid)
            # функция проверяет, есть ли ещё пустые позиции в сетке с помощью функции find_empty_positions.
            # если не найдено больше пустых позиций, это означает, что головоломка полностью решена, 
            # и функция завершает выполнение, возвращая сетку с решением.
            if not find_empty_positions(grid):
                return grid
            # Если еще есть пустые позиции, текущее значение i удаляется из пустой позиции pos
            # (возврат к предыдущему состоянию) для дальнейших попыток.
            grid[pos[0]][pos[1]] = "."
        return grid


# функция принимает аргумент solution - двумерный список строк, представляющий решение головоломки Sudoku. 
# Функция проверяет, является ли данное решение верным и возвращает True в случае верного решения и False в противном случае.
def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # перебираем числа от 0 до 8, представляя индексы строк и столбцов в сетке Sudoku.
    for i in range(9):
        # Создается кортеж pos, представляющий координаты позиции в сетке. 
        # В данном случае, pos устанавливается в текущий столбец i и первую строку (номер строки 0).
        pos = (0, i)
        # Вызывается функция get_col, чтобы получить все значения в текущем столбце pos из решения solution.
        proverka = get_col(solution, pos)
        # перебираем числа от 1 до 9 в виде строк.
        for j in "123456789":
            # Для каждого числа j, код проверяет, содержит ли столбец proverka это число.
            # Если оно отсутствует в столбце, это означает, что головоломка не решена правильно, 
            # и функция возвращает False.
            if j not in proverka:
                return False

        # аналогично столбцам, только теперь со строками
        pos = (i, 0)
        proverka = get_row(solution, pos)
        for j in "123456789":
            if j not in proverka:
                return False

        pos = ((i * 3) % 9, (i * 3) // 9)
        proverka = get_block(solution, pos)
        for j in "123456789":
            if j not in proverka:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # создается пустая сетка grid, представляющая собой 9x9 сетку, заполненную точками "."
    grid = [["." for i in range(9)] for j in range(9)]
    # вызывается функция solve, которая заполняет сетку grid решением головоломки Sudoku. 
    # После этого grid будет содержать правильное Sudoku-решение.
    grid = solve(grid)
    # проверяем, не превышает ли значение N максимальное количество чисел в Sudoku
    if N > 81:
        # Если N больше 81, оно устанавливается равным 81, чтобы предотвратить 
        # генерацию слишком большой числа скрытых чисел.
        N = 81
    # цикл для скрытия случайных чисел в сетке. Количество чисел, которые нужно скрыть, 
    # вычисляется как разница между максимальным числом (81) и N.
    for i in range(81 - N):
        # Для каждой итерации цикла выбираются случайные координаты x и y в диапазоне от 0 до 8, 
        # чтобы определить позицию в сетке.
        x, y = randint(0, 8), randint(0, 8)
        # цикл выполняется, пока выбранная позиция grid[x][y] в сетке пуста.
        while grid[x][y] == ".":
            x, y = randint(0, 8), randint(0, 8)
        # Когда найдена непустая позиция (клетка с числом), она заменяется на точку ".", что скрывает число.
        grid[x][y] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
