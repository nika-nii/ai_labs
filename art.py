import numpy as np
import random


def vec_val(vec):
    return np.count_nonzero(vec)


def run():
    print("Running")
    # Количество векторов признаков
    k = 20
    # Длина векторов
    d = 7
    # Бета, разрушение связи
    B = 1.0
    # Ро, внимательность (размер класса)
    rho = 0.6
    # Сгенерировали векторы признаков
    e = [np.array(gen_e(d)) for _ in range(k)]
    print("Векторы признаков:")
    for v in e:
        print(str_vec(v))
    # Получили начальный вектор-прототип
    p = [e[0].copy()]
    clusters = [
        [e[0]]
    ]

    print("Начальный вектор-прототип:", str_vec(*p))
    for E in e:
        print("Смотрим на вектор", str_vec(E))
        has_joined = False
        num = 0
        for P in p:
            print("Проверяем вектор-прототип", str_vec(P))
            # Похож ли вектор признаков на вектор-прототип?
            # Уравнение схожести (3.2)
            if vec_val(P & E) / (B + vec_val(P)) > vec_val(E) / (B + d):
                print("Вектор похож")
                # Проходит ли тест на внимательность?
                # (3.3)
                if vec_val(P & E) / vec_val(E) > rho:
                    print("Прошел тест на внимательность")
                    # Выполняем слияние прототипа с признаком
                    P &= E
                    print("Теперь прототип", str_vec(P))
                    clusters[num].append(E)
                    has_joined = True
            num += 1
        # Если все прототипы перебрали, но ни к одному не присоединили
        # Создаем новый прототип
        if not has_joined:
            print("Новый прототип", str_vec(E))
            p.append(E.copy())
            clusters.append([E])

    print("Получили кластеры")
    for c in clusters:
        print("{" +
              ",".join((str_vec(v) for v in c))
              + "}")


def gen_e(d=10):
    return np.array([False if random.randint(0, 1) == 0 else True for _ in range(d)])


def str_vec(vec):
    return "".join(map(lambda x: "1" if x else "0", vec))
