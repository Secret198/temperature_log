from flask import Flask, render_template, request, redirect, url_for
from models import db, Temperature
from datetime import datetime
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

class TemperatureScheme(Schema):
    temperature = fields.Float(
        required=True, 
    )


temp_schema = TemperatureScheme()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    temperatures = db.session.execute(db.select(Temperature).order_by(Temperature.timestamp.asc())).scalars()
    return render_template('index.html', temperatures=temperatures)

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()

    temperature = data["temperature"]
    timestamp = datetime.now().replace(microsecond=0)
    # timestamp = datetime.strptime(data["timestamp"], '%Y-%m-%d %H:%M:%S')


    new_temp = Temperature(temperature=temperature, timestamp=timestamp)
    db.session.add(new_temp)
    db.session.commit()


    return redirect(url_for('home'))


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Catches all HTTP errors (400, 401, 403, 404, 500, etc.) automatically"""
    return render_template(
        'error.html',
        code=e.code,
        title=e.name,             # e.g., "Bad Request", "Not Found"
        description=e.description # Default description provided by Flask/Werkzeug
    ), e.code

if __name__ == '__main__':
    # debug=True automatically reloads the app when you save changes
    app.run(debug=True)