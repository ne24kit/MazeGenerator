import argparse
from game import start_game
from maze import start_generator, alg_DFS, alg_Prim

class RangeError(Exception):
    pass

def check_range(int_value):
    if 6 <= int_value <= 19:
        return True
    # TODO: translate into English 
    raise RangeError(f"cторона лабиринта должна быть от 6 до 19, a НЕ: {int_value}")

def check(value):
    try:
        int_value = int(value)
        check_range(int_value)
    # TODO: translate into English 
    except ValueError:
        raise argparse.ArgumentTypeError(f"попытайтесь ввести число, а НЕ: {value}")

    except RangeError as e:
        raise argparse.ArgumentTypeError(e)

    return int_value


def play_game(args):
    print("Start game")
    
    match(args.algorithm):
        case "DFS":
            start_game(alg_DFS, args.size[0], args.size[1], args.filename, args.solution, args.players, args.bonuses)
        case "Prim":
            start_game(alg_Prim, args.size[0], args.size[1], args.filename, args.solution, args.players, args.bonuses)

def generator(args):
    print("Start generator")

    match(args.algorithm):
        case "DFS":
            start_generator(alg_DFS, args.size[0], args.size[1], args.solution, args.filename, args.save_maze)
        case "Prim":
            start_generator(alg_Prim, args.size[0], args.size[1], args.solution, args.filename, args.save_maze)

if __name__ == "__main__":
    # TODO: translate into English 
    parser = argparse.ArgumentParser(prog="'maze generator and solver'", description='ОПИСАНИЕ', epilog="Bye")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--size", help="Введите размер лабиринта ширина, высота", nargs=2, type=check, default=[10, 10], metavar=('w', 'h'))
    group.add_argument('-f', "--filename", help="Подгружает уже созданный лабиринт, введите <filename.txt>", type=str)

    parser.add_argument("-a", "--algorithm", help="Выберете алгоритм генерации", type=str, choices=['DFS', 'Prim'], default='DFS')
    parser.add_argument("-sol", "--solution", help="Лабиринт с решением", action='store_true', default=False)
    subparsers = parser.add_subparsers(title='mods', help='Режим работы программы game/generator', required=True)

    parser_game = subparsers.add_parser("game", help="Начинает игру")
    parser_game.add_argument("-p", "--players", help="Количество игроков", type=int, choices=[1, 2], default=1)
    parser_game.add_argument("-b", "--bonuses", help="Игра с бонусами: speed up, speed down, telepot", action='store_true', default=False)
    parser_game.set_defaults(func=play_game)
    
    parser_generator = subparsers.add_parser("generator", help="Режим генерации лабринта")
    parser_generator.add_argument("-sm", "--save_maze", help="Сохранить лабиринт в txt формате", action='store_true')

    parser_generator.set_defaults(func=generator)

    args = parser.parse_args()
    args.func(args)
