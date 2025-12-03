// script.js - обновленная версия
const input = document.getElementById("status-input")
input.value = sessionStorage.getItem("status") || ""

// === НОВЫЕ ФУНКЦИИ ДЛЯ РАНДОМИЗАЦИИ ===
function randomInRange() {
    // Генерация числа в диапазоне (0,1) - не включая 0 и 1
    let value
    do {
        value = Math.round(Math.random() * 100) / 100
    } while (value <= 0 || value >= 1)
    return value
}

function randomTime() {
    const times = [0, 0.25, 0.5, 0.75, 1]
    return times[Math.floor(Math.random() * times.length)]
}

// === ИСПРАВЛЕННАЯ refill() ===
function refill() {
    // Заполнение времени
    let timeValue = randomTime()
    document.getElementById("time-value").value = timeValue
    sessionStorage.setItem("time-value", timeValue)
    
    // Заполнение пределов (0,1) - не включая 0 и 1
    const limits = []
    for (let i=1; i<6; i++) {
        limits[i-1] = randomInRange()
    }
    
    // Заполнение возмущений (14 x 2) - ВСЕ в диапазоне (0,1)
    for (let i=1; i<15; i++) {
        // Коэффициент a
        let aValue = randomInRange()
        sessionStorage.setItem("faks-" + i + "-1", aValue)
        let elA = document.getElementById("faks-" + i + "-1")
        if (elA) elA.value = aValue
        
        // Коэффициент b  
        let bValue = randomInRange()
        sessionStorage.setItem("faks-" + i + "-2", bValue)
        let elB = document.getElementById("faks-" + i + "-2")
        if (elB) elB.value = bValue
    }

    // Заполнение начальных условий (0,1) - не включая 0 и 1
    for (let i=1; i<6; i++) {
        const limit = limits[i-1]
        let value
        do {
            value = randomInRange()
        } while (value >= limit) // Начальное условие должно быть меньше предела
        sessionStorage.setItem("init-eq-" + i, value)
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = value
    }

    // Заполнение предельных значений
    for (let i=1; i<6; i++) {
        const limit = limits[i-1]
        sessionStorage.setItem("restrictions-" + i, limit)
        let el = document.getElementById("restrictions-" + i)
        if (el) el.value = limit
    }

    // Заполнение внутренних функций - ВСЕ значения в диапазоне (0,1)
    // f₁: логистическая (2 параметра)
    let eq1_1 = randomInRange()
    let eq1_2 = randomInRange()
    sessionStorage.setItem("equations-1-1", eq1_1)
    sessionStorage.setItem("equations-1-2", eq1_2)
    document.getElementById("equations-1-1").value = eq1_1
    document.getElementById("equations-1-2").value = eq1_2
    
    // f₂: линейная (2 параметра)
    let eq2_1 = randomInRange()
    let eq2_2 = randomInRange()
    sessionStorage.setItem("equations-2-1", eq2_1)
    sessionStorage.setItem("equations-2-2", eq2_2)
    document.getElementById("equations-2-1").value = eq2_1
    document.getElementById("equations-2-2").value = eq2_2
    
    // f₃: ступенчатая (3 параметра)
    let eq3_1 = randomInRange()
    let eq3_2 = randomInRange()
    let eq3_3 = randomInRange()
    // Убедимся, что значения упорядочены: низ < порог < верх
    const sorted = [eq3_1, eq3_2, eq3_3].sort((a, b) => a - b)
    sessionStorage.setItem("equations-3-1", sorted[0])
    sessionStorage.setItem("equations-3-2", sorted[1])
    sessionStorage.setItem("equations-3-3", sorted[2])
    document.getElementById("equations-3-1").value = sorted[0]
    document.getElementById("equations-3-2").value = sorted[1]
    document.getElementById("equations-3-3").value = sorted[2]
    
    // f₄: линейная (2 параметра)
    let eq4_1 = randomInRange()
    let eq4_2 = randomInRange()
    sessionStorage.setItem("equations-4-1", eq4_1)
    sessionStorage.setItem("equations-4-2", eq4_2)
    document.getElementById("equations-4-1").value = eq4_1
    document.getElementById("equations-4-2").value = eq4_2
    
    // f₅: линейная (2 параметра)
    let eq5_1 = randomInRange()
    let eq5_2 = randomInRange()
    sessionStorage.setItem("equations-5-1", eq5_1)
    sessionStorage.setItem("equations-5-2", eq5_2)
    document.getElementById("equations-5-1").value = eq5_1
    document.getElementById("equations-5-2").value = eq5_2
    
    // f₆: дробная (2 параметра)
    let eq6_1 = randomInRange()
    let eq6_2 = randomInRange()
    sessionStorage.setItem("equations-6-1", eq6_1)
    sessionStorage.setItem("equations-6-2", eq6_2)
    document.getElementById("equations-6-1").value = eq6_1
    document.getElementById("equations-6-2").value = eq6_2
    
    // f₇: дробная (2 параметра)
    let eq7_1 = randomInRange()
    let eq7_2 = randomInRange()
    sessionStorage.setItem("equations-7-1", eq7_1)
    sessionStorage.setItem("equations-7-2", eq7_2)
    document.getElementById("equations-7-1").value = eq7_1
    document.getElementById("equations-7-2").value = eq7_2
    
    // f₈: линейная (2 параметра)
    let eq8_1 = randomInRange()
    let eq8_2 = randomInRange()
    sessionStorage.setItem("equations-8-1", eq8_1)
    sessionStorage.setItem("equations-8-2", eq8_2)
    document.getElementById("equations-8-1").value = eq8_1
    document.getElementById("equations-8-2").value = eq8_2
    
    // f₉: логистическая (фиксированная) - нет полей
    
    // f₁₀: линейная (2 параметра)
    let eq10_1 = randomInRange()
    let eq10_2 = randomInRange()
    sessionStorage.setItem("equations-10-1", eq10_1)
    sessionStorage.setItem("equations-10-2", eq10_2)
    document.getElementById("equations-10-1").value = eq10_1
    document.getElementById("equations-10-2").value = eq10_2
    
    // f₁₁: дробная (3 параметра)
    let eq11_1 = randomInRange()
    let eq11_2 = randomInRange()
    let eq11_3 = randomInRange()
    sessionStorage.setItem("equations-11-1", eq11_1)
    sessionStorage.setItem("equations-11-2", eq11_2)
    sessionStorage.setItem("equations-11-3", eq11_3)
    document.getElementById("equations-11-1").value = eq11_1
    document.getElementById("equations-11-2").value = eq11_2
    document.getElementById("equations-11-3").value = eq11_3
    
    // f₁₂: линейная (2 параметра)
    let eq12_1 = randomInRange()
    let eq12_2 = randomInRange()
    sessionStorage.setItem("equations-12-1", eq12_1)
    sessionStorage.setItem("equations-12-2", eq12_2)
    document.getElementById("equations-12-1").value = eq12_1
    document.getElementById("equations-12-2").value = eq12_2
    
    sessionStorage.removeItem("status")
    input.value = "Заполнено случайными значениями (t=" + timeValue + ")"
}

// === ИСПРАВЛЕННАЯ clearAll() ===
function clearAll() {
    // Очистка времени
    document.getElementById("time-value").value = "0.5"
    sessionStorage.setItem("time-value", "0.5")
    
    // Очистка возмущений (14 x 2)
    for (let i=1; i<15; i++) {
        sessionStorage.setItem("faks-" + i + "-1", "0.1")
        sessionStorage.setItem("faks-" + i + "-2", "2.0")
        
        let elA = document.getElementById("faks-" + i + "-1")
        let elB = document.getElementById("faks-" + i + "-2")
        if (elA) elA.value = "0.1"
        if (elB) elB.value = "2.0"
    }

    // Очистка начальных условий
    const defaultInit = ["0.5", "0.7", "0.9", "0.4", "0.5"]
    for (let i=1; i<6; i++) {
        sessionStorage.setItem("init-eq-" + i, defaultInit[i-1])
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = defaultInit[i-1]
    }

    // Очистка предельных значений
    for (let i=1; i<6; i++) {
        sessionStorage.setItem("restrictions-" + i, "1.0")
        let el = document.getElementById("restrictions-" + i)
        if (el) el.value = "1.0"
    }

    // Очистка внутренних функций (установка значений из документа)
    // f₁
    document.getElementById("equations-1-1").value = "0.5"
    document.getElementById("equations-1-2").value = "0.5"
    // f₂
    document.getElementById("equations-2-1").value = "0.3"
    document.getElementById("equations-2-2").value = "15"
    // f₃
    document.getElementById("equations-3-1").value = "0.3"
    document.getElementById("equations-3-2").value = "0.4"
    document.getElementById("equations-3-3").value = "0.5"
    // f₄
    document.getElementById("equations-4-1").value = "0.7"
    document.getElementById("equations-4-2").value = "11"
    // f₅
    document.getElementById("equations-5-1").value = "0.8"
    document.getElementById("equations-5-2").value = "9"
    // f₆
    document.getElementById("equations-6-1").value = "0.8"
    document.getElementById("equations-6-2").value = "12"
    // f₇
    document.getElementById("equations-7-1").value = "0.8"
    document.getElementById("equations-7-2").value = "11"
    // f₈
    document.getElementById("equations-8-1").value = "0.7"
    document.getElementById("equations-8-2").value = "13"
    // f₉: фиксированная, нет полей
    // f₁₀
    document.getElementById("equations-10-1").value = "0.55"
    document.getElementById("equations-10-2").value = "13"
    // f₁₁
    document.getElementById("equations-11-1").value = "0.55"
    document.getElementById("equations-11-2").value = "12"
    document.getElementById("equations-11-3").value = "2"
    // f₁₂
    document.getElementById("equations-12-1").value = "0.5"
    document.getElementById("equations-12-2").value = "3"
    
    // Сохраняем в sessionStorage
    const eqIds = [
        ["1-1", "1-2"], ["2-1", "2-2"], ["3-1", "3-2", "3-3"],
        ["4-1", "4-2"], ["5-1", "5-2"], ["6-1", "6-2"],
        ["7-1", "7-2"], ["8-1", "8-2"], ["10-1", "10-2"],
        ["11-1", "11-2", "11-3"], ["12-1", "12-2"]
    ]
    
    const eqValues = [
        ["0.5", "0.5"], ["0.3", "15"], ["0.3", "0.4", "0.5"],
        ["0.7", "11"], ["0.8", "9"], ["0.8", "12"],
        ["0.8", "11"], ["0.7", "13"], ["0.55", "13"],
        ["0.55", "12", "2"], ["0.5", "3"]
    ]
    
    for (let i=0; i<eqIds.length; i++) {
        for (let j=0; j<eqIds[i].length; j++) {
            sessionStorage.setItem("equations-" + eqIds[i][j], eqValues[i][j])
        }
    }
    
    sessionStorage.removeItem("status")
    input.value = "Очищено (значения из документа)"
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
    
    // Загрузка возмущений
    for (let i=1; i<15; i++) {
        for (let j=1; j<=2; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("faks-" + i + "-" + j) || (j===1 ? "0.1" : "2.0")
            }
        }
    }

    // Загрузка начальных условий
    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) {
            el.value = sessionStorage.getItem("init-eq-" + i) || "0.5"
        }
    }
    
    // Загрузка пределов
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) {
            el.value = sessionStorage.getItem("restrictions-" + i) || "1.0"
        }
    }

    // Загрузка внутренних функций
    const eqIds = [
        ["1-1", "1-2"], ["2-1", "2-2"], ["3-1", "3-2", "3-3"],
        ["4-1", "4-2"], ["5-1", "5-2"], ["6-1", "6-2"],
        ["7-1", "7-2"], ["8-1", "8-2"], ["10-1", "10-2"],
        ["11-1", "11-2", "11-3"], ["12-1", "12-2"]
    ]
    
    for (let eqSet of eqIds) {
        for (let id of eqSet) {
            let el = document.getElementById("equations-" + id)
            if (el) {
                el.value = sessionStorage.getItem("equations-" + id) || "0.5"
            }
        }
    }
}

// === ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ===
function getFaks() {
    const faks = []
    for (let i=1; i<15; i++) {
        const temp = []
        for (let j=1; j<=2; j++) { // ТЕПЕРЬ ТОЛЬКО 2 КОЭФФИЦИЕНТА
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) temp.push(el.value || (j===1 ? "0.1" : "2.0"))
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
    
    // f₁: 2 параметра
    equations.push([
        document.getElementById("equations-1-1")?.value || "0.5",
        document.getElementById("equations-1-2")?.value || "0.5"
    ])
    
    // f₂: 2 параметра
    equations.push([
        document.getElementById("equations-2-1")?.value || "0.3",
        document.getElementById("equations-2-2")?.value || "15"
    ])
    
    // f₃: 3 параметра
    equations.push([
        document.getElementById("equations-3-1")?.value || "0.3",
        document.getElementById("equations-3-2")?.value || "0.4",
        document.getElementById("equations-3-3")?.value || "0.5"
    ])
    
    // f₄: 2 параметра
    equations.push([
        document.getElementById("equations-4-1")?.value || "0.7",
        document.getElementById("equations-4-2")?.value || "11"
    ])
    
    // f₅: 2 параметра
    equations.push([
        document.getElementById("equations-5-1")?.value || "0.8",
        document.getElementById("equations-5-2")?.value || "9"
    ])
    
    // f₆: 2 параметра
    equations.push([
        document.getElementById("equations-6-1")?.value || "0.8",
        document.getElementById("equations-6-2")?.value || "12"
    ])
    
    // f₇: 2 параметра
    equations.push([
        document.getElementById("equations-7-1")?.value || "0.8",
        document.getElementById("equations-7-2")?.value || "11"
    ])
    
    // f₈: 2 параметра
    equations.push([
        document.getElementById("equations-8-1")?.value || "0.7",
        document.getElementById("equations-8-2")?.value || "13"
    ])
    
    // f₉: фиксированная (нет параметров)
    equations.push([])
    
    // f₁₀: 2 параметра
    equations.push([
        document.getElementById("equations-10-1")?.value || "0.55",
        document.getElementById("equations-10-2")?.value || "13"
    ])
    
    // f₁₁: 3 параметра
    equations.push([
        document.getElementById("equations-11-1")?.value || "0.55",
        document.getElementById("equations-11-2")?.value || "12",
        document.getElementById("equations-11-3")?.value || "2"
    ])
    
    // f₁₂: 2 параметра
    equations.push([
        document.getElementById("equations-12-1")?.value || "0.5",
        document.getElementById("equations-12-2")?.value || "3"
    ])
    
    return equations
}

// === ФУНКЦИЯ PROCESS() ===
async function process() {
    const faks = getFaks()
    const init_eq = getInitialEquations()
    const restrictions = getRestrictions()
    const equations = getEquations()
    const timeValue = document.getElementById("time-value").value || "0.5"

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
    
    // Сохраняем возмущения (14 x 2)
    for (let i=1; i<15; i++) {
        for (let j=1; j<=2; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) sessionStorage.setItem("faks-" + i + "-" + j, el.value)
        }
    }

    // Сохраняем начальные условия
    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) sessionStorage.setItem("init-eq-" + i, el.value)
    }
    
    // Сохраняем пределы
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) sessionStorage.setItem("restrictions-" + i, el.value)
    }

    // Сохраняем внутренние функции
    const eqIds = [
        ["1-1", "1-2"], ["2-1", "2-2"], ["3-1", "3-2", "3-3"],
        ["4-1", "4-2"], ["5-1", "5-2"], ["6-1", "6-2"],
        ["7-1", "7-2"], ["8-1", "8-2"], ["10-1", "10-2"],
        ["11-1", "11-2", "11-3"], ["12-1", "12-2"]
    ]
    
    for (let eqSet of eqIds) {
        for (let id of eqSet) {
            let el = document.getElementById("equations-" + id)
            if (el) sessionStorage.setItem("equations-" + id, el.value)
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