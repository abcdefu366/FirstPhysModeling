import numpy as np # для операций над векторами
import math as mt # для математических операций
import matplotlib.pyplot as plt # для построения графиков

# функция, осуществляющая наполнение массива углами от 0 до 360
def angles_appender(Angles):
    for i in range(360):
        Angles.append(i)

# функция, осуществляющая наполнение массива нулевыми значения для дальнейшей записи значений энергии шаров
def e_appender(E):
    for j in range(3):
        E1 = []
        for i in range(360):
            E1.append(0)
        E.append(E1)

# функция, осуществляющая построение графика зависимости энергии изначально покоящегося шара от угла удара
def plotter(Angles, E):
    plt.figure()
    plt.plot(Angles, E[0], 'o-r', label="µ1 = 0.01", lw=1)
    plt.plot(Angles, E[1], 'o-b', label="µ2 = 0.05", lw=1)
    plt.plot(Angles, E[2], 'o-g', label="µ3 = 0.1", lw=1)
    plt.xlabel('Угол α (град)')
    plt.ylabel('Энергия шара Е (Дж)')
    plt.legend()
    plt.grid(True)
    plt.show()

# функция, осуществляющая вычисление столкновений шаров и подчёт их энергий
def collusions_calculator(V0, V2, x1, y1, t, n1, g, x2, y2, x0, y0, E, k, i, m, r, Lx, Ly, R):
    # вспомогательные переменные для расчетов и рассмотрения всех возможных случаев
    angle1 = round(mt.radians(i), 5)
    angle2 = 0
    l = 0
    q = 0
    w = 0
    p = 0
    b = 0
    Vy0 = round(V0 * mt.sin(angle1), 3)
    Vx0 = round(V0 * mt.cos(angle1), 3)
    Vx2 = 0
    Vy2 = 0
    while (V0 > 0) or (V2 > 0): # выполняется до остановки одного из шаров
        if V0 > 0:
            if Vx0 != 0:
                x1 = x1 + Vx0 * t # вычисление координаты Х шара, по которому бьют
            if Vy0 != 0:
                y1 = y1 + Vy0 * t # вычисление координаты У шара, по которому бьют
            V0 = V0 - (n1 * g * t)
            if angle1 == 0 or angle1 == round(mt.radians(180), 5) or angle1 == round(mt.radians(270), 5) or angle1 == round(mt.radians(90), 5):
                if angle1 == 0 or angle1 == round(mt.radians(180), 5):
                    Vy0 = 0
                    if angle1 == 0:
                        Vx0 = V0
                    else:
                        Vx0 = -V0
                else:
                    Vx0 = 0
                    if angle1 == round(mt.radians(90), 5):
                        Vy0 = V0
                    else:
                        Vy0 = -V0
            else:
                Vx0 = round(V0 * mt.cos(angle1), 3)
                Vy0 = round(V0 * mt.sin(angle1), 3)
            if V0 < 0:
                V0 = 0
                Vx0 = 0
                Vy0 = 0
        if V2 > 0:
            if Vx2 != 0:
                x2 = x2 + Vx2 * t
            if Vy2 != 0:
                y2 = y2 + Vy2 * t
            V2 = V2 - (n1 * g * t)
            Vx2 = round(V2 * mt.cos(angle2), 3)
            Vy2 = round(V2 * mt.sin(angle2), 3)
            if V2 < 0:
                V2 = 0
                Vx2 = 0
                Vy2 = 0
        if mt.sqrt(mt.pow((x1 - x0), 2) + mt.pow((y1 - y0), 2)) <= R:
            V0 = 0
            x1 = x0
            y1 = y0
        if mt.sqrt(mt.pow((x2 - x0), 2) + mt.pow((y2 - y0), 2)) <= R:
            E[k][i] = m * V2 * V2 / 2.0
            V2 = 0
            V0 = 0
            continue # так как энергия вычислена, можно завершать выполнение цикла while
        if ((x1 + r) >= Lx or (x1 - r) <= 0) and w == 0:
            Vx0 = -Vx0
            angle1 = round(mt.radians(180) - angle1, 5)
            w = 1
        else:
            w = 0
        if ((y1 + r) >= Ly or (y1 - r) <= 0) and p == 0:
            Vy0 = -Vy0
            angle1 = round(angle1 - mt.radians(180), 5)
            p = 1
        else:
            p = 0
        if ((x2 + r) >= Lx or (x2 - r) <= 0) and q == 0:
            Vx2 = -Vx2
            angle2 = round(mt.radians(180) - angle2, 5)
            q = 1
        else:
            q = 0
        if ((y2 + r) >= Ly or (y2 - r) <= 0) and b == 0:
            Vy2 = -Vy2
            angle2 = round(angle2 - mt.radians(180), 5)
            b = 1
        else:
            b = 0
        if mt.sqrt(mt.pow((x1 - x2), 2) + mt.pow((y1 - y2), 2)) <= (2 * r) and l == 0:
            en = np.array([round((x2 - x1) / (2 * r), 3), round((y2 - y1) / (2 * r), 3)])
            et = np.array([round((y1 - y2) / (2 * r), 3), round((x2 - x1) / (2 * r), 3)])
            Vvect = np.array([Vx0, Vy0])
            V2vect = np.array([Vx2, Vy2])
            Vvect = (round(np.dot(V2vect, en), 3) * en) + (round(np.dot(Vvect, et), 3) * et)
            V2vect = (round(np.dot(np.array([Vx0, Vy0]), en), 3) * en) + (round(np.dot(V2vect, et), 3) * et)
            Vx0 = round(Vvect[0], 3)
            Vy0 = round(Vvect[1], 3)
            Vx2 = round(V2vect[0], 3)
            Vy2 = round(V2vect[1], 3)
            V0 = round(np.linalg.norm(Vvect), 3)
            V2 = round(np.linalg.norm(V2vect), 3)
            if V0 != 0:
                angle1 = round(mt.acos(round((Vx0 / V0), 3)), 5)
            else:
                Vx0 = 0
                Vy0 = 0
                angle1 = 0
            if V2 != 0:
                angle2 = round(mt.acos(round((Vx2 / V2), 3)), 5)
            else:
                Vx2 = 0
                Vy2 = 0
                angle2 = 0
            l = 1
        else:
            l = 0