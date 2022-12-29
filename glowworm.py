import numpy as np
from random import uniform
from scipy.spatial import distance as dist
import copy

borderPadding = 0.5

# Инициирует начальные позиции светлячков
def starting_points(settings):
    # Сбрасываем счетчик начального значения средних значений фитнесс функции
    global average
    average = 0

    global borderPadding
    # Инициирующий массив светлячков состоит из их координат.
    # Ограничение идет по выбранной фитнесс функции и зазору (бордюру) который светлячки не могут преодолеть для правильного отображения их позиции
    return np.array([[uniform(settings.testFunction.getMinX()+borderPadding, settings.testFunction.getMaxX()-borderPadding),
             uniform(settings.testFunction.getMinX()+borderPadding, settings.testFunction.getMaxX()-borderPadding)] for x in range(settings.populationSize)])


# счетчик начального значения средних значений фитнесс функции
average = 0


# Расчет лучшей позиции
def get_score(pop, settings):
    global average

    # Для каждого светлячка расчитать значение его фитнесс функции
    temp = [ (settings.testFunction.calculateZ(tup[0], tup[1])) for tup in pop ]

    # Скопировать получившийся массив и определить среднее значение фитнесс функций всех светлячков в текущей эпохе
    a = copy.deepcopy(temp)
    a.sort()
    # print("Best: ", a[0])
    average += a[0]
    print("average", average)

    # К значениям фитнесс функций применить спец коэффициенты (люминофор) для расчета светимости
    # Коэффициент нижней границы (lowerBound) смещает границу видимости
    # Коэффициент влияния (influence) рассчитывает на сколько далеко видно светлячка
    normal = [ x + settings.lowerBound for x in temp ]
    return [ x / settings.influence for x in normal ]

# Функция расчета матрицы влияния каждого светляка на каждого с диагональю с нулевыми значениями
def influence_matrix(pop, score, numWorms):

    # Матрица количество_светлячков*количество_светлячков. Все значения нуль
    graph = np.array([np.zeros(numWorms)] * numWorms)

    # По каждой строке светлячков
    for i in range(numWorms):
        # По каждому столбцу светлячков
        for j in range(numWorms):
            # Если светлячок сам с собой, то можно смело ставить 0
            if i == j:
                graph[i][j] = 0
            # Если фукнция равна меньше или равна результату текущиму
            elif dist.euclidean(pop[i], pop[j]) <= score[j]:
                # Функция euclidean просто считает расстояние до светлячка, аналог квадратичной функции, но оптимизированной
                graph[i][j] = dist.euclidean(pop[i], pop[j])
            else:
                continue
    return graph

# Функция расчета следующей эпохи, шагу
def next_turn(pop, score, im, settings):
    # Копирования всех светлячков для не изменения предыдущей популяции
    n_turn = copy.deepcopy(pop)
    # Цикл по всем светлячкам (размеру популяции)
    for i in range(settings.populationSize):
        # Изначально никуда не двигаемся
        x_move = 0
        y_move = 0
        # Цикл по всем соседям текущего светлячка
        for j in range(settings.populationSize):
            # Расчитываем процент светимости (перемещения) к данному соседу исходя из яркости соседа.
            # Если сасед далеко, то не берем его в расчет
            percent_move = 1 - (im[i][j] / score[j]) if im[i][j] != 0 else 0
            # Используем рассчитанный процент перемещения к светлячку учитывая свою светимость и соседа
            # pop[j][0] - Сосед светляк и его позицция по оси X
            # pop[i][0] - Сам светляк и его позиция по оси X
            # score[i], score[j] светимость своя, светимость соседа
            x_move += (pop[j][0] - pop[i][0]) * percent_move / 10 if score[i] > score[j] else 0
            y_move += (pop[j][1] - pop[i][1]) * percent_move / 10 if score[i] > score[j] else 0
        # Джиттер используеся для небольшого перемещения светлячка в случайном направлении чтобы предотвратить преждевременную сходимость
        jitter_x = settings.jitter * np.random.rand() * np.random.randint(-1,2)
        jitter_y = settings.jitter * np.random.rand() * np.random.randint(-1,2)

        # Добавляем влияние случайного перемещения в конечную точку
        n_turn[i][0] += x_move + jitter_x
        n_turn[i][1] += y_move + jitter_y

        # Проверяем на выход за границы диапазона рассчитанных координат светлячка
        n_turn[i][0] = keep_in_bounds(n_turn[i][0], settings.testFunction.getMinX(), settings.testFunction.getMaxX())
        n_turn[i][1] = keep_in_bounds(n_turn[i][1], settings.testFunction.getMinY(), settings.testFunction.getMaxY())
        
    return n_turn


# Функция проверяет границы, если точка не попадает в заданный промежуток, то она перемещается на границу иначе все хорошо
def keep_in_bounds(x, min_x, max_x):
    global borderPadding
    if x < min_x+borderPadding:
        return min_x+borderPadding
    elif x > max_x-borderPadding:
        return max_x-borderPadding
    else:
        return x