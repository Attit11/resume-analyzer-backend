from app.extensions import db


class ResumeAnalysis(db.Model):

    __tablename__ = "resume_analysis"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    resume_text = db.Column(db.Text)

    analysis = db.Column(db.Text)
