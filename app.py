from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def classify_bmi(bmi):
    if bmi < 18:
        return "Underweight", "underweight"
    elif 18 <= bmi < 25:
        return "Normal", "normal"
    elif 25 <= bmi < 30:
        return "Overweight", "overweight"
    else:
        return "Obese", "obese"

@app.context_processor
def inject_now():
    return {"now": datetime.now()}

@app.route("/")
def index():
    users = []
    try:
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    username, age, weight, height, gender, target = parts
                    weight = float(weight)
                    height = float(height)
                    bmi = round(weight / (height * height), 2)
                    category, css_class = classify_bmi(bmi)
                    users.append({
                        "username": username,
                        "age": age,
                        "weight": weight,
                        "height": height,
                        "bmi": bmi,
                        "category": category,
                        "css_class": css_class
                    })
    except FileNotFoundError:
        pass
    return render_template("index.html", users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        age = request.form["age"]
        weight = request.form["weight"]
        height = request.form["height"]
        gender = request.form["gender"]
        target = request.form["target"]

        with open("users.txt", "a") as f:
            f.write(f"{username},{age},{weight},{height},{gender},{target}\n")

        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    if request.method == "POST":
        username = request.form["username"]
        muscle = request.form["muscle"]
        exercise = request.form["exercise"]
        reps = request.form["reps"]
        sets = request.form["sets"]
        notes = request.form["notes"]
        date = datetime.now().strftime("%Y-%m-%d")

        with open("workouts.txt", "a") as f:
            f.write(f"{username},{muscle},{exercise},{reps},{sets},{notes},{date}\n")

        return redirect(url_for("progress"))
    return render_template("workouts.html")

@app.route("/progress")
def progress():
    workouts = []
    try:
        with open("workouts.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 7:
                    username, muscle, exercise, reps, sets, notes, date = parts
                    workouts.append({
                        "username": username,
                        "muscle": muscle,
                        "date": date
                    })
    except FileNotFoundError:
        pass
    return render_template("progress.html", workouts=workouts)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        username = request.form["username"]
        try:
            with open("users.txt", "r") as f:
                lines = f.readlines()
            with open("users.txt", "w") as f:
                for line in lines:
                    if not line.startswith(username + ","):
                        f.write(line)
        except FileNotFoundError:
            pass
        return redirect(url_for("index"))
    return render_template("delete.html")

if __name__ == "__main__":
    app.run(debug=True)
