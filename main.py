from flask import Flask, render_template, request
import numpy as np
from maut import maut_method  # Добавляем импорт функции MAUT

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        criteria_weights = request.form.getlist('criteria_weights[]', type=float)
        alternative_names = request.form.getlist('alternative_names[]')
        criteria_names = request.form.getlist('criteria_names[]')
        alternative_scores = np.array([request.form.getlist('scores_row_' + str(i) + '[]', type=int) for i in range(len(alternative_names))])

        # Определение типа критериев (предполагаем максимизацию)
        criterion_types = ['max'] * len(criteria_weights)  # В вашем случае все критерии на максимум
        utility_functions = ['u_exp'] * len(criteria_weights)  # Пример: экспоненциальные функции полезности для всех критериев

        # Использование MAUT для расчета полезности
        results_array = maut_method(alternative_scores, criteria_weights, criterion_types, utility_functions)
        results = dict(zip(alternative_names, results_array[:, 1]))  # Преобразуем результаты в словарь для отображения

    else:
        # Данные по умолчанию (без изменений)
        criteria_weights = [0.2, 0.15, 0.2, 0.15, 0.15, 0.15]
        alternative_names = ["Солнечная энергия", "Ветровая энергия", "Гидроэнергия", "Биомасса", "Ядерная энергия"]
        criteria_names = ["Экономическая эффективность", "Экологическая устойчивость", "Надежность и доступность", "Гибкость и адаптивность", "Техническая интеграция", "Социальная ответственность и общественное мнение"]
        alternative_scores = [
            [7, 8, 6, 7, 6, 7],
            [6, 7, 8, 6, 7, 6],
            [8, 6, 7, 6, 7, 7],
            [5, 7, 6, 7, 6, 6],
            [9, 6, 8, 5, 7, 8]
        ]
        results = {}

    return render_template('index.html', criteria_weights=criteria_weights, alternative_names=alternative_names, criteria_names=criteria_names, alternative_scores=alternative_scores, results=results)

if __name__ == '__main__':
    app.run(debug=True)
