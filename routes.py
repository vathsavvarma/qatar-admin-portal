from flask import request, jsonify
from flask_login import login_required, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Opportunity
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

@login_required
def dashboard():
    return jsonify({
        "message": f"Welcome {current_user.full_name}"
    })

def signup():
    data = request.get_json()

    name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    existing_user = Admin.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = Admin(
        full_name=name,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"})




def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    user = Admin.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    login_user(user)

    return jsonify({
    "message": "Login successful",
    "full_name": user.full_name   # ✅ send name to frontend
    })


from models import Opportunity, db
from flask_login import login_required, current_user

@login_required
def add_opportunity():
    data = request.get_json() or request.form

    new_op = Opportunity(
        title=data.get("title"),
        description=data.get("description"),
        category=data.get("category"),

        # 🔥 new fields
        duration=data.get("duration"),
        start_date=data.get("start_date"),
        skills=",".join(data.get("skills", [])) if isinstance(data.get("skills"), list) else data.get("skills"),
        future_opportunities=data.get("future_opportunities"),
        max_applicants=int(data.get("max_applicants")) if data.get("max_applicants") else None,

        admin_id=current_user.id
    )

    db.session.add(new_op)
    db.session.commit()

    return jsonify({
        "message": "Opportunity created",
        "id": new_op.id
    })


@login_required
def get_opportunities():
    ops = Opportunity.query.filter_by(admin_id=current_user.id).all()

    result = []

    for op in ops:
        result.append({
            "id": op.id,
            "title": op.title,
            "description": op.description,
            "category": op.category,
            "duration": op.duration,
            "start_date": op.start_date,
            "skills": op.skills,
            "future_opportunities": op.future_opportunities,
            "max_applicants": op.max_applicants
        })

    return jsonify(result)

@login_required
def update_opportunity(op_id):
    data = request.get_json() or request.form

    op = Opportunity.query.get(op_id)

    if not op:
        return jsonify({"error": "Not found"}), 404

    if op.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    op.title = data.get("title", op.title)
    op.description = data.get("description", op.description)
    op.category = data.get("category", op.category)
    op.duration = data.get("duration", op.duration)
    op.start_date = data.get("start_date", op.start_date)
    op.skills = ",".join(data.get("skills", [])) if isinstance(data.get("skills"), list) else data.get("skills")
    op.future_opportunities = data.get("future_opportunities", op.future_opportunities)
    op.max_applicants = int(data.get("max_applicants")) if data.get("max_applicants") else op.max_applicants

    db.session.commit()

    return jsonify({"message": "Updated"})


@login_required
def delete_opportunity(op_id):
    op = Opportunity.query.get(op_id)

    if not op:
        return jsonify({"error": "Opportunity not found"}), 404

    if op.admin_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(op)
    db.session.commit()

    return jsonify({"message": "Opportunity deleted successfully"})

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def forgot_password():
    data = request.get_json()
    email = data.get("email")

    # Always return same message (security reason)
    user = Admin.query.filter_by(email=email).first()

    if user:
        token = generate_reset_token(email)

        reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

        print(f"Reset Link: {reset_link}")  # simulate email

    return jsonify({"message": "If email exists, reset link sent"})

from itsdangerous import BadSignature, SignatureExpired

def reset_password(token):
    data = request.get_json()
    new_password = data.get("password")

    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return jsonify({"error": "Token expired"}), 400
    except BadSignature:
        return jsonify({"error": "Invalid token"}), 400

    user = Admin.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Password reset successful"})

@login_required
def get_opportunity(op_id):
    op = Opportunity.query.get(op_id)

    if not op or op.admin_id != current_user.id:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": op.id,
        "title": op.title,
        "description": op.description,
        "category": op.category,
        "duration": op.duration,
        "start_date": op.start_date,
        "skills": op.skills,
        "future_opportunities": op.future_opportunities,
        "max_applicants": op.max_applicants
    })