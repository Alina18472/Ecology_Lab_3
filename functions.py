import numpy as np
def pend(x, C, faks, f, xm, t=0.0, power=0.6):
    """
    Система дифференциальных уравнений для модели потерь от загрязнения атмосферы
    x = [Cf1, Cf2, Cf3, Cf4, Cf5] - потери (нормированные от 0 до 1)
    C - концентрация загрязняющих веществ (нормированная от 0 до 1)
    t - время (для возмущений x1-x6)
    faks - матрица коэффициентов возмущений [14 x 2] - ТОЛЬКО a и b для линейных функций
    f - матрица коэффициентов внутренних функций [12 x ...]
    xm - масштабирующие коэффициенты (максимальные значения)
    power - степень для нормализации (по умолчанию 0.75)
    """
    # Защита от слишком маленьких/больших степеней
    power = max(0.3, min(2.0, power))  # ограничиваем power от 0.3 до 2.0
    
    eps = 1e-4
    x_safe = np.clip(x, eps, 1.0 - eps)
    
    # === ОПТИМИЗАЦИЯ: ВЫЧИСЛЯЕМ ВСЕ ВОЗМУЩЕНИЯ ОДИН РАЗ ===
    
    # Массив для возмущений x1-x14
    x_vals = np.zeros(14)
    
    # x1-x6: зависят от времени t
    for i in range(min(6, len(faks))):
        if len(faks[i]) >= 2:
            val = fx_linear(t, faks[i])
            x_vals[i] = max(0.0, min(1.0, val / 10.0))  # нормализация сразу
    
    # x7-x14: зависят от концентрации C
    for i in range(6, min(14, len(faks))):
        if len(faks[i]) >= 2:
            val = fx_linear(C, faks[i])
            x_vals[i] = max(0.0, min(1.0, val / 10.0))  # нормализация сразу
    
    # Извлекаем значения для удобства
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14 = x_vals
    
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
    
    # Вычисляем суммы ОДИН РАЗ для всех уравнений
    sum_pos = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13
    sum_neg = x2 + x3 + x6 + x14
    
    sum_pos2 = x1 + x4 + x9 + x10 + x12
    sum_neg2 = x2 + x3 + x5 + x6
    
    sum_pos3 = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12
    sum_neg3 = x2 + x3 + x6 + x14
    
    sum_pos4 = x1 + x4 + x5 + x7 + x8 + x9 + x10 + x11 + x12 + x13
    sum_neg4 = x2 + x3 + x6 + x14
    
    sum_pos5 = x1 + x5
    sum_neg5 = x2 + x3 + x4 + x6 + x7 + x8 + x9 + x10 + x13 + x14
    
    # === ОПТИМИЗАЦИЯ: ИСПОЛЬЗУЕМ np.power ВМЕСТО ** ===
    
    # Уравнение 1: dCf1/dC (потери от заболеваемости)
    norm_sum_pos = min(1.0, np.power(sum_pos / 10.0, power))
    norm_sum_neg = min(1.0, np.power(sum_neg / 4.0, power))
    
    dCf1_dC = (1 / xm[0]) * (
        f1 * f2 * norm_sum_pos -
        f3 * norm_sum_neg
    )
    
    # Уравнение 2: dCf2/dC (потери сельского хозяйства)
    norm_sum_pos2 = min(1.0, np.power(sum_pos2 / 5.0, power))
    norm_sum_neg2 = min(1.0, np.power(sum_neg2 / 4.0, power))
    
    dCf2_dC = (1 / xm[1]) * (
        f4 * f5 * norm_sum_pos2 -
        f6 * norm_sum_neg2
    )
    
    # Уравнение 3: dCf3/dC (потери от изменения природы)
    norm_sum_pos3 = min(1.0, np.power(sum_pos3 / 9.0, power))
    norm_sum_neg3 = min(1.0, np.power(sum_neg3 / 4.0, power))
    
    dCf3_dC = (1 / xm[2]) * (
        norm_sum_pos3 -
        f7 * norm_sum_neg3
    )
    
    # Уравнение 4: dCf4/dC (потери от ухудшения качества жизни)
    norm_sum_pos4 = min(1.0, np.power(sum_pos4 / 10.0, power))
    norm_sum_neg4 = min(1.0, np.power(sum_neg4 / 4.0, power))
    
    dCf4_dC = (1 / xm[3]) * (
        f8 * f9 * f10 * norm_sum_pos4 -
        f11 * norm_sum_neg4
    )
    
    # Уравнение 5: dCf5/dC (потери предприятия)
    norm_sum_pos5 = min(1.0, np.power(sum_pos5 / 2.0, power))
    norm_sum_neg5 = min(1.0, np.power(sum_neg5 / 10.0, power))
    
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
    denominator = max(0.01, cf5 + b)
    raw = a / denominator
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

def test_system_with_time(power=0.75):
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
    
    derivatives = pend(x, C, faks, f, xm, t, power=power)
    
    print(f"Тест системы уравнений с степенной нормализацией (power={power}):")
    print(f"Входные значения Cf: {x}")
    print(f"Концентрация C: {C}")
    print(f"Время t: {t}")
    print(f"Производные dCf/dC: {derivatives}")
    
    # Дополнительно: покажем влияние степени на нормализацию
    print("\nПример влияния степени на нормализацию:")
    test_sums = [0.0, 2.5, 5.0, 7.5, 10.0]
    for s in test_sums:
        linear = min(1.0, s/10.0)
        power_075 = min(1.0, (s/10.0) ** 0.75)
        power_050 = min(1.0, (s/10.0) ** 0.50)
        print(f"Сумма={s:4.1f}: линейная={linear:.3f}, степень 0.75={power_075:.3f}, степень 0.50={power_050:.3f}")
    
    return derivatives

def compare_normalizations():
    """
    Функция для сравнения разных степеней нормализации
    """
    print("Сравнение разных степеней нормализации:")
    print("=" * 60)
    print("Значение | Линейная | Степень 0.9 | Степень 0.75 | Степень 0.5 | Степень 0.3")
    print("-" * 60)
    
    values = [i/10.0 for i in range(0, 11)]
    for v in values:
        linear = min(1.0, v)
        p09 = min(1.0, v ** 0.9)
        p075 = min(1.0, v ** 0.75)
        p05 = min(1.0, v ** 0.5)
        p03 = min(1.0, v ** 0.3)
        print(f"{v:6.1f}   | {linear:8.3f} | {p09:11.3f} | {p075:12.3f} | {p05:10.3f} | {p03:10.3f}")


if __name__ == "__main__":
    # Тестируем с разными степенями
    for power in [1.0, 0.9, 0.75, 0.5, 0.3]:
        print("\n" + "="*60)
        test_system_with_time(power=power)
    
    print("\n" + "="*60)
    compare_normalizations()