from flask import Flask, render_template, request, jsonify
import logging
import os
from process_ecology import process, u_list

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

os.makedirs('static/images', exist_ok=True)

@app.route('/')
def main():
    return render_template('index.html',
                         initial_equations=u_list,
                         # 14 возмущений (6 зависят от времени, 8 от концентрации)
                         faks=[
                             "x₁(t) - Износ оборудования",
                             "x₂(t) - Кредитные ресурсы", 
                             "x₃(t) - Иностранные инвесторы",
                             "x₄(t) - Спрос на продукцию",
                             "x₅(t) - Сложность найма",
                             "x₆(t) - Деловая репутация",
                             "x₇(C) - Уровень смога",
                             "x₈(C) - Задымленность от пожаров",
                             "x₉(C) - Летний антициклон",
                             "x₁₀(C) - Зимний антициклон",
                             "x₁₁(C) - Загруженность дорог",
                             "x₁₂(C) - Крупные предприятия",
                             "x₁₃(C) - Эпидемиологическая ситуация",
                             "x₁₄(C) - Санкции"
                         ],
                         # 12 внутренних функций
                         equations=[
                             "f₁(Cf₃) - Влияние на заболеваемость",
                             "f₂(Cf₄) - Влияние на качество жизни",
                             "f₃(Cf₅) - Влияние потерь предприятия",
                             "f₄(Cf₃) - Влияние на сельское хозяйство",
                             "f₅(Cf₄) - Влияние качества жизни на сельское хозяйство",
                             "f₆(Cf₅) - Влияние предприятия на сельское хозяйство",
                             "f₇(Cf₅) - Влияние предприятия на природу",
                             "f₈(Cf₁) - Влияние заболеваемости на качество жизни",
                             "f₉(Cf₂) - Влияние сельского хозяйства на качество жизни",
                             "f₁₀(Cf₃) - Влияние природы на качество жизни",
                             "f₁₁(Cf₅) - Влияние предприятия на качество жизни",
                             "f₁₂(Cf₁) - Влияние заболеваемости на предприятие"
                         ])

@app.route('/initial_equations')
def get_initial_equations():
    return jsonify(u_list)

@app.route('/draw_graphics', methods=['POST'])
def draw_graphics():
    try:
        data = request.get_json()
        
        # Получаем время из запроса (по умолчанию 0.0)
        time_value = data.get("time_value", "0.0")
        
        process(
            data["initial_equations"], 
            data["faks"], 
            data["equations"], 
            data["restrictions"],
            time_value
        )
        
        return jsonify({"status": "Выполнено", "time_used": time_value})
    except Exception as e:
        logging.error(f"Error in draw_graphics: {e}")
        return jsonify({"status": "Ошибка"})

@app.route('/graphic')
def get_graphic():
    return render_template('graphic.html')

@app.route('/diagrams')
def get_diagrams():
    return render_template('diagrams.html')

@app.route('/facks')
def get_disturbances():
    return render_template('facks.html')

@app.route('/clear_images', methods=['POST'])
def clear_images():
    """Очистка старых изображений"""
    try:
        images_to_clear = [
            'static/images/figure_eco.png',
            'static/images/disturbances_eco.png',
            'static/images/diagram_eco.png',
            'static/images/diagram_eco2.png',
            'static/images/diagram_eco3.png',
            'static/images/diagram_eco4.png',
            'static/images/diagram_eco5.png'
        ]
        
        for img_path in images_to_clear:
            if os.path.exists(img_path):
                os.remove(img_path)
                logging.info(f"Removed: {img_path}")
        
        return jsonify({"status": "Images cleared"})
    except Exception as e:
        logging.error(f"Error clearing images: {e}")
        return jsonify({"status": "Error clearing images"})

if __name__ == '__main__':
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    
    # Запуск приложения
    app.run(host='0.0.0.0', port=5000, debug=True)