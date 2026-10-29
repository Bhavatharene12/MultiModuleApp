from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "multimodule-24MIS0505-v3"

APP_TITLE = "MultiModule Student Management System"
VERSION_LABEL = "Version 3 – Connected Dashboard"

# ONE shared data store used by Module 1 (add/list), Module 2 (search) and the dashboard
students = [
    {"id": "24MIS0505", "name": "Bhavatharene", "department": "MIS", "email": "24mis0505@vitstudent.ac.in"},
    {"id": "24MIS0506", "name": "Arun Kumar", "department": "MIS", "email": "24mis0506@vitstudent.ac.in"},
    {"id": "24MIS0508", "name": "Priya Sharma", "department": "MIS", "email": "24mis0508@vitstudent.ac.in"},
]


@app.context_processor
def inject_globals():
    return {"app_title": APP_TITLE, "version_label": VERSION_LABEL, "total": len(students)}


# ---------------- Module 3 : Connected dashboard ----------------
@app.route("/")
def dashboard():
    modules = [
        {"name": "Module 1 – Add Student / Student List", "link": "students_list"},
        {"name": "Module 2 – Search by ID / Name", "link": "search"},
        {"name": "Module 3 – Connected Dashboard", "link": "dashboard"},
    ]
    return render_template(
        "dashboard.html",
        latest_id=students[-1]["id"] if students else "—",
        modules=modules,
        recent=list(reversed(students[-5:])),
    )


# ---------------- Module 1 ----------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
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
            flash(f"Student {name} ({sid}) added - now visible in Module 2 and the dashboard.", "success")
            return redirect(url_for("dashboard"))
    return render_template("add.html")


@app.route("/students")
def students_list():
    return render_template("students.html", students=students)


# ---------------- Module 2 ----------------
@app.route("/search")
def search():
    by = request.args.get("by", "id")
    q = request.args.get("q", "").strip()
    results = []
    if q:
        key = "id" if by == "id" else "name"
        results = [s for s in students if q.lower() in s[key].lower()]
    return render_template("search.html", by=by, q=q, results=results, searched=bool(q))


@app.route("/health")
def health():
    return {"status": "ok", "version": "v3"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
