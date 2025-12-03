# process_ecology.py - чистая версия без тестовых данных
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import logging

from functions import pend, calculate_total_loss, fx_linear  # ИМПОРТИРУЕМ fx_linear
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
        "Характеристики при C = 0 (начальная концентрация)",
        "Характеристики при C = 0.25",
        "Характеристики при C = 0.5", 
        "Характеристики при C = 0.75",
        "Характеристики при C = 1.0 (максимальная концентрация)"
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
    Создание единого графика характеристик от концентрации
    C - массив значений концентрации от 0 до 1
    data - массив решений [Cf1, Cf2, Cf3, Cf4, Cf5] для каждой концентрации
    """
    fig, ax = plt.subplots(figsize=(20, 10))  # Один график
    
    labels = [
        "Cf₁ - Потери от заболеваемости населения",
        "Cf₂ - Потери сельского хозяйства", 
        "Cf₃ - Потери от изменения природной среды",
        "Cf₄ - Потери от ухудшения качества жизни",
        "Cf₅ - Потери предприятия"
    ]
    
    line_labels = ["Cf₁", "Cf₂", "Cf₃", "Cf₄", "Cf₅"]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Отображаем все 5 характеристик на одном графике
    for i in range(5):
        y_data = np.clip(data[:, i], 0, 1.0)
        ax.plot(C, y_data, color=colors[i], linewidth=2.5, label=labels[i])
        
        # Добавляем тонкие подписи к линиям (без белого фона)
        mid_idx = len(C) // 2
        if mid_idx > 0:
            ax.text(C[mid_idx], y_data[mid_idx], f' {line_labels[i]}', 
                    color=colors[i], fontsize=10, va='center', ha='left')
    
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.0])
    ax.set_xlabel("C, концентрация загрязняющих веществ", fontsize=14, fontweight='bold')
    ax.set_ylabel("Значения характеристик", fontsize=14, fontweight='bold')
    ax.set_title("График характеристик от концентрации загрязняющих веществ", 
                 fontsize=16, fontweight='bold', pad=20)
    
    # ЛЕГЕНДА В ЛЕВОМ ВЕРХНЕМ УГЛУ
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9, 
               edgecolor='gray', fancybox=True)
    
    # Сетка
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Предельная линия
    ax.axhline(y=1.0, color='red', linestyle=':', alpha=0.7, linewidth=1.5, label='Предел')
    
    # Улучшаем внешний вид
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout(pad=3.0)
    fig.savefig('./static/images/figure_eco.png', bbox_inches='tight', dpi=150)
    plt.close(fig)


def cast_to_float(initial_equations, faks, equations, restrictions):
    """
    Преобразование всех входных данных в float
    ВАЖНО: equations (параметры внутренних функций) тоже преобразуются!
    """
    # Преобразуем начальные условия
    for i in range(len(initial_equations)):
        initial_equations[i] = float(initial_equations[i])

    # Преобразуем коэффициенты возмущений
    for i in range(len(faks)):
        for j in range(len(faks[i])):
            faks[i][j] = float(faks[i][j])

    # Преобразуем параметры внутренних функций (ВАЖНО!)
    for i in range(len(equations)):
        for j in range(len(equations[i])):
            equations[i][j] = float(equations[i][j])

    # Преобразуем предельные значения
    for i in range(len(restrictions)):
        restrictions[i] = float(restrictions[i])

    return initial_equations, faks, equations, restrictions


def process(initial_equations, faks, equations, restrictions, time_value=0.0):
    """
    Основная функция обработки данных и создания графиков
    initial_equations - начальные значения Cf [Cf1(0), Cf2(0), Cf3(0), Cf4(0), Cf5(0)]
    faks - коэффициенты возмущений [14 x 2] - ТОЛЬКО a и b для линейных функций
    equations - коэффициенты внутренних функций [12 x ...] - ТЕПЕРЬ ИСПОЛЬЗУЕТСЯ!
    restrictions - предельные значения [5]
    time_value - значение времени t для возмущений x1-x6
    """
    global data_sol

    # Преобразование строк в числа (ВСЕХ параметров!)
    initial_equations, faks, equations, restrictions = cast_to_float(
        initial_equations, faks, equations, restrictions
    )
    time_value = float(time_value)
    
    # Логирование полученных параметров для отладки
    logger.info(f"Параметры внутренних функций получены с интерфейса:")
    for i, eq_params in enumerate(equations):
        if eq_params:  # Проверяем, что список не пустой
            logger.info(f"  f{i+1}: {eq_params}")
    
    # Диапазон концентрации от 0 до 1
    C = np.linspace(0, 1, 100)
    
    # Масштабирующие коэффициенты (максимальные значения)
    xm = [1.0, 1.0, 1.0, 1.0, 1.0]  # По умолчанию 1.0

    # Решение системы дифференциальных уравнений
    # ВАЖНО: передаем equations (параметры внутренних функций) в pend()
    data_sol = odeint(pend, initial_equations, C, args=(faks, equations, xm, time_value))
    
    # Ограничение значений в диапазоне [0, 1]
  
    data_sol = np.clip(data_sol, 0.0, 1.0) 
    # Создание графиков
    create_graphic(C, data_sol)
    create_disturbances_graphic(C, faks, time_value)  
    fill_diagrams(data_sol, initial_equations, restrictions)
    
    # Дополнительная информация для логов
    logger.info(f"Расчет завершен. Концентрация: {len(C)} точек, время t={time_value}.")
    logger.info(f"Начальные значения: {initial_equations}")
    logger.info(f"Конечные значения при C=1: {data_sol[-1]}")
    
    # Вычисление значений возмущений в момент времени t
    logger.info("Значения возмущений x1-x6 в момент времени t=" + str(time_value) + ":")
    for i in range(min(6, len(faks))):
        value = fx_linear(time_value, faks[i])
        logger.info(f"  x{i+1}(t) = {value:.4f}")


# Описания характеристик для интерфейса
u_list = [
    "Cf₁ - Потери, связанные с ростом заболеваемости населения",
    "Cf₂ - Потери сельского хозяйства от воздействия атмосферных поллютантов",
    "Cf₃ - Потери от изменения природной среды",
    "Cf₄ - Потери из-за ухудшения качества жизни населения",
    "Cf₅ - Потери предприятия, возникающие при регулировании атмосферных выбросов и оплате штрафов"
]


def create_disturbances_graphic(C, faks, time_value=0.0):
    """
    Создание графиков возмущений
    C - массив концентраций
    faks - коэффициенты возмущений [14 x 2] - линейные функции
    time_value - значение времени t для x1-x6
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
    
    # === ВОЗМУЩЕНИЯ, ЗАВИСЯЩИЕ ОТ ВРЕМЕНИ (ПЕРВЫЕ 6) ===
    time_dependent_labels = [
        "x₁(t) - Износ технологического оборудования",
        "x₂(t) - Возможность использования кредитных ресурсов", 
        "x₃(t) - Привлечение зарубежных инвесторов",
        "x₄(t) - Спрос на продукцию предприятия",
        "x₅(t) - Сложность найма сотрудников",
        "x₆(t) - Деловая репутация компании"
    ]
    
    colors_time = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Для возмущений, зависящих от времени, вычисляем значение в момент времени t
    for i in range(min(6, len(faks))):
        if len(faks[i]) >= 2:
            value = fx_linear(time_value, faks[i])
            
            # Формируем уравнение для линейной функции
            eq_str = " = a·t + b"
            
            # Рисуем горизонтальную линию
            ax1.axhline(y=value, color=colors_time[i], linewidth=2.5, 
                       label=f"x{i+1}(t){eq_str}")
            
            # Добавляем тонкую подпись на линии (без белого фона)
            ax1.text(0.5, value, f' x{i+1}', color=colors_time[i], fontsize=9, 
                    va='center', ha='left')
    
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 10])
    ax1.set_ylabel("Значение возмущения", fontsize=12, fontweight='bold')
    ax1.set_title(f"Возмущения, зависящие от времени (t = {time_value:.2f})", 
                 fontsize=14, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', which='major', labelsize=10)
    
    # === ВОЗМУЩЕНИЯ, ЗАВИСЯЩИЕ ОТ КОНЦЕНТРАЦИИ (ПОСЛЕДНИЕ 8) ===
    conc_dependent_labels = [
        "x₇(C) - Повышенный уровень смога",
        "x₈(C) - Высокая задымленность от лесных пожаров",
        "x₉(C) - Продолжительный летний антициклон",
        "x₁₀(C) - Продолжительный зимний антициклон",
        "x₁₁(C) - Высокая загруженность автомагистралей",
        "x₁₂(C) - Наличие крупных промышленных предприятий",
        "x₁₃(C) - Эпидемиологическая ситуация",
        "x₁₄(C) - Наличие санкций"
    ]
    
    colors_conc = ['#e377c2', '#7f7f7f', '#bcbd22', '#17becf', 
                   '#ff1493', '#00ced1', '#ff7f0e', '#2ca02c']
    
    # Отрисовка возмущений, зависящих от концентрации
    for i in range(6, min(14, len(faks))):
        if i < len(faks) and len(faks[i]) >= 2:
            # Вычисляем значения для каждой концентрации C
            curve = []
            for c_val in C:
                curve.append(fx_linear(c_val, faks[i]))
            
            curve = np.clip(curve, 0, 10)
            label_idx = i - 6
            if label_idx < len(conc_dependent_labels):
                # Формируем уравнение для линейной функции
                eq_str = " = a·C + b"
                
                # Рисуем кривую
                ax2.plot(C, curve, color=colors_conc[label_idx], linewidth=2.5, 
                        label=f"x{i+1}(C){eq_str}")
                
                # Добавляем тонкую подпись на линии
                mid_idx = len(C) // 2
                if mid_idx < len(curve):
                    ax2.text(C[mid_idx], curve[mid_idx], f' x{i+1}', 
                            color=colors_conc[label_idx], fontsize=9, 
                            va='center', ha='left')
    
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

