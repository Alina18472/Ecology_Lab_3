# utils.py
import os

def get_initial_equations_from_inputs(ui):
    """Получение 5 начальных значений потерь Cf1-Cf5"""
    return [float(ui.lineEdits[f"u{i}"].text()) for i in range(1, 6)]

def get_faks_from_inputs(ui):
    """
    Получение коэффициентов для 14 возмущений
    Каждое возмущение имеет 4 коэффициента для полинома 3-й степени
    Всего 14 x 4 = 56 параметров
    """
    result = []
    
    # Для 14 возмущений (x1-x14)
    for fak_num in range(1, 15):  # от x1 до x14
        params = []
        # Каждое возмущение имеет 4 коэффициента: a, b, c, d
        # для полинома a*t³ + b*t² + c*t + d
        for param_num in range(1, 5):  # коэффициенты a, b, c, d
            try:
                # Ищем элемент с id "faks-{fak_num}-{param_num}"
                element_id = f"faks-{fak_num}-{param_num}"
                value = float(getattr(ui, f"lineEdit_{element_id}").text())
                params.append(value)
            except (AttributeError, ValueError, KeyError):
                # Если элемент не найден или значение некорректно, используем 0
                params.append(0.0)
        
        result.append(params)
    
    return result

def get_equations_from_inputs(ui):
    """
    Получение коэффициентов для 12 внутренних функций f1-f12
    Каждая функция имеет 5 коэффициентов для полинома 4-й степени
    Всего 12 x 5 = 60 параметров
    """
    result = []
    
    # Для 12 внутренних функций (f1-f12)
    for func_num in range(1, 13):  # от f1 до f12
        params = []
        # Каждая функция имеет 5 коэффициентов: a, b, c, d, e
        # для полинома a*Z⁴ + b*Z³ + c*Z² + d*Z + e
        for param_num in range(1, 6):  # коэффициенты a, b, c, d, e
            try:
                # Ищем элемент с id "equations-{func_num}-{param_num}"
                element_id = f"equations-{func_num}-{param_num}"
                value = float(getattr(ui, f"lineEdit_{element_id}").text())
                params.append(value)
            except (AttributeError, ValueError, KeyError):
                # Если элемент не найден или значение некорректно
                if param_num == 5:  # коэффициент e
                    params.append(0.0)  # свободный член
                elif param_num == 4:  # коэффициент d
                    params.append(1.0)  # линейный коэффициент по умолчанию
                else:
                    params.append(0.0)  # остальные коэффициенты
        
        result.append(params)
    
    return result

def get_restrictions(ui):
    """Получение 5 предельных значений для потерь Cf1-Cf5"""
    restrictions = []
    for i in range(1, 6):  # от Cf1 до Cf5
        try:
            value = float(ui.lineEdits[f"u_restrictions{i}"].text())
            restrictions.append(value)
        except (AttributeError, ValueError, KeyError):
            restrictions.append(1.0)  # значение по умолчанию
    return restrictions

def get_all_inputs_from_web():
    """
    Функция для получения данных из веб-интерфейса
    Используется в обработчиках Flask
    """
    from flask import request
    
    data = request.get_json()
    
    # Получение начальных условий (5 значений)
    initial_equations = []
    for i in range(1, 6):
        init_value = data.get(f"init-eq-{i}", "0.5")
        try:
            initial_equations.append(float(init_value))
        except ValueError:
            initial_equations.append(0.5)
    
    # Получение предельных значений (5 значений)
    restrictions = []
    for i in range(1, 6):
        restriction_value = data.get(f"restrictions-{i}", "1.0")
        try:
            restrictions.append(float(restriction_value))
        except ValueError:
            restrictions.append(1.0)
    
    # Получение возмущений (14 x 4 = 56 параметров)
    faks = []
    for i in range(1, 15):  # x1-x14
        fak_params = []
        for j in range(1, 5):  # a, b, c, d
            param_value = data.get(f"faks-{i}-{j}", "0.0")
            try:
                fak_params.append(float(param_value))
            except ValueError:
                fak_params.append(0.0)
        faks.append(fak_params)
    
    # Получение внутренних функций (12 x 5 = 60 параметров)
    equations = []
    for i in range(1, 13):  # f1-f12
        func_params = []
        for j in range(1, 6):  # a, b, c, d, e
            param_value = data.get(f"equations-{i}-{j}", "0.0")
            try:
                func_params.append(float(param_value))
            except ValueError:
                if j == 4:  # коэффициент d
                    func_params.append(1.0)
                elif j == 5:  # коэффициент e
                    func_params.append(0.0)
                else:
                    func_params.append(0.0)
        equations.append(func_params)
    
    return {
        "initial_equations": initial_equations,
        "faks": faks,
        "equations": equations,
        "restrictions": restrictions
    }

def clear_ecology_graphics():
    """Очистка старых графиков для модели экологии"""
    image_files = [
        "static/images/diagram_eco.png", 
        "static/images/diagram_eco2.png",
        "static/images/diagram_eco3.png", 
        "static/images/diagram_eco4.png", 
        "static/images/diagram_eco5.png", 
        "static/images/figure_eco.png",
        "static/images/disturbances_eco.png"
    ]
    
    cleared_files = []
    for file_path in image_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                cleared_files.append(file_path)
            except Exception as e:
                print(f"Ошибка при удалении {file_path}: {e}")
    
    return cleared_files

def generate_random_parameters():
    """
    Генерация случайных параметров для тестирования
    Возвращает словарь со всеми необходимыми параметрами
    """
    import random
    
    # Случайные начальные значения (0-1)
    initial_equations = [round(random.random() * 0.8 + 0.1, 2) for _ in range(5)]
    
    # Случайные предельные значения (0.5-1.0)
    restrictions = [round(random.random() * 0.5 + 0.5, 2) for _ in range(5)]
    
    # Случайные возмущения (14 x 4)
    faks = []
    for _ in range(14):
        fak_params = []
        # Для возмущений, зависящих от времени (первые 6)
        # делаем случайные коэффициенты, но d (свободный член) больше
        for j in range(4):
            if j == 3:  # коэффициент d (свободный член)
                fak_params.append(round(random.random() * 5 + 1, 2))
            else:
                fak_params.append(round(random.random() * 0.5 - 0.25, 2))
        faks.append(fak_params)
    
    # Случайные внутренние функции (12 x 5)
    equations = []
    for _ in range(12):
        func_params = []
        for j in range(5):
            if j == 3:  # коэффициент d (линейный)
                func_params.append(round(random.random() * 2 - 1, 2))
            elif j == 4:  # коэффициент e (свободный)
                func_params.append(round(random.random() * 0.5 - 0.25, 2))
            else:
                func_params.append(round(random.random() * 0.2 - 0.1, 2))
        equations.append(func_params)
    
    return {
        "initial_equations": initial_equations,
        "faks": faks,
        "equations": equations,
        "restrictions": restrictions
    }

def validate_inputs(initial_equations, faks, equations, restrictions):
    """
    Валидация входных данных
    Возвращает (is_valid, error_message)
    """
    try:
        # Проверка начальных условий (5 значений 0-1)
        if len(initial_equations) != 5:
            return False, "Должно быть 5 начальных значений"
        
        for i, val in enumerate(initial_equations):
            if not (0 <= val <= 1):
                return False, f"Начальное значение Cf{i+1} должно быть в диапазоне [0, 1]"
        
        # Проверка предельных значений (5 значений 0-1)
        if len(restrictions) != 5:
            return False, "Должно быть 5 предельных значений"
        
        for i, val in enumerate(restrictions):
            if not (0 <= val <= 1):
                return False, f"Предельное значение Cf{i+1} должно быть в диапазоне [0, 1]"
        
        # Проверка возмущений (14 x 4)
        if len(faks) != 14:
            return False, "Должно быть 14 возмущений"
        
        for i, fak in enumerate(faks):
            if len(fak) != 4:
                return False, f"Возмущение x{i+1} должно иметь 4 коэффициента"
        
        # Проверка внутренних функций (12 x 5)
        if len(equations) != 12:
            return False, "Должно быть 12 внутренних функций"
        
        for i, eq in enumerate(equations):
            if len(eq) != 5:
                return False, f"Функция f{i+1} должна иметь 5 коэффициентов"
        
        return True, "Данные корректны"
        
    except Exception as e:
        return False, f"Ошибка валидации: {str(e)}"

# Старые функции для совместимости (можно удалить после рефакторинга)
lines = (
    ('g', '-'), ('c', '-'), ('r', '-'), ('y', '-'), ('m', '-'),
    ('b', '-'), ('teal', '-'), ('gray', '-'), ('olive', '-'),
    ('g', '--'), ('c', '--'), ('r', '--'), ('y', '--'), ('m', '--'),
    ('b', '--'), ('teal', '--'), ('gray', '--'), ('olive', '--'),
    ('g', '-.'), ('c', '-.'), ('r', '-.'), ('y', '-.'), ('m', '-.')
)

def clear_graphics():
    """Старая функция для совместимости - очищает графики экологии"""
    return clear_ecology_graphics()

if __name__ == "__main__":
    # Тестирование функций
    print("Тестирование utils_ecology.py")
    
    # Генерация тестовых данных
    test_data = generate_random_parameters()
    print(f"Сгенерировано начальных значений: {len(test_data['initial_equations'])}")
    print(f"Сгенерировано возмущений: {len(test_data['faks'])}")
    print(f"Сгенерировано внутренних функций: {len(test_data['equations'])}")
    
    # Валидация
    is_valid, message = validate_inputs(
        test_data["initial_equations"],
        test_data["faks"],
        test_data["equations"],
        test_data["restrictions"]
    )
    
    print(f"Валидация: {is_valid}, сообщение: {message}")
    
    # Тест очистки графиков
    cleared = clear_ecology_graphics()
    print(f"Очищено файлов: {len(cleared)}")