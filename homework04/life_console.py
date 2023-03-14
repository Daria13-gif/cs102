import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.life = life

        self.width = life.cell_width
        self.height = life.cell_height

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width
        self.cell_height = self.height

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        s = "+" + "-" * self.width + "+"  # верхняя и нижняя часть рамки
        screen.addstr(0, 0, str(s))  # отображаем верхнюю часть рамки
        m = "|" + " " * self.width + "|"
        for i in range(1, self.height + 1):  # с помощью цикла отображаем все части рамки кроме верхней и нижней
            screen.addstr(i, 0, str(m))

        screen.addstr(self.height + 1, 0, str(s))  # нижняя часть рамки

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.width):  # идем по всем клеткам нашего поля
            for j in range(self.height):
                if self.life.curr_generation[j][i] == 1:  # если в текущем поколении клетка живая, то рисуем *
                    screen.addch(j + 1, i + 1, "*")

    def run(self) -> None:
        # открываем консоль
        screen = curses.initscr()
        while (
                not self.life.is_max_generations_exceeded and self.life.is_changing
        ): # пока не достигнем заданного кол-ва шагов
            # либо изменился экран
            self.draw_borders(screen)  # рисуем гарницы
            self.draw_grid(screen)  # рисуем поле
            screen.refresh()  # обновляем консоль
            time.sleep(1)  # делаем задержку в 1 сек
            self.life.step()  # делаем след. шаг игры
        screen.addstr(self.height + 2, self.width // 2 - 4, "Game Over")  # если игра закончилась пишет game over
        screen.refresh()
        time.sleep(1)
        curses.endwin()
