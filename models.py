from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))

    # 🔥 New fields
    duration = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    skills = db.Column(db.Text)   # store as comma-separated string
    future_opportunities = db.Column(db.Text)
    max_applicants = db.Column(db.Integer)

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)