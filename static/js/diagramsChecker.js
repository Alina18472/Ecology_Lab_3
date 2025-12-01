const status = sessionStorage.getItem("status")
const grid = document.querySelector('#diagrams-grid')

if (status !== "Выполнено") {
    grid.innerHTML = `
        <div class="no-data-message">
            <h3>Диаграммы не доступны</h3>
            <p>Выполните расчеты на странице "Параметры модели" чтобы увидеть диаграммы</p>
            <a href="/" class="btn-back">Вернуться к параметрам</a>
        </div>
    `
} else {
    // Проверяем загрузку каждой диаграммы
    const diagrams = ['diagram1', 'diagram2', 'diagram3', 'diagram4', 'diagram5']
    
    diagrams.forEach((id, index) => {
        const img = document.getElementById(id)
        if (img) {
            img.onerror = function() {
                const container = this.parentElement
                container.innerHTML = `
                    <div style="color: #dc3545; padding: 20px;">
                        <p>Диаграмма не сгенерирована</p>
                    </div>
                `
            }
            
            // Добавляем временную метку для предотвращения кэширования
            img.src = img.src.split('?')[0] + '?t=' + new Date().getTime()
        }
    })
}