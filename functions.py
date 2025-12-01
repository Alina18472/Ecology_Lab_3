#functions.py
import numpy as np

def pend(x, C, faks, f, xm, t=0.0):
    """
    Система дифференциальных уравнений для модели потерь от загрязнения атмосферы
    x = [Cf1, Cf2, Cf3, Cf4, Cf5] - потери (нормированные от 0 до 1)
    C - концентрация загрязняющих веществ (нормированная от 0 до 1)
    t - время (для возмущений x1-x6)
    faks - матрица коэффициентов возмущений [14 x 4]
    f - матрица коэффициентов внутренних функций [12 x 5]
    xm - масштабирующие коэффициенты (максимальные значения)
    
    Уравнения взяты из раздела 6.2 документа:
    dCf1/dC, dCf2/dC, dCf3/dC, dCf4/dC, dCf5/dC
    """
    eps = 1e-4
    x_safe = np.clip(x, eps, 1.0 - eps)
    
    # === ВОЗМУЩЕНИЯ x1-x6 (зависят от времени t) ===
    # Используем полином 3-й степени от времени: a*t³ + b*t² + c*t + d
    if len(faks) > 0:
        x1 = fx_poly3(t, faks[0])
    else:
        x1 = 0.0
    
    if len(faks) > 1:
        x2 = fx_poly3(t, faks[1])
    else:
        x2 = 0.0
    
    if len(faks) > 2:
        x3 = fx_poly3(t, faks[2])
    else:
        x3 = 0.0
    
    if len(faks) > 3:
        x4 = fx_poly3(t, faks[3])
    else:
        x4 = 0.0
    
    if len(faks) > 4:
        x5 = fx_poly3(t, faks[4])
    else:
        x5 = 0.0
    
    if len(faks) > 5:
        x6 = fx_poly3(t, faks[5])
    else:
        x6 = 0.0
    
    # === ВОЗМУЩЕНИЯ x7-x14 (зависят от концентрации C) ===
    # Используем полином 3-й степени от концентрации: a*C³ + b*C² + c*C + d
    if len(faks) > 6:
        x7 = fx_poly3(C, faks[6])
    else:
        x7 = 0.0
    
    if len(faks) > 7:
        x8 = fx_poly3(C, faks[7])
    else:
        x8 = 0.0
    
    if len(faks) > 8:
        x9 = fx_poly3(C, faks[8])
    else:
        x9 = 0.0
    
    if len(faks) > 9:
        x10 = fx_poly3(C, faks[9])
    else:
        x10 = 0.0
    
    if len(faks) > 10:
        x11 = fx_poly3(C, faks[10])
    else:
        x11 = 0.0
    
    if len(faks) > 11:
        x12 = fx_poly3(C, faks[11])
    else:
        x12 = 0.0
    
    if len(faks) > 12:
        x13 = fx_poly3(C, faks[12])
    else:
        x13 = 0.0
    
    if len(faks) > 13:
        x14 = fx_poly3(C, faks[13])
    else:
        x14 = 0.0
    
    # === ВНУТРЕННИЕ ФУНКЦИИ ===
    # f1(Cf3) до f12(Cf1) - полиномы 4-й степени
    f_vals = []
    for i in range(12):
        if i < len(f):
            # Для каждой функции берем коэффициенты и вычисляем значение
            if i == 0:  # f1(Cf3)
                f_vals.append(fx_poly4(x_safe[2], f[i]))
            elif i == 1:  # f2(Cf4)
                f_vals.append(fx_poly4(x_safe[3], f[i]))
            elif i == 2:  # f3(Cf5)
                f_vals.append(fx_poly4(x_safe[4], f[i]))
            elif i == 3:  # f4(Cf3)
                f_vals.append(fx_poly4(x_safe[2], f[i]))
            elif i == 4:  # f5(Cf4)
                f_vals.append(fx_poly4(x_safe[3], f[i]))
            elif i == 5:  # f6(Cf5)
                f_vals.append(fx_poly4(x_safe[4], f[i]))
            elif i == 6:  # f7(Cf5)
                f_vals.append(fx_poly4(x_safe[4], f[i]))
            elif i == 7:  # f8(Cf1)
                f_vals.append(fx_poly4(x_safe[0], f[i]))
            elif i == 8:  # f9(Cf2)
                f_vals.append(fx_poly4(x_safe[1], f[i]))
            elif i == 9:  # f10(Cf3)
                f_vals.append(fx_poly4(x_safe[2], f[i]))
            elif i == 10:  # f11(Cf5)
                f_vals.append(fx_poly4(x_safe[4], f[i]))
            elif i == 11:  # f12(Cf1)
                f_vals.append(fx_poly4(x_safe[0], f[i]))
        else:
            f_vals.append(0.0)
    
    # Упрощаем доступ к значениям функций
    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12 = f_vals
    
    # === СИСТЕМА УРАВНЕНИЙ (формулы 6.1-6.5 из документа) ===
    
    # Уравнение 1: dCf1/dC (потери от заболеваемости)
    dCf1_dC = (1 / xm[0]) * (
        f1 * f2 * (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13) -
        f3 * (x2 + x3 + x6 + x14)
    )
    
    # Уравнение 2: dCf2/dC (потери сельского хозяйства)
    dCf2_dC = (1 / xm[1]) * (
        f4 * f5 * (x1 + x4 + x9 + x10 + x12) -
        f6 * (x2 + x3 + x5 + x6)
    )
    
    # Уравнение 3: dCf3/dC (потери от изменения природы)
    dCf3_dC = (1 / xm[2]) * (
        (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12) -
        f7 * (x2 + x3 + x6 + x14)
    )
    
    # Уравнение 4: dCf4/dC (потери от ухудшения качества жизни)
    dCf4_dC = (1 / xm[3]) * (
        f8 * f9 * f10 * (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13) -
        f11 * (x2 + x3 + x6 + x14)
    )
    
    # Уравнение 5: dCf5/dC (потери предприятия)
    dCf5_dC = (1 / xm[4]) * (
        f12 * (x1 + x5) -
        (x2 + x3 + x4 + x6 + x7 + x8 + x9 + x10 + x13 + x14)
    )
    
    dkdt = [dCf1_dC, dCf2_dC, dCf3_dC, dCf4_dC, dCf5_dC]
    
    # === ОГРАНИЧЕНИЯ НА ГРАНИЦАХ ===
    for i in range(len(dkdt)):
        # Если переменная близка к 0 и производная отрицательна
        if x[i] <= eps and dkdt[i] < 0:
            dkdt[i] = 0.0
        # Если переменная близка к 1 и производная положительна
        if x[i] >= 1.0 - eps and dkdt[i] > 0:
            dkdt[i] = 0.0

    return dkdt


def fx_poly4(x, params):
    """
    Полином 4-й степени для внутренних функций
    params = [a, b, c, d, e] для уравнения: a*x^4 + b*x^3 + c*x^2 + d*x + e
    """
    if len(params) >= 5:
        a, b, c, d, e = params[0], params[1], params[2], params[3], params[4]
        return a * x**4 + b * x**3 + c * x**2 + d * x + e
    elif len(params) == 4:
        # Если задано 4 коэффициента, используем полином 3-й степени
        a, b, c, d = params[0], params[1], params[2], params[3]
        return a * x**3 + b * x**2 + c * x + d
    elif len(params) == 3:
        # Если задано 3 коэффициента, используем полином 2-й степени
        a, b, c = params[0], params[1], params[2]
        return a * x**2 + b * x + c
    elif len(params) == 2:
        # Линейная функция
        a, b = params[0], params[1]
        return a * x + b
    elif len(params) == 1:
        # Константа
        return params[0]
    else:
        return 0.0


def fx_poly3(x, params):
    """
    Полином 3-й степени для возмущений
    params = [a, b, c, d] для уравнения: a*x^3 + b*x^2 + c*x + d
    """
    if len(params) >= 4:
        a, b, c, d = params[0], params[1], params[2], params[3]
        return a * x**3 + b * x**2 + c * x + d
    elif len(params) == 3:
        a, b, c = params[0], params[1], params[2]
        return a * x**2 + b * x + c
    elif len(params) == 2:
        a, b = params[0], params[1]
        return a * x + b
    elif len(params) == 1:
        return params[0]
    else:
        return 0.0


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ИЗ РАЗДЕЛА 6.3 ДОКУМЕНТА
# ============================================================================

def f1_cf3(cf3):
    """
    f1(Cf3) - зависимость потерь от заболеваемости от потерь от изменения природы
    Логистическая кривая из формулы (6.8)
    """
    return 0.5 * np.exp(cf3) / (1 + 0.5 * (np.exp(cf3) - 1))


def f2_cf4(cf4):
    """
    f2(Cf4) - зависимость потерь от заболеваемости от потерь качества жизни
    Линейная функция из формулы (6.8) в документе
    """
    return 0.3 * cf4 + 15


def f3_cf5(cf5):
    """
    f3(Cf5) - зависимость потерь от заболеваемости от потерь предприятия
    Ступенчатая функция из формулы (6.10)
    """
    return np.where(cf5 < 0.4, 0.3, 0.5)


def f4_cf3(cf3):
    """
    f4(Cf3) - зависимость потерь сельского хозяйства от потерь от изменения природы
    Линейная функция из формулы (6.11)
    """
    return 0.7 * cf3 + 11


def f5_cf4(cf4):
    """
    f5(Cf4) - зависимость потерь сельского хозяйства от потерь качества жизни
    Линейная функция из формулы (6.12)
    """
    return 0.8 * cf4 + 9


def f6_cf5(cf5):
    """
    f6(Cf5) - зависимость потерь сельского хозяйства от потерь предприятия
    Обратно пропорциональная функция из формулы (6.13)
    """
    return 0.8 / (cf5 + 12)


def f7_cf5(cf5):
    """
    f7(Cf5) - зависимость потерь от изменения природы от потерь предприятия
    Обратно пропорциональная функция из формулы (6.14)
    """
    return 0.8 / (cf5 + 11)


def f8_cf1(cf1):
    """
    f8(Cf1) - зависимость потерь качества жизни от потерь от заболеваемости
    Линейная функция из формулы (6.15)
    """
    return 0.7 * cf1 + 13


def f9_cf2(cf2):
    """
    f9(Cf2) - зависимость потерь качества жизни от потерь сельского хозяйства
    Логистическая функция из формулы (6.16)
    """
    return 1 / (1 + np.exp(-cf2))


def f10_cf3(cf3):
    """
    f10(Cf3) - зависимость потерь качества жизни от потерь от изменения природы
    Линейная функция из формулы (6.17)
    """
    return 0.55 * cf3 + 13


def f11_cf5(cf5):
    """
    f11(Cf5) - зависимость потерь качества жизни от потерь предприятия
    Обратно пропорциональная функция из формулы (6.18)
    """
    return 0.55 / (cf5 + 12) + 2


def f12_cf1(cf1):
    """
    f12(Cf1) - зависимость потерь предприятия от потерь от заболеваемости
    Линейная функция из формулы (6.19)
    """
    return 0.5 * cf1 + 3


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def calculate_total_loss(Cf_values, weights=None):
    """
    Расчет суммарных потерь по формуле (2.9) из документа
    Cf_values = [Cf1, Cf2, Cf3, Cf4, Cf5]
    weights = [μ1, μ2, μ3, μ4, μ5] - весовые коэффициенты
    """
    if weights is None:
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # равные веса по умолчанию
    
    total_loss = 0.0
    for i in range(min(len(Cf_values), len(weights))):
        total_loss += weights[i] * Cf_values[i]
    
    return total_loss


def normalize_values(values, max_values=None):
    """
    Нормализация значений в диапазон [0, 1]
    values - массив значений
    max_values - максимальные значения для нормализации
    """
    if max_values is None:
        max_values = [1.0] * len(values)
    
    normalized = []
    for i in range(len(values)):
        if max_values[i] > 0:
            norm_val = values[i] / max_values[i]
        else:
            norm_val = values[i]
        
        # Ограничение в диапазоне [0, 1]
        norm_val = max(0.0, min(1.0, norm_val))
        normalized.append(norm_val)
    
    return normalized


def calculate_concentration_factor(C, params):
    """
    Расчет фактора концентрации для возмущений
    C - концентрация (0-1)
    params - параметры зависимости
    """
    if len(params) >= 4:
        # Кубическая зависимость
        return (params[0] * C**3 + params[1] * C**2 + 
                params[2] * C + params[3])
    elif len(params) >= 3:
        # Квадратичная зависимость
        return params[0] * C**2 + params[1] * C + params[2]
    elif len(params) >= 2:
        # Линейная зависимость
        return params[0] * C + params[1]
    elif len(params) >= 1:
        # Константа
        return params[0]
    else:
        return 0.0


# ============================================================================
# ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ И ВАЛИДАЦИИ
# ============================================================================

def test_system_with_time():
    """
    Тестовая функция для проверки работы системы уравнений с учетом времени
    """
    # Тестовые значения
    x = [0.5, 0.7, 0.9, 0.4, 0.5]  # Cf1-Cf5
    C = 0.5  # Концентрация
    t = 0.5  # Время
    
    # Тестовые коэффициенты возмущений (14 x 4)
    faks = [
        [0.1, -0.2, 0.5, 2.0],     # x1(t) = 0.1t³ - 0.2t² + 0.5t + 2.0
        [-0.1, 0.3, -0.2, 2.2],    # x2(t) = -0.1t³ + 0.3t² - 0.2t + 2.2
        [0.0, 0.0, 0.0, 0.0],      # x3(t) = 0
        [0.2, -0.1, 1.0, 4.0],     # x4(t) = 0.2t³ - 0.1t² + 1.0t + 4.0
        [-0.1, 0.2, -0.3, 3.0],    # x5(t) = -0.1t³ + 0.2t² - 0.3t + 3.0
        [0.05, -0.05, 0.1, 2.0],   # x6(t) = 0.05t³ - 0.05t² + 0.1t + 2.0
        [0, 0, 7, 5],              # x7(C) = 7C + 5
        [0, 0, 0, 0],              # x8(C) = 0
        [0, 0, 0.6, 3],            # x9(C) = 0.6C + 3
        [0, 0, 0.7, 4],            # x10(C) = 0.7C + 4
        [0, 0, 3, 5],              # x11(C) = 3C + 5
        [0, 0, 3.2, 3],            # x12(C) = 3.2C + 3
        [0, 0, 3.3, 4],            # x13(C) = 3.3C + 4
        [0, 0, 2, 5]               # x14(C) = 2C + 5
    ]
    
    # Тестовые коэффициенты внутренних функций (12 x 5)
    f = []
    for i in range(12):
        # Простые линейные коэффициенты для теста
        f.append([0.0, 0.0, 0.0, 1.0, 0.0])
    
    # Масштабирующие коэффициенты
    xm = [1.0, 1.0, 1.0, 1.0, 1.0]
    
    # Расчет производных
    derivatives = pend(x, C, faks, f, xm, t)
    
    print("Тест системы уравнений с временем:")
    print(f"Входные значения Cf: {x}")
    print(f"Концентрация C: {C}")
    print(f"Время t: {t}")
    print(f"x1(t) при t={t}: {fx_poly3(t, faks[0]):.4f}")
    print(f"x2(t) при t={t}: {fx_poly3(t, faks[1]):.4f}")
    print(f"x3(t) при t={t}: {fx_poly3(t, faks[2]):.4f}")
    print(f"x4(t) при t={t}: {fx_poly3(t, faks[3]):.4f}")
    print(f"x5(t) при t={t}: {fx_poly3(t, faks[4]):.4f}")
    print(f"x6(t) при t={t}: {fx_poly3(t, faks[5]):.4f}")
    print(f"x7(C) при C={C}: {fx_poly3(C, faks[6]):.4f}")
    print(f"Производные dCf/dC: {derivatives}")
    
    return derivatives


if __name__ == "__main__":
    # Запуск теста при прямом выполнении файла
    test_system_with_time()