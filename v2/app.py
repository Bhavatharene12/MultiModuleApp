from flask import Flask, render_template, request

app = Flask(__name__)

APP_TITLE = "MultiModule Student Management System"
VERSION_LABEL = "Version 2 – Module 2"

# Module 2 works on its own data set (sample records) - there is no Module 1 here.
students = [
    {"id": "24MIS0505", "name": "Bhavatharene", "department": "MIS", "email": "24mis0505@vitstudent.ac.in"},
    {"id": "24MIS0506", "name": "Arun Kumar", "department": "MIS", "email": "24mis0506@vitstudent.ac.in"},
    {"id": "24MIS0508", "name": "Priya Sharma", "department": "MIS", "email": "24mis0508@vitstudent.ac.in"},
    {"id": "24MIS0514", "name": "Karthik Raja", "department": "MIS", "email": "24mis0514@vitstudent.ac.in"},
    {"id": "24MIS0519", "name": "Divya Lakshmi", "department": "MIS", "email": "24mis0519@vitstudent.ac.in"},
]


@app.context_processor
def inject_globals():
    return {"app_title": APP_TITLE, "version_label": VERSION_LABEL}


@app.route("/")
@app.route("/search")
def search():
    """Module 2 - Search Student by ID / Name."""
    by = request.args.get("by", "id")
    q = request.args.get("q", "").strip()
    results = []
    if q:
        key = "id" if by == "id" else "name"
        results = [s for s in students if q.lower() in s[key].lower()]
    return render_template("search.html", by=by, q=q, results=results,
                           searched=bool(q), total=len(students))


@app.route("/health")
def health():
    return {"status": "ok", "version": "v2"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
