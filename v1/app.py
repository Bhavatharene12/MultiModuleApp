from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "multimodule-24MIS0505-v1"

APP_TITLE = "MultiModule Student Management System"
VERSION_LABEL = "Version 1 – Module 1"

# Module 1 data: students are kept in memory
students = []


@app.context_processor
def inject_globals():
    return {"app_title": APP_TITLE, "version_label": VERSION_LABEL}


@app.route("/")
@app.route("/add", methods=["GET", "POST"])
def add_student():
    """Module 1 - Add Student."""
    if request.method == "POST":
        sid = request.form.get("student_id", "").strip().upper()
        name = request.form.get("name", "").strip()
        dept = request.form.get("department", "").strip()
        email = request.form.get("email", "").strip()
        if not (sid and name and dept and email):
            flash("All fields are required.", "error")
        elif any(s["id"] == sid for s in students):
            flash(f"Student ID {sid} already exists.", "error")
        else:
            students.append({"id": sid, "name": name, "department": dept, "email": email})
            flash(f"Student {name} ({sid}) added successfully.", "success")
            return redirect(url_for("students_list"))
    return render_template("add.html")


@app.route("/students")
def students_list():
    """Module 1 - Student List."""
    return render_template("students.html", students=students)


@app.route("/health")
def health():
    return {"status": "ok", "version": "v1"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
