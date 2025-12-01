const input = document.getElementById("status-input")
input.value = sessionStorage.getItem("status") || ""

// === НОВЫЕ ФУНКЦИИ ДЛЯ РАНДОМИЗАЦИИ ===
// ВСЕ значения должны быть в диапазоне [0, 1]
function randomInRange(min = 0, max = 1) {
    // Генерация числа в диапазоне [min, max]
    return Math.round((Math.random() * (max - min) + min) * 100) / 100
}

function randomCf() {
    // Для Cf1-Cf5: 0 до 1
    return randomInRange(0, 1)
}

function randomCoefficientPositive() {
    // Для коэффициентов полиномов: только положительные 0-1
    return randomInRange(0, 1)
}

function randomCoefficientSmall() {
    // Для старших коэффициентов: маленькие положительные
    return randomInRange(0.01, 0.3)
}

function randomTime() {
    // Время t: только указанные значения
    const times = [0, 0.25, 0.5, 0.75, 1]
    return times[Math.floor(Math.random() * times.length)]
}

function randomLinearCoefficient() {
    // Линейные коэффициенты (c): 0-1 (ранее было 0.1-3)
    return randomInRange(0, 1)
}

function randomConstantCoefficient() {
    // Свободные члены (d): 0-1 (ранее было 1-6)
    return randomInRange(0, 1)
}

// === ИСПРАВЛЕННАЯ refill() ===
function refill() {
    // Заполнение времени (только указанные значения)
    let timeValue = randomTime()
    document.getElementById("time-value").value = timeValue
    sessionStorage.setItem("time-value", timeValue)
    
    // Генерируем сначала пределы (0.6-1.0)
    const limits = []
    for (let i=1; i<6; i++) {
        limits[i-1] = randomInRange(0.6, 1.0)
    }
    
    // Заполнение возмущений (14 x 4) - ТОЛЬКО [0, 1]
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let value
            if (i <= 6) {
                // x₁-x₆: зависят от времени
                if (j === 1 || j === 2) {
                    // a,b: старшие коэффициенты (маленькие положительные)
                    value = randomCoefficientSmall()
                } else if (j === 3) {
                    // c: линейный коэффициент по t
                    value = randomLinearCoefficient()  // 0-1
                } else {
                    // d: свободный член
                    value = randomConstantCoefficient()  // 0-1
                }
            } else {
                // x₇-x₁₄: зависят от концентрации
                if (j === 1 || j === 2) {
                    // a,b: старшие коэффициенты (маленькие положительные)
                    value = randomCoefficientSmall()
                } else if (j === 3) {
                    // c: линейный коэффициент по C
                    value = randomLinearCoefficient()  // 0-1
                } else {
                    // d: свободный член
                    value = randomConstantCoefficient()  // 0-1
                }
            }
            
            sessionStorage.setItem("faks-" + i + "-" + j, value)
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) el.value = value
        }
    }

    // Заполнение начальных условий (5 значений) - меньше пределов, но в [0, 1]
    for (let i=1; i<6; i++) {
        const limit = limits[i-1]
        let value = randomInRange(0, limit)  // от 0 до предела, но предел уже в [0.6, 1.0]
        sessionStorage.setItem("init-eq-" + i, value)
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = value
    }

    // Заполнение предельных значений (0.6-1.0)
    for (let i=1; i<6; i++) {
        const limit = limits[i-1]
        sessionStorage.setItem("restrictions-" + i, limit)
        let el = document.getElementById("restrictions-" + i)
        if (el) el.value = limit
    }

    // Заполнение внутренних функций (12 x 5) - ВСЕ значения в [0, 1]
    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let value
            if (j === 4) {
                // d: линейный коэффициент (0-1)
                value = randomInRange(0, 1)
            } else if (j === 5) {
                // e: свободный член (0-0.5)
                value = randomInRange(0, 0.5)
            } else {
                // a,b,c: старшие коэффициенты (маленькие положительные)
                value = randomCoefficientSmall()
            }
            
            // Убедимся, что значение точно в [0, 1]
            value = Math.min(Math.max(value, 0), 1)
            value = Math.round(value * 100) / 100
            
            sessionStorage.setItem("equations-" + i + "-" + j, value)
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) el.value = value
        }
    }
    
    sessionStorage.removeItem("status")
    input.value = "Заполнено случайными значениями (t=" + timeValue + ")"
}

// === ИСПРАВЛЕННАЯ clearAll() ===
function clearAll() {
    // Очистка времени
    document.getElementById("time-value").value = "0.0"
    sessionStorage.setItem("time-value", "0.0")
    
    // Очистка возмущений (14 x 4) - значения в [0, 1]
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let defaultValue = "0.1"
            if (j === 3) defaultValue = "0.5"  // линейный коэффициент
            if (j === 4) defaultValue = "0.3"  // свободный член
            
            sessionStorage.setItem("faks-" + i + "-" + j, defaultValue)
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) el.value = defaultValue
        }
    }

    // Очистка начальных условий (5 значений) - 0.5
    for (let i=1; i<6; i++) {
        sessionStorage.setItem("init-eq-" + i, "0.5")
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = "0.5"
    }

    // Очистка предельных значений - 1.0
    for (let i=1; i<6; i++) {
        sessionStorage.setItem("restrictions-" + i, "1.0")
        let el = document.getElementById("restrictions-" + i)
        if (el) el.value = "1.0"
    }

    // Очистка внутренних функций (12 x 5) - значения в [0, 1]
    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let defaultValue = "0.1"
            if (j === 4) defaultValue = "0.5"  // линейный коэффициент
            if (j === 5) defaultValue = "0.2"  // свободный член
            
            sessionStorage.setItem("equations-" + i + "-" + j, defaultValue)
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) el.value = defaultValue
        }
    }
    
    sessionStorage.removeItem("status")
    input.value = "Очищено (t=0.0)"
}

// === ЗАГРУЗКА СОХРАНЕННЫХ ЗНАЧЕНИЙ ===
if (input.value !== "Выполнено") {
    refill()
} else {
    // Загрузка сохраненных значений
    const savedTime = sessionStorage.getItem("time-value")
    if (savedTime) {
        document.getElementById("time-value").value = savedTime
    }
    
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("faks-" + i + "-" + j) || "0.1"
            }
        }
    }

    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) {
            el.value = sessionStorage.getItem("init-eq-" + i) || "0.5"
        }
    }
    
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) {
            el.value = sessionStorage.getItem("restrictions-" + i) || "1.0"
        }
    }

    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("equations-" + i + "-" + j) || "0.1"
            }
        }
    }
}

// === ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ===
function getFaks() {
    const faks = []
    for (let i=1; i<15; i++) {
        const temp = []
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) temp.push(el.value || "0.1")
        }
        faks.push(temp)
    }
    return faks
}

function getInitialEquations() {
    const init_eq = []
    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) init_eq.push(el.value || "0.5")
    }
    return init_eq
}

function getRestrictions() {
    const restrictions = []
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) restrictions.push(el.value || "1.0")
    }
    return restrictions
}

function getEquations() {
    const equations = []
    for (let i=1; i<13; i++) {
        const temp = []
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) temp.push(el.value || "0.1")
        }
        equations.push(temp)
    }
    return equations
}

// === ФУНКЦИЯ PROCESS() ===
async function process() {
    const faks = getFaks()
    const init_eq = getInitialEquations()
    const restrictions = getRestrictions()
    const equations = getEquations()
    const timeValue = document.getElementById("time-value").value || "0.0"

    // Проверка начальных значений ≤ пределов
    let isValid = true
    for (let i=0; i<5; i++) {
        const initVal = parseFloat(init_eq[i])
        const limitVal = parseFloat(restrictions[i])
        if (initVal > limitVal) {
            alert(`Ошибка: Начальное значение Cf${i+1} (${initVal}) превышает предел (${limitVal})`)
            isValid = false
            break
        }
    }
    
    if (!isValid) return

    // Сохранение в sessionStorage
    sessionStorage.setItem("time-value", timeValue)
    
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) sessionStorage.setItem("faks-" + i + "-" + j, el.value)
        }
    }

    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) sessionStorage.setItem("init-eq-" + i, el.value)
    }
    
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) sessionStorage.setItem("restrictions-" + i, el.value)
    }

    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) sessionStorage.setItem("equations-" + i + "-" + j, el.value)
        }
    }

    try {
        const response = await fetch('/draw_graphics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "faks": faks,
                "initial_equations": init_eq,
                "restrictions": restrictions,
                "equations": equations,
                "time_value": timeValue
            })
        })

        const result = await response.json()
        input.value = result.status + " (t=" + timeValue + ")"
        sessionStorage.setItem("status", result.status)
        
        // Автоматическое обновление через 1 секунду
        setTimeout(() => {
            window.location.reload()
        }, 1000)
    } catch (error) {
        input.value = "Ошибка соединения"
        console.error("Error:", error)
    }
}

// Загрузка сохраненного времени при загрузке страницы
const timeInput = document.getElementById("time-value")
if (timeInput) {
    const savedTime = sessionStorage.getItem("time-value")
    if (savedTime) {
        timeInput.value = savedTime
    }
}