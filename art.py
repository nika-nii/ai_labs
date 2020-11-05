import numpy as np
import random


def vec_val(vec):
    return vec.count(True)


def gen_e(d=10):
    return [False if random.randint(0, 1) == 0 else True for _ in range(d)]


def str_vec(vec):
    return "".join(map(lambda x: "1" if x else "0", vec))


def op_and(vec1, vec2):
    return [x1 and x2 for x1, x2 in zip(vec1, vec2)]


def run():
    noisy = False
    # Количество векторов признаков
    k = 20
    # Длина векторов
    d = 7
    # Бета, разрушение связи
    B = 1.0
    # Ро, внимательность (размер класса)
    rho = 0.8
    # Сгенерировали векторы признаков
    e = [gen_e(d) for _ in range(k)]
    print("Векторы признаков:")
    line_cnt = 0
    for v in e:
        if line_cnt > 20:
            print("...")
            break
        print(str_vec(v))
    p = []
    clusters = []
    clusters_changed = True

    while clusters_changed:
        print("Есть изменения, запускаем цикл заново")
        clusters_changed = False
        # Очищаем кластеры
        clusters = [
            [] for _ in p
        ]
        is_in_cluster = [False for _ in e]
        for E in e:
            # Если рассматриваемый вектор признаков - первый,  примем его за вектор-прототип
            if not p:
                # Получили начальный вектор-прототип
                p = [e[0].copy()]
                clusters = [
                    [e[0]]
                ]
                clusters_changed = True
                if noisy:
                    print("Начальный вектор-прототип:", str_vec(*p))
            else:
                if noisy:
                    print("Смотрим на вектор", str_vec(E))
                has_joined = False
                num = 0
                for P in p:
                    if noisy:
                        print("Проверяем вектор-прототип", str_vec(P))
                    # Похож ли вектор признаков на вектор-прототип?
                    # Уравнение схожести (3.2)
                    if vec_val(op_and(P, E)) / (B + vec_val(P)) > vec_val(E) / (B + d):
                        if noisy:
                            print("Вектор похож")
                        # Проходит ли тест на внимательность?
                        # (3.3)
                        if vec_val(op_and(P, E)) / vec_val(E) >= rho:
                            if noisy:
                                print("Прошел тест на внимательность")
                            e_index = e.index(E)
                            if not is_in_cluster:
                                # Выполняем слияние прототипа с признаком
                                if P != E:
                                    clusters_changed = True
                                    P = op_and(P, E)
                                clusters[num].append(E)
                                is_in_cluster[e_index] = True
                                if noisy:
                                    print("Теперь прототип", str_vec(P))
                            has_joined = True
                    num += 1
                # Если все прототипы перебрали, но ни к одному не присоединили
                # Создаем новый прототип
                if not has_joined:
                    if not is_in_cluster[e.index(E)]:
                        if noisy:
                            print("Новый прототип", str_vec(E))
                        p.append(E.copy())
                        clusters.append([E])
    print("Получили кластеры")
    num = 0
    for c in clusters:
        print(str_vec(p[num]) + ":" + "{" +
              ",".join((str_vec(v) for v in c))
              + "}")
        num += 1
