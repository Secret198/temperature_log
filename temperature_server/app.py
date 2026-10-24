from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Temperature
from datetime import datetime, time
from werkzeug.exceptions import HTTPException
from sqlalchemy import text, func
from marshmallow import Schema, fields, validate, ValidationError
from forecast import calculate_forecast

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
    all_records = Temperature.get_all_records()
    forecast_df = calculate_forecast(all_records)

    forecast_data = []
    for timestamp, row in forecast_df.iterrows():
        forecast_data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': round(float(row['mean']), 2),
            'lower_bound': round(float(row['mean_ci_lower']), 2),
            'upper_bound': round(float(row['mean_ci_upper']), 2)
        })
    print(forecast_data)

    temp_count = Temperature.get_today_count()

    if temp_count < 50:
       
        temperatures = Temperature.get_all_today()
    else:
        
        temperatures = Temperature.get_hourly_today()
    print(temperatures)
    return render_template('index.html', temperatures=temperatures)

@app.route("/ev/<year>")
def based_on_year(year):
    temperatures = Temperature.based_on_year(year)
    return jsonify([dict(row) for row in temperatures])

@app.route("/ev/honap/<year_month>")
def based_on_year_month(year_month):
    temperatures = Temperature.based_on_year_month(year_month)
    return jsonify([dict(row) for row in temperatures])

@app.route("/ev/honap/nap/<year_month_day>")
def based_on_year_month_day(year_month_day):
    temperatures = Temperature.based_on_year_month_day(year_month_day)
    return jsonify([dict(row) for row in temperatures])

@app.route("/last_week")
def last_week():
    temperatures = Temperature.last_week()
    return jsonify([dict(row) for row in temperatures])

@app.route("/last_month")
def last_month():
    temperatures = Temperature.last_month()
    return jsonify([dict(row) for row in temperatures])

@app.route("/last_year")
def last_year():
    temperatures = Temperature.last_year()
    return jsonify([dict(row) for row in temperatures])

@app.route("/yearly")
def yearly():
    temperatures = Temperature.yearly()
    return jsonify([dict(row) for row in temperatures])

@app.route("/all")
def all_route():
    temperatures = Temperature.get_all_records()
    return jsonify([dict(row) for row in temperatures])

@app.route('/add', methods=['POST'])
def add_temp():
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