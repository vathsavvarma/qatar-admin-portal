from flask import Flask
from models import db, Admin
from flask_login import LoginManager
from routes import signup, login, dashboard, add_opportunity, get_opportunities, update_opportunity, delete_opportunity, forgot_password, reset_password, get_opportunity
from flask import render_template
from flask_cors import CORS


app = Flask(__name__)

CORS(app, supports_credentials=True)
@app.route('/')
def home():
    return render_template('admin.html')

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET'])
app.add_url_rule('/opportunities', 'add_opportunity', add_opportunity, methods=['POST'])
app.add_url_rule('/opportunities', 'get_opportunities', get_opportunities, methods=['GET'])
app.add_url_rule('/opportunities/<int:op_id>', 'update_opportunity', update_opportunity, methods=['PUT'])
app.add_url_rule('/opportunities/<int:op_id>', 'delete_opportunity', delete_opportunity, methods=['DELETE'])
app.add_url_rule('/forgot-password', 'forgot_password', forgot_password, methods=['POST'])
app.add_url_rule('/reset-password/<token>', 'reset_password', reset_password, methods=['POST'])
app.add_url_rule('/opportunities/<int:op_id>', 'get_opportunity', get_opportunity, methods=['GET'])


# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)