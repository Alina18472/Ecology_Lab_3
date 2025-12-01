import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import logging

from functions import pend, calculate_total_loss
from radar_diagram import RadarDiagram

data_sol = []
logger = logging.getLogger(__name__)


def fill_diagrams(data, initial_equations, restrictions):
    """
    Создание радар-диаграмм для различных концентраций
    data - решения системы [Cf1, Cf2, Cf3, Cf4, Cf5] для разных C
    initial_equations - начальные значения
    restrictions - предельные значения
    """
    radar = RadarDiagram()
    
    clipped_initial = np.clip(initial_equations, 0, 1.0)
    clipped_data = np.clip(data, 0, 1.0)
    clipped_restrictions = np.clip(restrictions, 0, 1.0)

    # Индексы для различных концентраций (C от 0 до 1)
    conc_indices = [
        0,                    # C = 0
        int(len(data) / 4),   # C = 0.25
        int(len(data) / 2),   # C = 0.5
        int(3 * len(data) / 4), # C = 0.75
        -1                    # C = 1.0
    ]
    
    titles = [
        "Потери при C = 0 (начальная концентрация)",
        "Потери при C = 0.25",
        "Потери при C = 0.5", 
        "Потери при C = 0.75",
        "Потери при C = 1.0 (максимальная концентрация)"
    ]
    
    filenames = [
        './static/images/diagram_eco.png',
        './static/images/diagram_eco2.png',
        './static/images/diagram_eco3.png',
        './static/images/diagram_eco4.png',
        './static/images/diagram_eco5.png'
    ]

    for i, (idx, title, fname) in enumerate(zip(conc_indices, titles, filenames)):
        current_vals = clipped_data[idx]
        
        if i == 0:
            radar.draw(
                filename=fname,
                initial_data=clipped_initial,
                current_data=current_vals,
                label="",
                title=title,
                restrictions=clipped_restrictions,
                show_both_lines=False
            )
        else:
            radar.draw(
                filename=fname,
                initial_data=clipped_initial,
                current_data=current_vals,
                label="",
                title=title,
                restrictions=clipped_restrictions,
                show_both_lines=True
            )


def create_graphic(C, data):
    """
    Создание графика потерь от концентрации
    C - массив значений концентрации от 0 до 1
    data - массив решений [Cf1, Cf2, Cf3, Cf4, Cf5] для каждой концентрации
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 16))
    
    labels = [
        "Cf1 - Потери от заболеваемости населения",
        "Cf2 - Потери сельского хозяйства", 
        "Cf3 - Потери от изменения природной среды",
        "Cf4 - Потери от ухудшения качества жизни",
        "Cf5 - Потери предприятия"
    ]
    
    line_labels = ["Cf1", "Cf2", "Cf3", "Cf4", "Cf5"]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # График 1: Cf1, Cf2, Cf3
    for i in range(3):
        y_data = np.clip(data[:, i], 0, 1.0)
        ax1.plot(C, y_data, color=colors[i], linewidth=2.5, label=labels[i])
        
        mid_idx = len(C) // 2
        if mid_idx > 0:
            ax1.text(C[mid_idx], y_data[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=9, va='center', ha='left',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1.0])
    ax1.set_ylabel("Значения потерь", fontsize=14, fontweight='bold')
    ax1.set_title("График 1: Потери от загрязнения атмосферы (Cf1-Cf3)", fontsize=16, fontweight='bold', pad=20)
    ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=12)
    
    ax1.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1, label='Предел')
    
    # График 2: Cf4, Cf5 и суммарные потери
    for i in range(3, 5):
        y_data = np.clip(data[:, i], 0, 1.0)
        ax2.plot(C, y_data, color=colors[i], linewidth=2.5, label=labels[i])
        
        mid_idx = len(C) // 2
        if mid_idx > 0:
            ax2.text(C[mid_idx], y_data[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=9, va='center', ha='left',
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Расчет и отрисовка суммарных потерь
    total_loss = []
    for row in data:
        total_loss.append(calculate_total_loss(row))
    
    total_loss_norm = np.clip(total_loss, 0, 1.0)
    ax2.plot(C, total_loss_norm, color='black', linewidth=3, linestyle='--', 
             label='Суммарные потери (нормированные)')
    
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1.0])
    ax2.set_xlabel("C, концентрация загрязняющих веществ", fontsize=14, fontweight='bold')
    ax2.set_ylabel("Значения потерь", fontsize=14, fontweight='bold')
    ax2.set_title("График 2: Потери от загрязнения атмосферы (Cf4-Cf5 и суммарные)", 
                  fontsize=16, fontweight='bold', pad=20)
    ax2.legend(loc='upper left', fontsize=12, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(axis='both', which='major', labelsize=12)
    
    ax2.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1, label='Предел')
    
    plt.tight_layout(pad=3.0)
    fig.savefig('./static/images/figure_eco.png', bbox_inches='tight', dpi=150)
    plt.close(fig)


def cast_to_float(initial_equations, faks, equations, restrictions):
    """
    Преобразование всех входных данных в float
    """
    for i in range(len(initial_equations)):
        initial_equations[i] = float(initial_equations[i])

    for i in range(len(faks)):
        for j in range(len(faks[i])):
            faks[i][j] = float(faks[i][j])

    for i in range(len(equations)):
        for j in range(len(equations[i])):
            equations[i][j] = float(equations[i][j])

    for i in range(len(restrictions)):
        restrictions[i] = float(restrictions[i])

    return initial_equations, faks, restrictions


def process(initial_equations, faks, equations, restrictions):
    """
    Основная функция обработки данных и создания графиков
    initial_equations - начальные значения Cf [Cf1(0), Cf2(0), Cf3(0), Cf4(0), Cf5(0)]
    faks - коэффициенты возмущений [14 x 4]
    equations - коэффициенты внутренних функций [12 x 5]
    restrictions - предельные значения [5]
    """
    global data_sol

    # Преобразование строк в числа
    initial_equations, faks, restrictions = cast_to_float(initial_equations, faks, equations, restrictions)
    
    # Диапазон концентрации от 0 до 1
    C = np.linspace(0, 1, 100)
    
    # Масштабирующие коэффициенты (максимальные значения)
    # Из документа: 1/max Cf_i - нормировочные множители
    xm = [1.0, 1.0, 1.0, 1.0, 1.0]  # По умолчанию 1.0, можно настраивать

    # Решение системы дифференциальных уравнений
    # Используем концентрацию C как независимую переменную
    data_sol = odeint(pend, initial_equations, C, args=(faks, equations, xm))
    
    # Ограничение значений в диапазоне [0, 1]
    data_sol = np.clip(data_sol, 1e-3, 1.0)
    
    # Создание графиков
    create_graphic(C, data_sol)
    create_disturbances_graphic(C, faks)  
    fill_diagrams(data_sol, initial_equations, restrictions)
    
    # Дополнительная информация для логов
    logger.info(f"Расчет завершен. Концентрация: {len(C)} точек.")
    logger.info(f"Начальные значения: {initial_equations}")
    logger.info(f"Конечные значения при C=1: {data_sol[-1]}")
    
    # Расчет суммарных потерь при максимальной концентрации
    total_loss_max = calculate_total_loss(data_sol[-1])
    logger.info(f"Суммарные потери при C=1: {total_loss_max:.4f}")


# Описания характеристик для интерфейса
u_list = [
    "Cf1 - Потери, связанные с ростом заболеваемости населения",
    "Cf2 - Потери сельского хозяйства от воздействия атмосферных поллютантов",
    "Cf3 - Потери от изменения природной среды",
    "Cf4 - Потери из-за ухудшения качества жизни населения",
    "Cf5 - Потери предприятия, возникающие при регулировании атмосферных выбросов и оплате штрафов"
]


def create_disturbances_graphic(C, faks):
    """
    Создание графиков возмущений
    C - массив концентраций
    faks - коэффициенты возмущений
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
    
    # === ВОЗМУЩЕНИЯ, ЗАВИСЯЩИЕ ОТ ВРЕМЕНИ (ПЕРВЫЕ 6) ===
    time_dependent_labels = [
        "x1(t) - Износ технологического оборудования",
        "x2(t) - Возможность использования кредитных ресурсов", 
        "x3(t) - Привлечение зарубежных инвесторов",
        "x4(t) - Спрос на продукцию предприятия",
        "x5(t) - Сложность найма сотрудников",
        "x6(t) - Деловая репутация компании"
    ]
    
    colors_time = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Для возмущений, зависящих от времени, используем постоянные значения
    for i in range(min(6, len(faks))):
        # Берем свободный член (params[3]) как постоянное значение
        if len(faks[i]) > 3:
            constant_val = faks[i][3]
        else:
            constant_val = 0.0
            
        ax1.axhline(y=constant_val, color=colors_time[i], linewidth=2.5, 
                   label=f"{time_dependent_labels[i]} = {constant_val:.2f}")
    
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 10])
    ax1.set_ylabel("Значение возмущения", fontsize=12, fontweight='bold')
    ax1.set_title("Возмущения, зависящие от времени (постоянные на интервале)", 
                 fontsize=14, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=10)
    
    # === ВОЗМУЩЕНИЯ, ЗАВИСЯЩИЕ ОТ КОНЦЕНТРАЦИИ (ПОСЛЕДНИЕ 8) ===
    conc_dependent_labels = [
        "x7(C) - Повышенный уровень смога",
        "x8(C) - Высокая задымленность от лесных пожаров",
        "x9(C) - Продолжительный летний антициклон",
        "x10(C) - Продолжительный зимний антициклон",
        "x11(C) - Высокая загруженность автомагистралей",
        "x12(C) - Наличие крупных промышленных предприятий",
        "x13(C) - Эпидемиологическая ситуация",
        "x14(C) - Наличие санкций"
    ]
    
    colors_conc = ['#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 
                   '#ff1493', '#00ced1', '#ff7f0e', '#2ca02c']
    
    # Функция для вычисления полинома 3-й степени
    def f3(x, params):
        if len(params) >= 4:
            return params[0] * x**3 + params[1] * x**2 + params[2] * x + params[3]
        elif len(params) == 3:
            return params[0] * x**2 + params[1] * x + params[2]
        elif len(params) == 2:
            return params[0] * x + params[1]
        elif len(params) == 1:
            return params[0]
        else:
            return 0.0
    
    # Отрисовка возмущений, зависящих от концентрации
    for i in range(6, min(14, len(faks))):
        if i < len(faks) and len(faks[i]) > 0:
            # Вычисляем значения для каждой концентрации C
            curve = []
            for c_val in C:
                curve.append(f3(c_val, faks[i]))
            
            curve = np.clip(curve, 0, 10)
            label_idx = i - 6
            if label_idx < len(conc_dependent_labels):
                ax2.plot(C, curve, color=colors_conc[label_idx], linewidth=2.5, 
                        label=conc_dependent_labels[label_idx])
    
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 10])
    ax2.set_xlabel("C, концентрация загрязняющих веществ", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Значение возмущения", fontsize=12, fontweight='bold')
    ax2.set_title("Возмущения, зависящие от концентрации загрязняющих веществ", 
                 fontsize=14, fontweight='bold', pad=10)
    ax2.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.tick_params(axis='both', which='major', labelsize=10)
    
    plt.tight_layout()
    fig.savefig('./static/images/disturbances_eco.png', bbox_inches='tight', dpi=150)
    plt.close(fig)


def get_scenario_data(scenario_name="default"):
    """
    Получение тестовых данных для различных сценариев из документа
    """
    scenarios = {
        "default": {
            "initial_equations": [0.5, 0.7, 0.9, 0.4, 0.5],
            "faks": [
                [0, 0, 0, 2.0],     # x1(t) = 2
                [0, 0, 0, 2.2],     # x2(t) = 2.2
                [0, 0, 0, 0.0],     # x3(t) = 0
                [0, 0, 0, 4.0],     # x4(t) = 4
                [0, 0, 0, 3.0],     # x5(t) = 3
                [0, 0, 0, 2.0],     # x6(t) = 2
                [0, 0, 7, 5],       # x7(C) = 7C + 5
                [0, 0, 0, 0],       # x8(C) = 0
                [0, 0, 0.6, 3],     # x9(C) = 0.6C + 3
                [0, 0, 0.7, 4],     # x10(C) = 0.7C + 4
                [0, 0, 3, 5],       # x11(C) = 3C + 5
                [0, 0, 3.2, 3],     # x12(C) = 3.2C + 3
                [0, 0, 3.3, 4],     # x13(C) = 3.3C + 4
                [0, 0, 2, 5]        # x14(C) = 2C + 5
            ],
            "equations": [
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f1(Cf3) - простая линейная
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f2(Cf4)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f3(Cf5)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f4(Cf3)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f5(Cf4)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f6(Cf5)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f7(Cf5)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f8(Cf1)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f9(Cf2)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f10(Cf3)
                [0.0, 0.0, 0.0, 1.0, 0.0],  # f11(Cf5)
                [0.0, 0.0, 0.0, 1.0, 0.0]   # f12(Cf1)
            ],
            "restrictions": [1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "test_scenario": {
            "initial_equations": [0.3, 0.5, 0.7, 0.2, 0.4],
            "faks": [
                [0, 0, 0, 1.5], [0, 0, 0, 1.8], [0, 0, 0, 0.5],
                [0, 0, 0, 3.0], [0, 0, 0, 2.0], [0, 0, 0, 1.5],
                [0.1, 0, 5, 4], [0, 0, 0, 0], [0, 0.2, 0, 2.5],
                [0, 0.3, 0, 3], [0.2, 0, 2, 4], [0.1, 0, 2.5, 2],
                [0.3, 0, 2, 3], [0.1, 0, 1.5, 4]
            ],
            "equations": [
                [0.0, 0.0, 0.1, 0.8, 0.0],
                [0.0, 0.0, 0.2, 0.7, 0.0],
                [0.0, 0.0, 0.0, 0.9, 0.0],
                [0.0, 0.0, 0.1, 0.8, 0.0],
                [0.0, 0.0, 0.2, 0.7, 0.0],
                [0.0, 0.0, -0.1, 0.9, 0.0],
                [0.0, 0.0, -0.2, 1.0, 0.0],
                [0.0, 0.0, 0.3, 0.6, 0.0],
                [0.0, 0.0, 0.2, 0.7, 0.0],
                [0.0, 0.0, 0.1, 0.8, 0.0],
                [0.0, 0.0, -0.3, 1.1, 0.0],
                [0.0, 0.0, 0.4, 0.5, 0.0]
            ],
            "restrictions": [0.9, 0.9, 0.9, 0.9, 0.9]
        }
    }
    
    return scenarios.get(scenario_name, scenarios["default"])


if __name__ == "__main__":
    # Тестирование модуля
    print("Тестирование модуля process_ecology.py")
    
    # Получение тестовых данных
    test_data = get_scenario_data("default")
    
    print(f"Начальные значения: {test_data['initial_equations']}")
    print(f"Количество возмущений: {len(test_data['faks'])}")
    print(f"Количество внутренних функций: {len(test_data['equations'])}")
    
    # Тестовый вызов process
    process(
        test_data["initial_equations"].copy(),
        test_data["faks"].copy(),
        test_data["equations"].copy(),
        test_data["restrictions"].copy()
    )
    
    print("Тест завершен. Проверьте папку static/images на наличие созданных графиков.")