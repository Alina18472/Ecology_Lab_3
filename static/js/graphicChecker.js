const status = sessionStorage.getItem("status")
const element = document.getElementById("graphic-image")
const container = document.getElementById("graphic-container")

if (status !== "Выполнено") {
    container.innerHTML = `
        <div class="no-data-message">
            <h3>График потерь не доступен</h3>
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
                <p>График не был сгенерирован или произошла ошибка при загрузке</p>
                <a href="/" class="btn-back">Вернуться к параметрам</a>
            </div>
        `
    }
    
    // Добавляем временную метку для предотвращения кэширования
    element.src = element.src.split('?')[0] + '?t=' + new Date().getTime()
}