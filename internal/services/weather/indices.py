import math

import numpy as np


def calc_ffmc(fo: float, h: float, t: float, w: float, ro: float):
    """
    FFMC (Fine Fuel Moisture Code) - показатель влажности мелких легковоспламеняющихся материалов.
    Оригинальный код на NCL https://github.com/NCAR/fire-indices/blob/master/calc_ffmc.ncl

    :param fo: FFMC предыдущего дня
    :param h: Средняя относительная влажность (%)
    :param t: Средняя температура (градусы Цельсия)
    :param w: Скорость ветра в МИЛЯХ в час (mph). Тут внимательно!
    :param ro: Дневное количество осадков

    :return: Вычисленное значение FFMC
    """

    # Рассчитываем начальное содержание влаги в горючем материале
    mo = 147.2 * (101.0 - fo) / (59.5 + fo)

    # Корректируем влажность с учетом осадков
    rf = np.where(ro > 0.5, ro - 0.5, -1.0)

    # Если были осадки, корректируем значение mo
    if np.any(rf > 0):
        mo = np.where(
            rf > 0,
            np.where(
                mo > 150.0,
                mo + 42.5 * rf * np.exp(-100. / (251.0 - mo)) * (1 - np.exp(-6.93 / rf)) + 0.0015 * ((mo - 150.0) ** 2) * np.sqrt(rf),
                mo + 42.5 * rf * np.exp(-100. / (251.0 - mo)) * (1 - np.exp(-6.93 / rf))
            ),
            mo
        )

    # Рассчитываем равновесное содержание влаги в горючем материале
    ed = 0.942 * h ** 0.679 + 11 * np.exp((h - 100.) / 10.0) + 0.18 * (21.1 - t) * (1 - np.exp(-0.115 * h))
    ew = 0.618 * h ** 0.753 + 10 * np.exp((h - 100.) / 10.0) + 0.18 * (21.1 - t) * (1 - np.exp(-0.115 * h))

    # Рассчитываем скорость высыхания горючего материала
    ko1 = np.where(
        mo > ed,
        0.424 * (1 - (h / 100) ** 1.7) + 0.0694 * np.sqrt(w) * (1 - (h / 100) ** 8.0),
        0.424 * (1 - ((100 - h) / 100) ** 1.7) + 0.0694 * np.sqrt(w) * (1 - ((100 - h) / 100) ** 8.0)
    )

    kdw = ko1 * 0.581 * np.exp(0.0365 * t)

    # Окончательный расчет содержания влаги
    m = np.where(mo > ed, ed + (mo - ed) * 10 ** (-kdw), mo)
    m = np.where(mo < ew, ew - (ew - mo) * 10 ** (-kdw), m)

    # Ограничиваем значение в пределах допустимого диапазона [0, 250]
    m = np.clip(m, 0.0, 250.0)

    return m

def calc_dmc(po: float, t: float, ro: float, h: float, le: float):
    """
    Расчет Duff Moisture Code (DMC) на основе входных параметров.
    Оригинальный код на NCL https://github.com/NCAR/fire-indices/blob/master/calc_dmc.ncl

    :param po: DMC предыдущего дня
    :param t: Температура (градусы Цельсия)
    :param ro: Суточное количество осадков (мм)
    :param h: Средняя относительная влажность (%)
    :param le: Длина дня (количество солнечного света)

    :return: Рассчитанное значение DMC
    """

    # Проверяем, превышает ли температура -1.1
    t_dmc = t > -1.1

    # Корректируем количество осадков
    re = np.where(ro > 1.5, 0.92 * ro - 1.27, 0)

    # Рассчитываем начальное значение влажности торфа
    mo = 20.0 + np.exp(5.6348 - (po / 43.43))

    # Рассчитываем коэффициент b, который зависит от po
    b = 14.0 - 1.3 * np.log(po)
    b = np.where(po > 65., 6.2 * np.log(po) - 17.2, b)
    b = np.where(po < 33., 100. / (0.5 + 0.3 * po), b)

    # Рассчитываем влажность после осадков (если были осадки)
    mr = np.where(re > 0, mo + (1000. * re / (48.77 + b * re)), 0)

    # Обновляем po, если были осадки
    po = np.where(re > 0, 244.72 - 43.43 * np.log(mr - 20.0), po)

    # Убеждаемся, что po не отрицательное
    po = np.maximum(po, 0.0)

    # Рассчитываем коэффициент испарения
    k = 1.894 * (t_dmc + 1.1) * (100 - h) * le * 10**(-6)

    # Итоговый расчет DMC
    p = np.maximum(po + 100 * k, 0.0)

    return p

def calc_dc(ro: float, t: float, do: float, lf: float) -> float:
    """
    Расчет Drought Code (DC)
    Оригинальный код на NCL https://github.com/NCAR/fire-indices/blob/master/calc_dc.ncl

    :param ro: Суточное количество осадков (мм)
    :param t: Температура (градусы цельсия)
    :param do: Значение DC предыдущего дня
    :param lf: Коррекция длины дня

    :return: Рассчитанное значение DC
    """
    # Проверяем, превышает ли температура -2.8
    t_dc: float = float(t > -2.8)

    # Корректируем осадки
    rd: float = 0.83 * ro - 1.27 if ro > 2.8 else -1.0

    # Рассчитываем начальное значение влажности засухи
    qo: float = 800.0 * np.exp(-do / 400.0)

    # Корректируем значение влажности с учетом осадков
    qr: float = qo + (3.937 * rd)

    # Обновляем значение DC, если были осадки
    dr: float = 400.0 * np.log(800.0 / qr) if rd > 0 else do

    # Убеждаемся, что DC не отрицательное
    dr = max(dr, 0.0)

    # Рассчитываем влияние температуры и длины дня
    v: float = (0.36 * (t_dc + 2.8)) + lf
    v = max(v, 0.0)

    # Итоговый расчет DC
    drou: float = max(dr + 0.5 * v, 0.0)

    return drou

def calc_isi(w: float, m: float) -> float:
    """
    Расчет Initial Spread Index (ISI) на основе входных параметров.
    Оригинальный код на NCL https://github.com/NCAR/fire-indices/blob/master/calc_isi.ncl

    :param w: Скорость ветра в МИЛЯХ в час (mph). Тут внимательно!
    :param m: Промежуточное значение из FFMC

    :return: Рассчитанное значение ISI
    """
    # Рассчитываем влияние ветра
    fw: float = np.exp(0.05039 * w)

    # Рассчитываем коэффициент распространения огня
    ff: float = 91.9 * np.exp(-0.1386 * m) * (1 + (m**5.31 / (4.93 * 10**7)))

    # Итоговый индекс ISI (убедимся, что он не отрицательный)
    r: float = max(0.208 * fw * ff, 0.0)

    return r

def calc_bui(p: float, d: float) -> float:
    """
    Расчет Build Up Index (BUI) на основе входных параметров.
    Оригинальный код на NCL https://github.com/NCAR/fire-indices/blob/master/calc_bui.ncl

    :param p: DMC (Duff Moisture Code)
    :param d: DC (Drought Code)

    :return: Рассчитанное значение BUI
    """

    # Если оба значения равны 0, устанавливаем их в NaN (аналог _FillValue в NCL)
    if p == 0.0 and d == 0.0:
        return 0.0  # В NCL это _FillValue, но здесь лучше вернуть 0

    # Рассчитываем промежуточное значение dfour
    dfour: float = 0.4 * d

    # Проверяем, если p или d NaN (например, при обработке данных)
    if np.isnan(p) or np.isnan(d):
        return 0.0  # Если данные отсутствуют, возвращаем 0

    # Основной расчет BUI
    if p > dfour:
        u: float = p - (1.0 - 0.8 * d / (p + dfour)) * (0.92 + (0.0114 * p) ** 1.7)
    else:
        u: float = 0.8 * p * d / (p + dfour) if (p + dfour) != 0 else 0.0  # Защита от деления на 0

    # Убеждаемся, что BUI не становится отрицательным
    return max(u, 0.0)


def calculate_fwi(isi: float, bui: float) -> float:
    """
    Расчет Fire Weather Index (FWI) — Индекса Пожарной Опасности.
    Оригинальный код на из публикации https://publications.gc.ca/collections/collection_2016/rncan-nrcan/Fo133-1-424-eng.pdf

    :param isi: Initial Spread Index (ISI)
    :param bui: Build Up Index (BUI)

    :return: Рассчитанное значение Fire Weather Index (FWI)
    """

    if bui <= 80.0:
        fwi = 0.1 * isi * (0.626 * bui ** 0.809 + 2.0)
    else:
        fwi = 0.1 * isi * (1000.0 / (25.0 + 108.64 / math.exp(0.023 * bui)))

    if fwi > 1.0:
        fwi = math.exp(2.72 * (0.434 * math.log(fwi)) ** 0.647)

    return fwi