from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "secret123"

API = "http://127.0.0.1:8000"


# 🏠 Home
@app.route("/")
def home():
    return render_template("index.html")


# 🔐 Register
@app.route("/register", methods=["POST"])
def register():
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": request.form["password"]
    }

    res = requests.post(f"{API}/register", json=data)

    if res.status_code == 200:
        # ✅ Better UX → go to dashboard directly
        login_data = {
            "username": data["username"],
            "password": data["password"]
        }
        login_res = requests.post(f"{API}/login", data=login_data)

        if login_res.status_code == 200:
            session["token"] = login_res.json()["access_token"]
            return redirect("/dashboard")

        return redirect("/")
    else:
        return "Registration Failed"


# 🔑 Login
@app.route("/login", methods=["POST"])
def login():
    data = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    res = requests.post(f"{API}/login", data=data)

    if res.status_code == 200:
        token = res.json()["access_token"]
        session["token"] = token
        return redirect("/dashboard")
    else:
        return "Login Failed"


# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    token = session.get("token")

    # ✅ Safety check
    if not token:
        return redirect("/")

    headers = {"Authorization": f"Bearer {token}"}

    res = requests.get(f"{API}/tasks", headers=headers)

    tasks = res.json() if res.status_code == 200 else []

    return render_template("dashboard.html", tasks=tasks)


# ➕ Add Task (FIXED - only one function)
@app.route("/add-task", methods=["POST"])
def add_task():
    token = session.get("token")

    if not token:
        return redirect("/")

    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "deadline": request.form.get("deadline") or None
    }

    requests.post(f"{API}/tasks", json=data, headers=headers)

    return redirect("/dashboard")


# ✏️ Update task
@app.route("/update-task/<int:task_id>", methods=["POST"])
def update_task(task_id):
    token = session.get("token")

    if not token:
        return redirect("/")

    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "deadline": request.form.get("deadline"),
        "is_done": True if request.form.get("is_done") == "on" else False
    }

    requests.put(f"{API}/tasks/{task_id}", json=data, headers=headers)

    return redirect("/dashboard")


# ❌ Delete task
@app.route("/delete-task/<int:task_id>")
def delete_task(task_id):
    token = session.get("token")

    if not token:
        return redirect("/")

    headers = {"Authorization": f"Bearer {token}"}

    requests.delete(f"{API}/tasks/{task_id}", headers=headers)

    return redirect("/dashboard")


# 🚪 Logout (NEW - better UX)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)