from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример данных (наш "мини-склад задач")
tasks = [
    {"id": 1, "title": "Сделать урок по REST API", "completed": False},
    {"id": 2, "title": "Сходить за кофе", "completed": True},
]

@app.route("/")
def index():
    return "Добро пожаловать в ToDo API!"

if __name__ == "__main__":
    app.run(debug=True)