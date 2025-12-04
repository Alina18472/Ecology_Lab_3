# utils.py - исправленная версия
import os
import random

def get_faks_from_inputs(ui):
    """
    Получение коэффициентов для 14 возмущений
    Теперь каждый возмущение имеет 2 коэффициента: a, b для линейной функции
    """
    result = []
    
    for fak_num in range(1, 15):  
        params = []
        for param_num in range(1, 3): 
            try:
                element_id = f"faks-{fak_num}-{param_num}"
                value = float(getattr(ui, f"lineEdit_{element_id}").text())
                params.append(value)
            except (AttributeError, ValueError, KeyError):
                params.append(0.0)
        
        result.append(params)
    
    return result

def get_equations_from_inputs(ui):
    result = []
 
    params = []
    for param_num in range(1, 3):  # a, b
        try:
            element_id = f"equations-1-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.5 if param_num == 1 else 0.5)
    result.append(params)
    
    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-2-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.3 if param_num == 1 else 15.0)
    result.append(params)

    params = []
    for param_num in range(1, 4):
        try:
            element_id = f"equations-3-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            if param_num == 1: params.append(0.3)
            elif param_num == 2: params.append(0.4)
            else: params.append(0.5)
    result.append(params)
    

    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-4-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.7 if param_num == 1 else 11.0)
    result.append(params)

    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-5-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.8 if param_num == 1 else 9.0)
    result.append(params)
 
    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-6-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.8 if param_num == 1 else 12.0)
    result.append(params)
    
 
    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-7-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.8 if param_num == 1 else 11.0)
    result.append(params)
    

    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-8-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.7 if param_num == 1 else 13.0)
    result.append(params)
    

    result.append([10.0, 5.0])
    

    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-10-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.55 if param_num == 1 else 13.0)
    result.append(params)
    

    params = []
    for param_num in range(1, 4):
        try:
            element_id = f"equations-11-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            if param_num == 1: params.append(0.55)
            elif param_num == 2: params.append(12.0)
            else: params.append(2.0)
    result.append(params)
    

    params = []
    for param_num in range(1, 3):
        try:
            element_id = f"equations-12-{param_num}"
            value = float(getattr(ui, f"lineEdit_{element_id}").text())
            params.append(value)
        except:
            params.append(0.5 if param_num == 1 else 3.0)
    result.append(params)
    
    return result

def validate_inputs(initial_equations, faks, equations, restrictions):

    try:
  
        if len(initial_equations) != 5:
            return False, "Должно быть 5 начальных значений"
        
        for i, val in enumerate(initial_equations):
            if not (0 <= val <= 1):
                return False, f"Начальное значение Cf{i+1} должно быть в диапазоне [0, 1]"
        
        if len(restrictions) != 5:
            return False, "Должно быть 5 предельных значений"
        
        for i, val in enumerate(restrictions):
            if not (0 <= val <= 1):
                return False, f"Предельное значение Cf{i+1} должно быть в диапазоне [0, 1]"

        if len(faks) != 14:
            return False, "Должно быть 14 возмущений"
        
        for i, fak in enumerate(faks):
            if len(fak) != 2:
                return False, f"Возмущение x{i+1} должно иметь 2 коэффициента (a и b)"
        
     
        if len(equations) != 12:
            return False, "Должно быть 12 внутренних функций"
 
        expected_lengths = [2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2]
        for i, eq in enumerate(equations):
            if i < len(expected_lengths) and len(eq) != expected_lengths[i]:
                return False, f"Функция f{i+1} должна иметь {expected_lengths[i]} коэффициента(ов)"
        
        return True, "Данные корректны"
        
    except Exception as e:
        return False, f"Ошибка валидации: {str(e)}"