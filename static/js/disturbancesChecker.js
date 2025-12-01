const status = sessionStorage.getItem("status")
const element = document.getElementById("disturbances-image")
const container = document.getElementById("disturbances-container")

if (status !== "Выполнено") {
    container.innerHTML = `
        <div class="no-data-message">
            <h3>График возмущений не доступен</h3>
            <p>Выполните расчеты на странице "Параметры модели" чтобы увидеть график</p>
            <a href="/" class="btn-back">Вернуться к параметрам</a>
        </div>
    `
} else {
    // Проверяем, загрузилось ли изображение
    element.onload = function() {
        element.style.display = "block"
    }
    
    element.onerror = function() {
        container.innerHTML = `
            <div class="no-data-message">
                <h3>Ошибка загрузки графика</h3>
                <p>График возмущений не был сгенерирован или произошла ошибка при загрузке</p>
                <a href="/" class="btn-back">Вернуться к параметрам</a>
            </div>
        `
    }
    
    // Добавляем временную метку для предотвращения кэширования
    element.src = element.src.split('?')[0] + '?t=' + new Date().getTime()
}