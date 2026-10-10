import os
import tempfile
import unittest
from app import app, db, Job


class JobTrackerTests(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{self.db_path}",
            WTF_CSRF_ENABLED=False,
        )
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_dashboard_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Job notification tracker", response.data)

    def test_add_job(self):
        response = self.client.post("/jobs/new", data={
            "title": "Python Developer",
            "organization": "Example Ltd",
            "qualification": "B.Tech",
            "category": "Private",
            "status": "Open",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Job.query.count(), 1)
            self.assertEqual(Job.query.first().title, "Python Developer")

    def test_required_fields(self):
        response = self.client.post("/jobs/new", data={"title": "", "organization": ""})
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Job.query.count(), 0)

    def test_search_filter(self):
        with app.app_context():
            db.session.add(Job(title="Data Analyst", organization="Acme", category="Private"))
            db.session.add(Job(title="Forest Guard", organization="Department", category="Government"))
            db.session.commit()
        response = self.client.get("/?q=Forest")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Forest Guard", response.data)
        self.assertNotIn(b"Data Analyst", response.data)

    def test_delete_job(self):
        with app.app_context():
            job = Job(title="Test Role", organization="Test Org")
            db.session.add(job)
            db.session.commit()
            job_id = job.id
        response = self.client.post(f"/jobs/{job_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(Job.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
