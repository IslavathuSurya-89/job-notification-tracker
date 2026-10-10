from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    organization = db.Column(db.String(160), nullable=False)
    department = db.Column(db.String(120), nullable=False, default="Not specified")
    qualification = db.Column(db.String(120), nullable=False, default="Any")
    age_limit = db.Column(db.String(100), nullable=False, default="Check notification")
    vacancies = db.Column(db.Integer, nullable=True)
    salary = db.Column(db.String(100), nullable=False, default="As per notification")
    category = db.Column(db.String(40), nullable=False, default="Government")
    location = db.Column(db.String(120), nullable=False, default="India")
    notification_date = db.Column(db.Date, nullable=True)
    last_date = db.Column(db.Date, nullable=True)
    apply_url = db.Column(db.String(500), nullable=False, default="")
    status = db.Column(db.String(30), nullable=False, default="Open")
    notes = db.Column(db.Text, nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_expired(self):
        return self.last_date is not None and self.last_date < date.today()


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()
    qualification = request.args.get("qualification", "").strip()

    query = Job.query
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(
            Job.title.ilike(pattern),
            Job.organization.ilike(pattern),
            Job.department.ilike(pattern),
            Job.location.ilike(pattern),
        ))
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if qualification:
        query = query.filter(Job.qualification.ilike(f"%{qualification}%"))

    jobs = query.order_by(Job.last_date.is_(None), Job.last_date.asc(), Job.created_at.desc()).all()
    today = date.today()
    stats = {
        "total": Job.query.count(),
        "open": Job.query.filter_by(status="Open").count(),
        "closing_soon": Job.query.filter(
            Job.status == "Open",
            Job.last_date >= today,
            Job.last_date <= date.fromordinal(today.toordinal() + 7),
        ).count(),
        "expired": Job.query.filter(Job.last_date.isnot(None), Job.last_date < today).count(),
    }
    return render_template("index.html", jobs=jobs, stats=stats, today=today,
                           filters={"q": search, "category": category, "status": status,
                                    "qualification": qualification})


@app.route("/jobs/new", methods=["GET", "POST"])
def new_job():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        organization = request.form.get("organization", "").strip()
        if not title or not organization:
            flash("Job title and organization are required.", "error")
            return render_template("job_form.html", job=None)

        job = Job(
            title=title,
            organization=organization,
            department=request.form.get("department", "").strip() or "Not specified",
            qualification=request.form.get("qualification", "").strip() or "Any",
            age_limit=request.form.get("age_limit", "").strip() or "Check notification",
            vacancies=int(request.form["vacancies"]) if request.form.get("vacancies", "").isdigit() else None,
            salary=request.form.get("salary", "").strip() or "As per notification",
            category=request.form.get("category", "Government"),
            location=request.form.get("location", "").strip() or "India",
            notification_date=parse_date(request.form.get("notification_date")),
            last_date=parse_date(request.form.get("last_date")),
            apply_url=request.form.get("apply_url", "").strip(),
            status=request.form.get("status", "Open"),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(job)
        db.session.commit()
        flash("Job notification added successfully.", "success")
        return redirect(url_for("index"))
    return render_template("job_form.html", job=None)


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        organization = request.form.get("organization", "").strip()
        if not title or not organization:
            flash("Job title and organization are required.", "error")
            return render_template("job_form.html", job=job)
        job.title = title
        job.organization = organization
        job.department = request.form.get("department", "").strip() or "Not specified"
        job.qualification = request.form.get("qualification", "").strip() or "Any"
        job.age_limit = request.form.get("age_limit", "").strip() or "Check notification"
        job.vacancies = int(request.form["vacancies"]) if request.form.get("vacancies", "").isdigit() else None
        job.salary = request.form.get("salary", "").strip() or "As per notification"
        job.category = request.form.get("category", "Government")
        job.location = request.form.get("location", "").strip() or "India"
        job.notification_date = parse_date(request.form.get("notification_date"))
        job.last_date = parse_date(request.form.get("last_date"))
        job.apply_url = request.form.get("apply_url", "").strip()
        job.status = request.form.get("status", "Open")
        job.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash("Job notification updated.", "success")
        return redirect(url_for("index"))
    return render_template("job_form.html", job=job)


@app.post("/jobs/<int:job_id>/delete")
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job notification deleted.", "success")
    return redirect(url_for("index"))


@app.cli.command("seed")
def seed():
    """Load fictional demo records into an empty database."""
    if Job.query.first():
        print("Database already contains jobs; seed skipped.")
        return
    samples = [
        Job(title="Junior Assistant (Demo)", organization="Example State Department",
            department="Administration", qualification="12th Pass", age_limit="18–30 years (demo only)",
            vacancies=120, salary="As per official notice", category="Government",
            location="Andhra Pradesh", notification_date=date.today(),
            last_date=date.fromordinal(date.today().toordinal() + 20),
            apply_url="https://example.com/", status="Open",
            notes="Fictional sample record. Verify all details from the official notification."),
        Job(title="Python Intern (Demo)", organization="Example Tech Company",
            department="Software Engineering", qualification="B.Tech / Python basics",
            age_limit="Not specified", vacancies=5, salary="Stipend varies",
            category="Private", location="Remote", notification_date=date.today(),
            last_date=date.fromordinal(date.today().toordinal() + 10),
            apply_url="https://example.com/", status="Open",
            notes="Fictional sample record for testing the tracker."),
        Job(title="Data Entry Operator (Demo)", organization="Example Public Office",
            department="Data Operations", qualification="12th Pass",
            age_limit="Check official notice", vacancies=25, salary="As per notice",
            category="Government", location="India", notification_date=date.today(),
            last_date=date.fromordinal(date.today().toordinal() - 2),
            apply_url="https://example.com/", status="Closed",
            notes="Fictional expired sample record.")
    ]
    db.session.add_all(samples)
    db.session.commit()
    print("Added 3 fictional sample jobs.")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
