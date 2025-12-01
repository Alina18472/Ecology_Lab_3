const input = document.getElementById("status-input")
input.value = sessionStorage.getItem("status") || ""

function random() {
    return Math.round(((Math.random() * 0.7 + 0.01) + Number.EPSILON) * 100) / 100
}

function randomCoefficient() {
    return Math.round(((Math.random() * 2 - 1) + Number.EPSILON) * 100) / 100
}

function randomFakCoefficient(isTimeDependent) {
    if (isTimeDependent) {
        // Для зависящих от времени: случайное положительное значение для d
        return Math.round(((Math.random() * 5 + 1) + Number.EPSILON) * 100) / 100
    } else {
        // Для зависящих от концентрации: случайные коэффициенты
        return Math.round(((Math.random() * 3 - 1) + Number.EPSILON) * 100) / 100
    }
}

if (input.value !== "Выполнено") {
    refill()
} else {
    // Загрузка сохраненных значений
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("faks-" + i + "-" + j) || ""
            }
        }
    }

    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) {
            el.value = sessionStorage.getItem("init-eq-" + i) || ""
        }
    }

    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) {
                el.value = sessionStorage.getItem("equations-" + i + "-" + j) || ""
            }
        }
    }
}

function getFaks() {
    const faks = []
    for (let i=1; i<15; i++) {
        const temp = []
        for (let j=1; j<5; j++) {
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) temp.push(el.value || "0")
        }
        faks.push(temp)
    }
    return faks
}

function getInitialEquations() {
    const init_eq = []
    for (let i=1; i<6; i++) {
        let el = document.getElementById("init-eq-" + i)
        if (el) init_eq.push(el.value || "0")
    }
    return init_eq
}

function getRestrictions() {
    const restrictions = []
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) restrictions.push(el.value || "1")
    }
    return restrictions
}

function getEquations() {
    const equations = []
    for (let i=1; i<13; i++) {
        const temp = []
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) temp.push(el.value || "0")
        }
        equations.push(temp)
    }
    return equations
}

async function process() {
    const faks = getFaks()
    const init_eq = getInitialEquations()
    const restrictions = getRestrictions()
    const equations = getEquations()

    // Сохранение в sessionStorage
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

    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) sessionStorage.setItem("equations-" + i + "-" + j, el.value)
        }
    }

    const response = await fetch('/draw_graphics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "faks": faks,
            "initial_equations": init_eq,
            "restrictions": restrictions,
            "equations": equations
        })
    })

    const result = await response.json()
    input.value = result.status
    sessionStorage.setItem("status", result.status)
    
    // Автоматическое обновление через 1 секунду
    setTimeout(() => {
        window.location.reload()
    }, 1000)
}

function refill() {
    // Заполнение возмущений (14 x 4)
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            let value
            if (i <= 6) {
                // Возмущения, зависящие от времени (x1-x6)
                if (j === 4) {
                    value = randomFakCoefficient(true) // коэффициент d
                } else {
                    value = randomCoefficient()
                }
            } else {
                // Возмущения, зависящие от концентрации (x7-x14)
                value = randomFakCoefficient(false)
            }
            
            sessionStorage.setItem("faks-" + i + "-" + j, value)
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) el.value = value
        }
    }

    // Заполнение начальных условий (5 значений)
    for (let i=1; i<6; i++) {
        let value = random()
        sessionStorage.setItem("init-eq-" + i, value)
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = value
    }

    // Заполнение внутренних функций (12 x 5)
    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let value
            if (j === 4) {
                value = randomCoefficient() // линейный коэффициент
            } else if (j === 5) {
                value = randomCoefficient() // свободный член
            } else {
                value = randomCoefficient() // старшие коэффициенты
            }
            
            sessionStorage.setItem("equations-" + i + "-" + j, value)
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) el.value = value
        }
    }
    
    sessionStorage.removeItem("status")
    input.value = "Заполнено случайными значениями"
}

function clearAll() {
    // Очистка возмущений
    for (let i=1; i<15; i++) {
        for (let j=1; j<5; j++) {
            sessionStorage.setItem("faks-" + i + "-" + j, "0")
            let el = document.getElementById("faks-" + i + "-" + j)
            if (el) el.value = "0"
        }
    }

    // Очистка начальных условий
    for (let i=1; i<6; i++) {
        sessionStorage.setItem("init-eq-" + i, "0.5")
        let el = document.getElementById("init-eq-" + i)
        if (el) el.value = "0.5"
    }

    // Очистка внутренних функций
    for (let i=1; i<13; i++) {
        for (let j=1; j<6; j++) {
            let defaultValue = "0"
            if (j === 4) defaultValue = "1"
            sessionStorage.setItem("equations-" + i + "-" + j, defaultValue)
            let el = document.getElementById("equations-" + i + "-" + j)
            if (el) el.value = defaultValue
        }
    }

    // Очистка предельных значений
    for (let i=1; i<6; i++) {
        let el = document.getElementById("restrictions-" + i)
        if (el) el.value = "1.0"
    }
    
    sessionStorage.removeItem("status")
    input.value = "Очищено"
}