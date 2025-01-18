from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример данных (наш "мини-склад задач")
tasks = [
    {"id": 1, "title": "Сделать урок по REST API", "completed": False},
    {"id": 2, "title": "Сходить за кофе", "completed": True},
]

@app.get("/")
def index():
    return "Добро пожаловать в ToDo API!"

@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)

@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Задача не найдена"}), 404

@app.post("/api/tasks")
def create_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title", "Без названия"),
        "completed": False,
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404
    
    task["title"] = data.get("title", task["title"])
    task["completed"] = data.get("completed", task["completed"])
    return jsonify(task)

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Задача удалена"})

if __name__ == "__main__":
    app.run(debug=True)