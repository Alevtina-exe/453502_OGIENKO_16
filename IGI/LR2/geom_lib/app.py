import os
import sys
from geometric_lib.circle import area as circle_area, perimeter as circle_perimeter
from geometric_lib.square import area as square_area, perimeter as square_perimeter

def main():
    # Получаем данные из переменных окружения
    figure = os.getenv('FIGURE_TYPE')
    param1 = os.getenv('PARAM1')
    param2 = os.getenv('PARAM2') # Для прямоугольника, но в вашей библиотеке его нет

    if not figure or not param1:
        print("Ошибка: Не указаны переменные окружения FIGURE_TYPE и PARAM1")
        sys.exit(1)

    try:
        param1 = float(param1)
    except ValueError:
        print("Ошибка: PARAM1 должно быть числом")
        sys.exit(1)

    print(f"Вычисляем параметры для: {figure}")
    
    if figure == 'circle':
        r = param1
        print(f"Радиус круга: {r}")
        print(f"Площадь круга: {circle_area(r)}")
        print(f"Длина окружности: {circle_perimeter(r)}")
    elif figure == 'square':
        a = param1
        print(f"Сторона квадрата: {a}")
        print(f"Площадь квадрата: {square_area(a)}")
        print(f"Периметр квадрата: {square_perimeter(a)}")
    else:
        print(f"Ошибка: Неизвестный тип фигуры '{figure}'. Допустимо: circle, square")
        sys.exit(1)

if __name__ == "__main__":
    main()