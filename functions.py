# # functions.py
# import numpy as np

# def pend(x, C, faks, f, xm, t=0.0):
#     """
#     Система дифференциальных уравнений для модели потерь от загрязнения атмосферы
#     x = [Cf1, Cf2, Cf3, Cf4, Cf5] - потери (нормированные от 0 до 1)
#     C - концентрация загрязняющих веществ (нормированная от 0 до 1)
#     t - время (для возмущений x1-x6)
#     faks - матрица коэффициентов возмущений [14 x 2] - ТОЛЬКО a и b для линейных функций
#     f - матрица коэффициентов внутренних функций [12 x ...]
#     xm - масштабирующие коэффициенты (максимальные значения)
    
#     Уравнения взяты из раздела 6.2 документа
#     """
#     eps = 1e-4
#     x_safe = np.clip(x, eps, 1.0 - eps)
    
#     # === ВОЗМУЩЕНИЯ x1-x6 (зависят от времени t) ===
#     # ЛИНЕЙНЫЕ ФУНКЦИИ: a*t + b
#     if len(faks) > 0 and len(faks[0]) >= 2:
#         x1 = fx_linear(t, faks[0])
#     else:
#         x1 = 0.0
    
#     if len(faks) > 1 and len(faks[1]) >= 2:
#         x2 = fx_linear(t, faks[1])
#     else:
#         x2 = 0.0
    
#     if len(faks) > 2 and len(faks[2]) >= 2:
#         x3 = fx_linear(t, faks[2])
#     else:
#         x3 = 0.0
    
#     if len(faks) > 3 and len(faks[3]) >= 2:
#         x4 = fx_linear(t, faks[3])
#     else:
#         x4 = 0.0
    
#     if len(faks) > 4 and len(faks[4]) >= 2:
#         x5 = fx_linear(t, faks[4])
#     else:
#         x5 = 0.0
    
#     if len(faks) > 5 and len(faks[5]) >= 2:
#         x6 = fx_linear(t, faks[5])
#     else:
#         x6 = 0.0
    
#     # === ВОЗМУЩЕНИЯ x7-x14 (зависят от концентрации C) ===
#     # ЛИНЕЙНЫЕ ФУНКЦИИ: a*C + b
#     if len(faks) > 6 and len(faks[6]) >= 2:
#         x7 = fx_linear(C, faks[6])
#     else:
#         x7 = 0.0
    
#     if len(faks) > 7 and len(faks[7]) >= 2:
#         x8 = fx_linear(C, faks[7])
#     else:
#         x8 = 0.0
    
#     if len(faks) > 8 and len(faks[8]) >= 2:
#         x9 = fx_linear(C, faks[8])
#     else:
#         x9 = 0.0
    
#     if len(faks) > 9 and len(faks[9]) >= 2:
#         x10 = fx_linear(C, faks[9])
#     else:
#         x10 = 0.0
    
#     if len(faks) > 10 and len(faks[10]) >= 2:
#         x11 = fx_linear(C, faks[10])
#     else:
#         x11 = 0.0
    
#     if len(faks) > 11 and len(faks[11]) >= 2:
#         x12 = fx_linear(C, faks[11])
#     else:
#         x12 = 0.0
    
#     if len(faks) > 12 and len(faks[12]) >= 2:
#         x13 = fx_linear(C, faks[12])
#     else:
#         x13 = 0.0
    
#     if len(faks) > 13 and len(faks[13]) >= 2:
#         x14 = fx_linear(C, faks[13])
#     else:
#         x14 = 0.0
    
#     # === ВНУТРЕННИЕ ФУНКЦИИ ===
#     # Используем параметры из f
    
#     # f₁: логистическая (2 параметра)
#     if len(f) > 0 and len(f[0]) >= 2:
#         f1 = f1_cf3(x_safe[2], f[0][0], f[0][1])  # f1(Cf3)
#     else:
#         f1 = f1_cf3_default(x_safe[2])
    
#     # f₂: линейная (2 параметра)
#     if len(f) > 1 and len(f[1]) >= 2:
#         f2 = f2_cf4(x_safe[3], f[1][0], f[1][1])  # f2(Cf4)
#     else:
#         f2 = f2_cf4_default(x_safe[3])
    
#     # f₃: ступенчатая (3 параметра)
#     if len(f) > 2 and len(f[2]) >= 3:
#         f3 = f3_cf5(x_safe[4], f[2][0], f[2][1], f[2][2])  # f3(Cf5)
#     else:
#         f3 = f3_cf5_default(x_safe[4])
    
#     # f₄: линейная (2 параметра)
#     if len(f) > 3 and len(f[3]) >= 2:
#         f4 = f4_cf3(x_safe[2], f[3][0], f[3][1])  # f4(Cf3)
#     else:
#         f4 = f4_cf3_default(x_safe[2])
    
#     # f₅: линейная (2 параметра)
#     if len(f) > 4 and len(f[4]) >= 2:
#         f5 = f5_cf4(x_safe[3], f[4][0], f[4][1])  # f5(Cf4)
#     else:
#         f5 = f5_cf4_default(x_safe[3])
    
#     # f₆: дробная (2 параметра)
#     if len(f) > 5 and len(f[5]) >= 2:
#         f6 = f6_cf5(x_safe[4], f[5][0], f[5][1])  # f6(Cf5)
#     else:
#         f6 = f6_cf5_default(x_safe[4])
    
#     # f₇: дробная (2 параметра)
#     if len(f) > 6 and len(f[6]) >= 2:
#         f7 = f7_cf5(x_safe[4], f[6][0], f[6][1])  # f7(Cf5)
#     else:
#         f7 = f7_cf5_default(x_safe[4])
    
#     # f₈: линейная (2 параметра)
#     if len(f) > 7 and len(f[7]) >= 2:
#         f8 = f8_cf1(x_safe[0], f[7][0], f[7][1])  # f8(Cf1)
#     else:
#         f8 = f8_cf1_default(x_safe[0])
    
#     # f₉: логистическая (фиксированная, но может быть настроена)
#     if len(f) > 8 and len(f[8]) >= 2:
#         f9 = f9_cf2(x_safe[1], f[8][0], f[8][1])  # f9(Cf2)
#     else:
#         f9 = f9_cf2_default(x_safe[1])
    
#     # f₁₀: линейная (2 параметра)
#     if len(f) > 9 and len(f[9]) >= 2:
#         f10 = f10_cf3(x_safe[2], f[9][0], f[9][1])  # f10(Cf3)
#     else:
#         f10 = f10_cf3_default(x_safe[2])
    
#     # f₁₁: дробная (3 параметра)
#     if len(f) > 10 and len(f[10]) >= 3:
#         f11 = f11_cf5(x_safe[4], f[10][0], f[10][1], f[10][2])  # f11(Cf5)
#     else:
#         f11 = f11_cf5_default(x_safe[4])
    
#     # f₁₂: линейная (2 параметра)
#     if len(f) > 11 and len(f[11]) >= 2:
#         f12 = f12_cf1(x_safe[0], f[11][0], f[11][1])  # f12(Cf1)
#     else:
#         f12 = f12_cf1_default(x_safe[0])
    
#     # === СИСТЕМА УРАВНЕНИЙ (формулы 6.1-6.5 из документа) ===
    
#     # Уравнение 1: dCf1/dC (потери от заболеваемости)
#     dCf1_dC = (1 / xm[0]) * (
#         f1 * f2 * (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13) -
#         f3 * (x2 + x3 + x6 + x14)
#     )
    
#     # Уравнение 2: dCf2/dC (потери сельского хозяйства)
#     dCf2_dC = (1 / xm[1]) * (
#         f4 * f5 * (x1 + x4 + x9 + x10 + x12) -
#         f6 * (x2 + x3 + x5 + x6)
#     )
    
#     # Уравнение 3: dCf3/dC (потери от изменения природы)
#     dCf3_dC = (1 / xm[2]) * (
#         (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12) -
#         f7 * (x2 + x3 + x6 + x14)
#     )
    
#     # Уравнение 4: dCf4/dC (потери от ухудшения качества жизни)
#     dCf4_dC = (1 / xm[3]) * (
#         f8 * f9 * f10 * (x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13) -
#         f11 * (x2 + x3 + x6 + x14)
#     )
    
#     # Уравнение 5: dCf5/dC (потери предприятия)
#     dCf5_dC = (1 / xm[4]) * (
#         f12 * (x1 + x5) -
#         (x2 + x3 + x4 + x6 + x7 + x8 + x9 + x10 + x13 + x14)
#     )
    
#     dkdt = [dCf1_dC, dCf2_dC, dCf3_dC, dCf4_dC, dCf5_dC]
    
#     # === ОГРАНИЧЕНИЯ НА ГРАНИЦАХ ===
#     for i in range(len(dkdt)):
#         # Если переменная близка к 0 и производная отрицательна
#         if x[i] <= eps and dkdt[i] < 0:
#             dkdt[i] = 0.0
#         # Если переменная близка к 1 и производная положительна
#         if x[i] >= 1.0 - eps and dkdt[i] > 0:
#             dkdt[i] = 0.0

#     return dkdt


# def fx_linear(x, params):
#     """
#     Линейная функция для возмущений (как в документе)
#     params = [a, b] для уравнения: a*x + b
#     """
#     if len(params) >= 2:
#         a, b = params[0], params[1]
#         return a * x + b
#     elif len(params) == 1:
#         # Константа
#         return params[0]
#     else:
#         return 0.0


# # ============================================================================
# # НАСТРАИВАЕМЫЕ ВНУТРЕННИЕ ФУНКЦИИ
# # ============================================================================

# # f₁(Cf₃) = a·e^{Cf₃} / (1 + b·(e^{Cf₃} - 1))
# def f1_cf3(cf3, a=0.5, b=0.5):
#     """Логистическая функция"""
#     return a * np.exp(cf3) / (1 + b * (np.exp(cf3) - 1))

# def f1_cf3_default(cf3):
#     """Значение по умолчанию"""
#     return f1_cf3(cf3, 0.5, 0.5)

# # f₂(Cf₄) = a·Cf₄ + b
# def f2_cf4(cf4, a=0.3, b=15.0):
#     """Линейная функция"""
#     # Масштабируем, так как Cf4 в [0,1], а b большое
#     return (a * cf4 * 20 + b) / 20

# def f2_cf4_default(cf4):
#     return f2_cf4(cf4, 0.3, 15.0)

# # f₃(Cf₅) = low при Cf₅ < threshold, иначе high
# def f3_cf5(cf5, low=0.3, threshold=0.4, high=0.5):
#     """Ступенчатая функция"""
#     if cf5 < threshold:
#         return low
#     else:
#         return high

# def f3_cf5_default(cf5):
#     return f3_cf5(cf5, 0.3, 0.4, 0.5)

# # f₄(Cf₃) = a·Cf₃ + b
# def f4_cf3(cf3, a=0.7, b=11.0):
#     """Линейная функция"""
#     return (a * cf3 * 15 + b) / 15

# def f4_cf3_default(cf3):
#     return f4_cf3(cf3, 0.7, 11.0)

# # f₅(Cf₄) = a·Cf₄ + b
# def f5_cf4(cf4, a=0.8, b=9.0):
#     """Линейная функция"""
#     return (a * cf4 * 15 + b) / 15

# def f5_cf4_default(cf4):
#     return f5_cf4(cf4, 0.8, 9.0)

# # f₆(Cf₅) = a / (Cf₅ + b)
# def f6_cf5(cf5, a=0.8, b=12.0):
#     """Дробно-рациональная функция"""
#     return a / (cf5 * 15 + b) * 15

# def f6_cf5_default(cf5):
#     return f6_cf5(cf5, 0.8, 12.0)

# # f₇(Cf₅) = a / (Cf₅ + b)
# def f7_cf5(cf5, a=0.8, b=11.0):
#     """Дробно-рациональная функция"""
#     return a / (cf5 * 15 + b) * 15

# def f7_cf5_default(cf5):
#     return f7_cf5(cf5, 0.8, 11.0)

# # f₈(Cf₁) = a·Cf₁ + b
# def f8_cf1(cf1, a=0.7, b=13.0):
#     """Линейная функция"""
#     return (a * cf1 * 20 + b) / 20

# def f8_cf1_default(cf1):
#     return f8_cf1(cf1, 0.7, 13.0)

# # f₉(Cf₂) = 1 / (1 + e^{-Cf₂}) - но можно настроить масштаб
# def f9_cf2(cf2, scale=10.0, shift=5.0):
#     """Логистическая функция"""
#     scaled_cf2 = cf2 * scale - shift
#     return 1 / (1 + np.exp(-scaled_cf2))

# def f9_cf2_default(cf2):
#     return f9_cf2(cf2, 10.0, 5.0)

# # f₁₀(Cf₃) = a·Cf₃ + b
# def f10_cf3(cf3, a=0.55, b=13.0):
#     """Линейная функция"""
#     return (a * cf3 * 20 + b) / 20

# def f10_cf3_default(cf3):
#     return f10_cf3(cf3, 0.55, 13.0)

# # f₁₁(Cf₅) = a / (Cf₅ + b) + c
# def f11_cf5(cf5, a=0.55, b=12.0, c=2.0):
#     """Дробно-рациональная функция с смещением"""
#     return (a / (cf5 * 15 + b) * 15 + c) / 3

# def f11_cf5_default(cf5):
#     return f11_cf5(cf5, 0.55, 12.0, 2.0)

# # f₁₂(Cf₁) = a·Cf₁ + b
# def f12_cf1(cf1, a=0.5, b=3.0):
#     """Линейная функция"""
#     return (a * cf1 * 10 + b) / 10

# def f12_cf1_default(cf1):
#     return f12_cf1(cf1, 0.5, 3.0)


# # ============================================================================
# # ДОПОЛНИТЕЛЬНЫЕ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# # ============================================================================

# def calculate_total_loss(Cf_values, weights=None):
#     """
#     Расчет суммарных потерь по формуле (2.9) из документа
#     Cf_values = [Cf1, Cf2, Cf3, Cf4, Cf5]
#     weights = [μ1, μ2, μ3, μ4, μ5] - весовые коэффициенты
#     """
#     if weights is None:
#         weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # равные веса по умолчанию
    
#     total_loss = 0.0
#     for i in range(min(len(Cf_values), len(weights))):
#         total_loss += weights[i] * Cf_values[i]
    
#     return total_loss


# def normalize_values(values, max_values=None):
#     """
#     Нормализация значений в диапазон [0, 1]
#     values - массив значений
#     max_values - максимальные значения для нормализации
#     """
#     if max_values is None:
#         max_values = [1.0] * len(values)
    
#     normalized = []
#     for i in range(len(values)):
#         if max_values[i] > 0:
#             norm_val = values[i] / max_values[i]
#         else:
#             norm_val = values[i]
        
#         # Ограничение в диапазоне [0, 1]
#         norm_val = max(0.0, min(1.0, norm_val))
#         normalized.append(norm_val)
    
#     return normalized


# def calculate_concentration_factor(C, params):
#     """
#     Расчет фактора концентрации для возмущений
#     C - концентрация (0-1)
#     params - параметры зависимости [a, b] для линейной функции
#     """
#     if len(params) >= 2:
#         # Линейная зависимость a*C + b
#         return params[0] * C + params[1]
#     elif len(params) >= 1:
#         # Константа
#         return params[0]
#     else:
#         return 0.0


# # ============================================================================
# # ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ И ВАЛИДАЦИИ
# # ============================================================================

# def test_system_with_time():
#     """
#     Тестовая функция для проверки работы системы уравнений с учетом времени
#     Использует значения из документа (раздел 6.4)
#     """
#     # Тестовые значения из документа
#     x = [0.5, 0.7, 0.9, 0.4, 0.5]  # Cf1-Cf5
#     C = 0.5  # Концентрация
#     t = 0.5  # Время
    
#     # Коэффициенты возмущений из документа (Таблица 6.9)
#     faks = [
#         [0.1, 2.0],      # x1(t) = 0.1*t + 2.0
#         [-0.3, 2.2],     # x2(t) = -0.3*t + 2.2
#         [0.0, 0.0],      # x3(t) = 0
#         [3.0, 4.0],      # x4(t) = 3.0*t + 4.0
#         [-0.3, 3.0],     # x5(t) = -0.3*t + 3.0
#         [0.05, 2.0],     # x6(t) = 0.05*t + 2.0
#         [7.0, 5.0],      # x7(C) = 7.0*C + 5.0
#         [0.0, 0.0],      # x8(C) = 0
#         [0.6, 3.0],      # x9(C) = 0.6*C + 3.0
#         [0.7, 4.0],      # x10(C) = 0.7*C + 4.0
#         [3.0, 5.0],      # x11(C) = 3.0*C + 5.0
#         [3.2, 3.0],      # x12(C) = 3.2*C + 3.0
#         [3.3, 4.0],      # x13(C) = 3.3*C + 4.0
#         [2.0, 5.0]       # x14(C) = 2.0*C + 5.0
#     ]
    
#     # Коэффициенты внутренних функций из документа
#     f = [
#         [0.5, 0.5],           # f₁: логистическая
#         [0.3, 15.0],          # f₂: линейная
#         [0.3, 0.4, 0.5],      # f₃: ступенчатая
#         [0.7, 11.0],          # f₄: линейная
#         [0.8, 9.0],           # f₅: линейная
#         [0.8, 12.0],          # f₆: дробная
#         [0.8, 11.0],          # f₇: дробная
#         [0.7, 13.0],          # f₈: линейная
#         [10.0, 5.0],          # f₉: логистическая (масштаб)
#         [0.55, 13.0],         # f₁₀: линейная
#         [0.55, 12.0, 2.0],    # f₁₁: дробная
#         [0.5, 3.0]            # f₁₂: линейная
#     ]
    
#     # Масштабирующие коэффициенты
#     xm = [1.0, 1.0, 1.0, 1.0, 1.0]
    
#     # Расчет производных
#     derivatives = pend(x, C, faks, f, xm, t)
    
#     print("Тест системы уравнений с настраиваемыми функциями:")
#     print(f"Входные значения Cf: {x}")
#     print(f"Концентрация C: {C}")
#     print(f"Время t: {t}")
#     print(f"Производные dCf/dC: {derivatives}")
    
#     # Проверка внутренних функций с параметрами
#     print("\nЗначения внутренних функций с параметрами:")
#     print(f"f1(Cf3={x[2]}) = {f1_cf3(x[2], f[0][0], f[0][1]):.4f}")
#     print(f"f2(Cf4={x[3]}) = {f2_cf4(x[3], f[1][0], f[1][1]):.4f}")
#     print(f"f3(Cf5={x[4]}) = {f3_cf5(x[4], f[2][0], f[2][1], f[2][2]):.4f}")
    
#     return derivatives


# if __name__ == "__main__":
#     # Запуск теста при прямом выполнении файла
#     test_system_with_time()

# functions.py - ВСЕ функции нормализованы к [0,1]
import numpy as np

def pend(x, C, faks, f, xm, t=0.0):
    """
    Система дифференциальных уравнений для модели потерь от загрязнения атмосферы
    x = [Cf1, Cf2, Cf3, Cf4, Cf5] - потери (нормированные от 0 до 1)
    C - концентрация загрязняющих веществ (нормированная от 0 до 1)
    t - время (для возмущений x1-x6)
    faks - матрица коэффициентов возмущений [14 x 2] - ТОЛЬКО a и b для линейных функций
    f - матрица коэффициентов внутренних функций [12 x ...]
    xm - масштабирующие коэффициенты (максимальные значения)
    """
    eps = 1e-4
    x_safe = np.clip(x, eps, 1.0 - eps)
    
    # === НОРМАЛИЗАЦИЯ ВОЗМУЩЕНИЙ ===
    # Функция для нормализации любого значения к [0,1]
    def normalize_value(value, max_possible=10.0):
        """Нормализует значение к диапазону [0,1]"""
        return max(0.0, min(1.0, value / max_possible))
    
    # === ВОЗМУЩЕНИЯ x1-x6 (зависят от времени t) ===
    # ЛИНЕЙНЫЕ ФУНКЦИИ: a*t + b
    if len(faks) > 0 and len(faks[0]) >= 2:
        x1 = normalize_value(fx_linear(t, faks[0]))
    else:
        x1 = 0.0
    
    if len(faks) > 1 and len(faks[1]) >= 2:
        x2 = normalize_value(fx_linear(t, faks[1]))
    else:
        x2 = 0.0
    
    if len(faks) > 2 and len(faks[2]) >= 2:
        x3 = normalize_value(fx_linear(t, faks[2]))
    else:
        x3 = 0.0
    
    if len(faks) > 3 and len(faks[3]) >= 2:
        x4 = normalize_value(fx_linear(t, faks[3]))
    else:
        x4 = 0.0
    
    if len(faks) > 4 and len(faks[4]) >= 2:
        x5 = normalize_value(fx_linear(t, faks[4]))
    else:
        x5 = 0.0
    
    if len(faks) > 5 and len(faks[5]) >= 2:
        x6 = normalize_value(fx_linear(t, faks[5]))
    else:
        x6 = 0.0
    
    # === ВОЗМУЩЕНИЯ x7-x14 (зависят от концентрации C) ===
    # ЛИНЕЙНЫЕ ФУНКЦИИ: a*C + b
    if len(faks) > 6 and len(faks[6]) >= 2:
        x7 = normalize_value(fx_linear(C, faks[6]))
    else:
        x7 = 0.0
    
    if len(faks) > 7 and len(faks[7]) >= 2:
        x8 = normalize_value(fx_linear(C, faks[7]))
    else:
        x8 = 0.0
    
    if len(faks) > 8 and len(faks[8]) >= 2:
        x9 = normalize_value(fx_linear(C, faks[8]))
    else:
        x9 = 0.0
    
    if len(faks) > 9 and len(faks[9]) >= 2:
        x10 = normalize_value(fx_linear(C, faks[9]))
    else:
        x10 = 0.0
    
    if len(faks) > 10 and len(faks[10]) >= 2:
        x11 = normalize_value(fx_linear(C, faks[10]))
    else:
        x11 = 0.0
    
    if len(faks) > 11 and len(faks[11]) >= 2:
        x12 = normalize_value(fx_linear(C, faks[11]))
    else:
        x12 = 0.0
    
    if len(faks) > 12 and len(faks[12]) >= 2:
        x13 = normalize_value(fx_linear(C, faks[12]))
    else:
        x13 = 0.0
    
    if len(faks) > 13 and len(faks[13]) >= 2:
        x14 = normalize_value(fx_linear(C, faks[13]))
    else:
        x14 = 0.0
    
    # === ВНУТРЕННИЕ ФУНКЦИИ ===
    # Используем параметры из f
    
    # f₁: логистическая (2 параметра)
    if len(f) > 0 and len(f[0]) >= 2:
        f1 = f1_cf3_norm(x_safe[2], f[0][0], f[0][1])  # УЖЕ нормализована
    else:
        f1 = f1_cf3_default_norm(x_safe[2])
    
    # f₂: линейная (2 параметра)
    if len(f) > 1 and len(f[1]) >= 2:
        f2 = f2_cf4_norm(x_safe[3], f[1][0], f[1][1])  # УЖЕ нормализована
    else:
        f2 = f2_cf4_default_norm(x_safe[3])
    
    # f₃: ступенчатая (3 параметра)
    if len(f) > 2 and len(f[2]) >= 3:
        f3 = f3_cf5_norm(x_safe[4], f[2][0], f[2][1], f[2][2])  # УЖЕ нормализована
    else:
        f3 = f3_cf5_default_norm(x_safe[4])
    
    # f₄: линейная (2 параметра)
    if len(f) > 3 and len(f[3]) >= 2:
        f4 = f4_cf3_norm(x_safe[2], f[3][0], f[3][1])  # УЖЕ нормализована
    else:
        f4 = f4_cf3_default_norm(x_safe[2])
    
    # f₅: линейная (2 параметра)
    if len(f) > 4 and len(f[4]) >= 2:
        f5 = f5_cf4_norm(x_safe[3], f[4][0], f[4][1])  # УЖЕ нормализована
    else:
        f5 = f5_cf4_default_norm(x_safe[3])
    
    # f₆: дробная (2 параметра)
    if len(f) > 5 and len(f[5]) >= 2:
        f6 = f6_cf5_norm(x_safe[4], f[5][0], f[5][1])  # УЖЕ нормализована
    else:
        f6 = f6_cf5_default_norm(x_safe[4])
    
    # f₇: дробная (2 параметра)
    if len(f) > 6 and len(f[6]) >= 2:
        f7 = f7_cf5_norm(x_safe[4], f[6][0], f[6][1])  # УЖЕ нормализована
    else:
        f7 = f7_cf5_default_norm(x_safe[4])
    
    # f₈: линейная (2 параметра)
    if len(f) > 7 and len(f[7]) >= 2:
        f8 = f8_cf1_norm(x_safe[0], f[7][0], f[7][1])  # УЖЕ нормализована
    else:
        f8 = f8_cf1_default_norm(x_safe[0])
    
    # f₉: логистическая (фиксированная, но может быть настроена)
    if len(f) > 8 and len(f[8]) >= 2:
        f9 = f9_cf2_norm(x_safe[1], f[8][0], f[8][1])  # УЖЕ нормализована
    else:
        f9 = f9_cf2_default_norm(x_safe[1])
    
    # f₁₀: линейная (2 параметра)
    if len(f) > 9 and len(f[9]) >= 2:
        f10 = f10_cf3_norm(x_safe[2], f[9][0], f[9][1])  # УЖЕ нормализована
    else:
        f10 = f10_cf3_default_norm(x_safe[2])
    
    # f₁₁: дробная (3 параметра)
    if len(f) > 10 and len(f[10]) >= 3:
        f11 = f11_cf5_norm(x_safe[4], f[10][0], f[10][1], f[10][2])  # УЖЕ нормализована
    else:
        f11 = f11_cf5_default_norm(x_safe[4])
    
    # f₁₂: линейная (2 параметра)
    if len(f) > 11 and len(f[11]) >= 2:
        f12 = f12_cf1_norm(x_safe[0], f[11][0], f[11][1])  # УЖЕ нормализована
    else:
        f12 = f12_cf1_default_norm(x_safe[0])
    
    # === СИСТЕМА УРАВНЕНИЙ (формулы 6.1-6.5 из документа) ===
    
    # Уравнение 1: dCf1/dC (потери от заболеваемости)
    # Все значения уже в [0,1], но суммируем их (максимум 10 слагаемых = 10)
    sum_pos = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13
    sum_neg = x2 + x3 + x6 + x14
    
    # Нормализуем суммы к [0,1] (максимум 10 слагаемых, каждый в [0,1])
    norm_sum_pos = min(1.0, sum_pos / 10.0)
    norm_sum_neg = min(1.0, sum_neg / 4.0)
    
    dCf1_dC = (1 / xm[0]) * (
        f1 * f2 * norm_sum_pos -
        f3 * norm_sum_neg
    )
    
    # Уравнение 2: dCf2/dC (потери сельского хозяйства)
    sum_pos2 = x1 + x4 + x9 + x10 + x12
    sum_neg2 = x2 + x3 + x5 + x6
    norm_sum_pos2 = min(1.0, sum_pos2 / 5.0)
    norm_sum_neg2 = min(1.0, sum_neg2 / 4.0)
    
    dCf2_dC = (1 / xm[1]) * (
        f4 * f5 * norm_sum_pos2 -
        f6 * norm_sum_neg2
    )
    
    # Уравнение 3: dCf3/dC (потери от изменения природы)
    sum_pos3 = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12
    sum_neg3 = x2 + x3 + x6 + x14
    norm_sum_pos3 = min(1.0, sum_pos3 / 9.0)
    norm_sum_neg3 = min(1.0, sum_neg3 / 4.0)
    
    dCf3_dC = (1 / xm[2]) * (
        norm_sum_pos3 -
        f7 * norm_sum_neg3
    )
    
    # Уравнение 4: dCf4/dC (потери от ухудшения качества жизни)
    sum_pos4 = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13
    sum_neg4 = x2 + x3 + x6 + x14
    norm_sum_pos4 = min(1.0, sum_pos4 / 10.0)
    norm_sum_neg4 = min(1.0, sum_neg4 / 4.0)
    
    dCf4_dC = (1 / xm[3]) * (
        f8 * f9 * f10 * norm_sum_pos4 -
        f11 * norm_sum_neg4
    )
    
    # Уравнение 5: dCf5/dC (потери предприятия)
    sum_pos5 = x1 + x5
    sum_neg5 = x2 + x3 + x4 + x6 + x7 + x8 + x9 + x10 + x13 + x14
    norm_sum_pos5 = min(1.0, sum_pos5 / 2.0)
    norm_sum_neg5 = min(1.0, sum_neg5 / 10.0)
    
    dCf5_dC = (1 / xm[4]) * (
        f12 * norm_sum_pos5 -
        norm_sum_neg5
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


def fx_linear(x, params):
    """
    Линейная функция для возмущений
    params = [a, b] для уравнения: a*x + b
    """
    if len(params) >= 2:
        a, b = params[0], params[1]
        return a * x + b
    elif len(params) == 1:
        return params[0]
    else:
        return 0.0


# ============================================================================
# НОРМАЛИЗОВАННЫЕ ВНУТРЕННИЕ ФУНКЦИИ (все в диапазоне [0,1])
# ============================================================================

# f₁(Cf₃) = a·e^{Cf₃} / (1 + b·(e^{Cf₃} - 1))
def f1_cf3_norm(cf3, a=0.5, b=0.5):
    """Логистическая функция, нормированная к [0,1]"""
    raw = a * np.exp(cf3) / (1 + b * (np.exp(cf3) - 1))
    return max(0.0, min(1.0, raw))

def f1_cf3_default_norm(cf3):
    return f1_cf3_norm(cf3, 0.5, 0.5)

# f₂(Cf₄) = a·Cf₄ + b
def f2_cf4_norm(cf4, a=0.3, b=15.0):
    """Линейная функция, нормированная к [0,1]"""
    # Нормализуем: (a*cf4 + b) / (a + b)
    raw = a * cf4 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f2_cf4_default_norm(cf4):
    return f2_cf4_norm(cf4, 0.3, 15.0)

# f₃(Cf₅) = low при Cf₅ < threshold, иначе high
def f3_cf5_norm(cf5, low=0.3, threshold=0.4, high=0.5):
    """Ступенчатая функция, уже в [0,1]"""
    if cf5 < threshold:
        return max(0.0, min(1.0, low))
    else:
        return max(0.0, min(1.0, high))

def f3_cf5_default_norm(cf5):
    return f3_cf5_norm(cf5, 0.3, 0.4, 0.5)

# f₄(Cf₃) = a·Cf₃ + b
def f4_cf3_norm(cf3, a=0.7, b=11.0):
    """Линейная функция, нормированная к [0,1]"""
    raw = a * cf3 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f4_cf3_default_norm(cf3):
    return f4_cf3_norm(cf3, 0.7, 11.0)

# f₅(Cf₄) = a·Cf₄ + b
def f5_cf4_norm(cf4, a=0.8, b=9.0):
    """Линейная функция, нормированная к [0,1]"""
    raw = a * cf4 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f5_cf4_default_norm(cf4):
    return f5_cf4_norm(cf4, 0.8, 9.0)

# f₆(Cf₅) = a / (Cf₅ + b)
def f6_cf5_norm(cf5, a=0.8, b=12.0):
    """Дробно-рациональная функция, нормированная к [0,1]"""
    # Гарантируем, что знаменатель положительный
    denominator = max(0.01, cf5 + b)
    raw = a / denominator
    # Нормализуем: делим на максимальное возможное значение (при cf5=0)
    max_val = a / b if b > 0 else 10.0
    if max_val > 0:
        return max(0.0, min(1.0, raw / max_val))
    return 0.5

def f6_cf5_default_norm(cf5):
    return f6_cf5_norm(cf5, 0.8, 12.0)

# f₇(Cf₅) = a / (Cf₅ + b)
def f7_cf5_norm(cf5, a=0.8, b=11.0):
    """Дробно-рациональная функция, нормированная к [0,1]"""
    denominator = max(0.01, cf5 + b)
    raw = a / denominator
    max_val = a / b if b > 0 else 10.0
    if max_val > 0:
        return max(0.0, min(1.0, raw / max_val))
    return 0.5

def f7_cf5_default_norm(cf5):
    return f7_cf5_norm(cf5, 0.8, 11.0)

# f₈(Cf₁) = a·Cf₁ + b
def f8_cf1_norm(cf1, a=0.7, b=13.0):
    """Линейная функция, нормированная к [0,1]"""
    raw = a * cf1 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f8_cf1_default_norm(cf1):
    return f8_cf1_norm(cf1, 0.7, 13.0)

# f₉(Cf₂) = 1 / (1 + e^{-Cf₂})
def f9_cf2_norm(cf2, scale=10.0, shift=5.0):
    """Логистическая функция, уже в [0,1]"""
    # Масштабируем Cf2 для получения разумного диапазона
    scaled_cf2 = cf2 * scale - shift
    raw = 1 / (1 + np.exp(-scaled_cf2))
    return max(0.0, min(1.0, raw))

def f9_cf2_default_norm(cf2):
    return f9_cf2_norm(cf2, 10.0, 5.0)

# f₁₀(Cf₃) = a·Cf₃ + b
def f10_cf3_norm(cf3, a=0.55, b=13.0):
    """Линейная функция, нормированная к [0,1]"""
    raw = a * cf3 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f10_cf3_default_norm(cf3):
    return f10_cf3_norm(cf3, 0.55, 13.0)

# f₁₁(Cf₅) = a / (Cf₅ + b) + c
def f11_cf5_norm(cf5, a=0.55, b=12.0, c=2.0):
    """Дробно-рациональная функция с смещением, нормированная к [0,1]"""
    denominator = max(0.01, cf5 + b)
    raw = a / denominator + c
    # Приблизительная нормализация
    max_val = (a / b + c) if b > 0 else (a / 0.01 + c)
    if max_val > 0:
        return max(0.0, min(1.0, raw / max_val))
    return 0.5

def f11_cf5_default_norm(cf5):
    return f11_cf5_norm(cf5, 0.55, 12.0, 2.0)

# f₁₂(Cf₁) = a·Cf₁ + b
def f12_cf1_norm(cf1, a=0.5, b=3.0):
    """Линейная функция, нормированная к [0,1]"""
    raw = a * cf1 + b
    denominator = abs(a) + abs(b)
    if denominator > 0:
        return max(0.0, min(1.0, raw / denominator))
    return 0.5

def f12_cf1_default_norm(cf1):
    return f12_cf1_norm(cf1, 0.5, 3.0)


# ============================================================================
# СТАРЫЕ ФУНКЦИИ ДЛЯ ОБРАТНОЙ СОВМЕСТИМОСТИ (можно удалить позже)
# ============================================================================

def f1_cf3(cf3, a=0.5, b=0.5):
    """Старая версия для обратной совместимости"""
    return f1_cf3_norm(cf3, a, b)

def f1_cf3_default(cf3):
    return f1_cf3_default_norm(cf3)

def f2_cf4(cf4, a=0.3, b=15.0):
    """Старая версия для обратной совместимости"""
    return f2_cf4_norm(cf4, a, b)

def f2_cf4_default(cf4):
    return f2_cf4_default_norm(cf4)

# ... аналогично для остальных функций ...


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
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]
    
    total_loss = 0.0
    for i in range(min(len(Cf_values), len(weights))):
        total_loss += weights[i] * Cf_values[i]
    
    return max(0.0, min(1.0, total_loss))


def normalize_values(values, max_values=None):
    """
    Нормализация значений в диапазон [0, 1]
    """
    if max_values is None:
        max_values = [1.0] * len(values)
    
    normalized = []
    for i in range(len(values)):
        if max_values[i] > 0:
            norm_val = values[i] / max_values[i]
        else:
            norm_val = values[i]
        
        norm_val = max(0.0, min(1.0, norm_val))
        normalized.append(norm_val)
    
    return normalized


# ============================================================================
# ФУНКЦИИ ДЛЯ ТЕСТИРОВАНИЯ
# ============================================================================

def test_system_with_time():
    """
    Тестовая функция для проверки работы системы уравнений
    """
    x = [0.5, 0.7, 0.9, 0.4, 0.5]
    C = 0.5
    t = 0.5
    
    faks = [
        [0.1, 2.0], [-0.3, 2.2], [0.0, 0.0], [3.0, 4.0], [-0.3, 3.0],
        [0.05, 2.0], [7.0, 5.0], [0.0, 0.0], [0.6, 3.0], [0.7, 4.0],
        [3.0, 5.0], [3.2, 3.0], [3.3, 4.0], [2.0, 5.0]
    ]
    
    f = [
        [0.5, 0.5], [0.3, 15.0], [0.3, 0.4, 0.5], [0.7, 11.0],
        [0.8, 9.0], [0.8, 12.0], [0.8, 11.0], [0.7, 13.0],
        [10.0, 5.0], [0.55, 13.0], [0.55, 12.0, 2.0], [0.5, 3.0]
    ]
    
    xm = [1.0, 1.0, 1.0, 1.0, 1.0]
    
    derivatives = pend(x, C, faks, f, xm, t)
    
    print("Тест системы уравнений с нормализованными функциями:")
    print(f"Входные значения Cf: {x}")
    print(f"Концентрация C: {C}")
    print(f"Время t: {t}")
    print(f"Производные dCf/dC: {derivatives}")
    
    # Проверяем, что все значения в разумных пределах
    for i, deriv in enumerate(derivatives):
        if abs(deriv) > 10:
            print(f"ВНИМАНИЕ: Большая производная dCf{i+1}/dC = {deriv}")
    
    return derivatives


if __name__ == "__main__":
    test_system_with_time()