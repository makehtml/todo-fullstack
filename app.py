from uuid import uuid4

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super_secret_key"  # Замените на свой секретный ключ!
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
JWTManager(app)


# Пример данных (наш "мини-склад задач")
tasks = [
    {"id": str(uuid4()), "title": "Сделать урок по REST API", "completed": False},
    {"id": str(uuid4()), "title": "Сходить за кофе", "completed": True},
]
users = {"frodo": "myprecious", "sam": "po-ta-toes"}

def make_response(status, message, data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    })

@app.errorhandler(500)
def handle_500_error(e):
    return make_response("error", "Что-то пошло не так на сервере"), 500

@app.errorhandler(404)
def handle_404_error(e):
    return make_response("error", "Ресурс не найден"), 404

@app.get("/")
def index():
    return "Добро пожаловать в ToDo API!"

@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)

@app.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return make_response("error", "Задача не найдена"), 404

    return make_response("success", "Задача найдена", task)

@app.route("/api/tasks/<task_id>", methods=["OPTIONS"])
def options_task(task_id):
    response = jsonify({"message": "Preflight request successful"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

@app.post("/api/tasks")
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Поле 'title' обязательно"}), 400

    new_task = {
        "id": str(uuid4()),
        "title": data["title"],
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

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Задача удалена"})

@app.get("/api/data")
def get_data():
    return jsonify({"message": "Привет из Flask!", "items": [1, 2, 3, 4, 5]})

@app.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        roles = "admin" if username == "frodo" else "user"
        token = create_access_token(identity={"username": username, "roles": roles})
        return jsonify({"access_token": token}), 200

    return jsonify({"error": "Неверные логин или пароль"}), 401

@app.get("/protected")
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Добро пожаловать, {current_user}!"}), 200

@app.get("/admin")
@jwt_required()
def admin_route():
    user = get_jwt_identity()
    if user.get("roles") != "admin":
        return jsonify({"error": "Доступ запрещён"}), 403

    return jsonify({"message": "Добро пожаловать, администратор!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
