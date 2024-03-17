# Генератор лабиринтов

## Описание проекта
Данный проект направлен на создание программы на Python, которая будет генерировать случайные лабиринты c решением.

## Реализуемый функционал
### Базовый функционал:
- Изначально лабиринт будет представлять собой матрицу из стен - "1" и клеток - "0"
- Генерация с помощью DFS или минимального остовного дерева (поддержка обоих вариантов)
- Вариант генерации выбирается с помощью аргумента командной строки 
- Отображение лабиринтов в консоли с помощью специальных символов 
- Сохранение/загрузка лабиринтов в/из файлов
- Решение лабиринтов и отображение пути.

### Дополнительный функционал:
- Более сложные алгоритмы генерации
- Графический интерфейс
- Возможность пользователю самому проходить лабиринт
- Возможность проходить лабиринт в мультиплеерном режиме (можно разделить экран на две части, а можно в одном лабиринте блуждать двумя героями


## Архитектура
1. **Класс MazeGenerator**
- Метод `generate_maze(size, complexity)`: генерация лабиринта заданного размера и сложности.
- Метод `visualize_maze()`: визуализация сгенерированного лабиринта.

2. **Класс Maze**
- Атрибуты: размер лабиринта, алгоритм генерации.
- Метод `save_maze_to_file`: сохранение лабиринта в файл.
- Метод `display`: вывод в консоль
- Метод `upload`: загрузка готового лабиринта из файла.
- Метод `solve`: решение лабринта, показ пути

3. **Класс Cell**
- Атрибуты: координаты (x, y), status (посещена ли клетка), словарь стен клетки (left, up, down, right)
- Метод `get_status`: если клетка посещенна алгоритмом то она нулевая, иначе 1
- Meтод `del_side`: удаляет стену то есть меняет значение в словаре стен с `True` на `False`

4. **Функция alg_Prim**
- Для каждой ячейки создайте набор, каждый из которых будет содержать только эту одну ячейку.
- Для каждой стены в некотором случайном порядке:
- - Если клетки, разделенные этой стеной, принадлежат к разным наборам:
- - Удалим текущую стену.
- - Объединим множества ранее разделенных клеток.

5. **Функция alg_DFS**
- Выберите начальную ячейку, пометьте ее как посещенную и поместите в стек.
- Пока стек не пуст:
- - Вытащите ячейку из стека и сделайте ее текущей.
- - Если у текущей клетки есть соседи, которые не были посещены
- - - Переместите текущую ячейку в стек
- - - Выберите одного из непосещенных соседей
- - - Удалите стену между текущей клеткой и выбранной клеткой
- - - Пометьте выбранную клетку как посещенную и переместите ее в стек 