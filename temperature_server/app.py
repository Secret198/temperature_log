from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Temperature
from datetime import datetime, time
from werkzeug.exceptions import HTTPException
from sqlalchemy import text, func
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

    query = text("""
        SELECT count(temperature)     
            FROM temperature
            WHERE timestamp >= datetime('now', '-1 day', 'localtime')
    """)

    temp_count = db.session().execute(query).scalar()

    

    if temp_count < 50:
        query = text("""SELECT 
                        temperature,
                        strftime('%Y-%m-%d %H:%M:%S', timestamp) AS timestamp
                    FROM temperature
                    WHERE timestamp >= datetime('now', '-1 day', 'localtime')""")
        temperatures = db.session.execute(query).mappings()
        # temperatures = db.session.execute(db.select(Temperature).order_by(Temperature.timestamp.asc())).scalars()
    else:
        query = text("""
                SELECT 
                    strftime('%H', timestamp) AS hour_num,
                    ROUND(AVG(temperature), 2) AS temperature,
                    strftime('%Y-%m-%d %H:%M:%S', timestamp) AS timestamp,
                    COUNT(*) AS record_count
                FROM temperature
                WHERE timestamp >= datetime('now', '-1 day', 'localtime')
                GROUP BY hour_num
                ORDER BY hour_num ASC;
            """)
        
        result = db.session.execute(query)
        temperatures = result.mappings().all()
    return render_template('index.html', temperatures=temperatures)

@app.route("/ev/<year>")
def based_on_year(year):
    
    query = text("""
        SELECT 
            strftime('%m', timestamp) AS month_num,
            ROUND(AVG(temperature), 2) AS temperature,
            strftime('%Y-%m', timestamp) AS timestamp,
            COUNT(*) AS record_count
        FROM temperature
        WHERE strftime('%Y', timestamp) = :year
        GROUP BY month_num
        ORDER BY month_num ASC;
    """)

    result = db.session.execute(query, {"year": year})
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])

@app.route("/ev/honap/<year_month>")
def based_on_year_month(year_month):
    
    query = text("""
            SELECT 
                strftime('%d', timestamp) AS day_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y-%m-%d', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            WHERE strftime('%Y-%m', timestamp) = :year_month
            GROUP BY day_num
            ORDER BY day_num ASC;
        """)
    
    result = db.session.execute(query, {"year_month": year_month})
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


@app.route("/ev/honap/nap/<year_month_day>")
def based_on_year_month_day(year_month_day):
    
    query = text("""
            SELECT 
                strftime('%H', timestamp) AS hour_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y-%m-%d %H', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            WHERE strftime('%Y-%m-%d', timestamp) = :year_month_day
            GROUP BY hour_num
            ORDER BY hour_num ASC;
        """)
    
    result = db.session.execute(query, {"year_month_day": year_month_day})
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


@app.route("/last_week")
def last_week():
    
    query = text("""
            SELECT 
                strftime('%d', timestamp) AS day_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y-%m-%d', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            WHERE timestamp >= datetime('now', '-7 day', 'localtime')
            GROUP BY day_num
            ORDER BY day_num ASC;
        """)
    
    result = db.session.execute(query)
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


@app.route("/last_month")
def last_month():
    
    query = text("""
            SELECT 
                strftime('%d', timestamp) AS month_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y-%m-%d', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            WHERE timestamp >= datetime('now', '-1 month', 'localtime')
            GROUP BY month_num
            ORDER BY month_num ASC;
        """)
    
    result = db.session.execute(query)
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


@app.route("/last_year")
def last_year():
    
    query = text("""
            SELECT 
                strftime('%m', timestamp) AS month_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y-%m', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            WHERE timestamp >= datetime('now', '-1 year', 'localtime')
            GROUP BY month_num
            ORDER BY month_num ASC;
        """)
    
    result = db.session.execute(query)
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


@app.route("/all")
def all():
    
    query = text("""
            SELECT 
                strftime('%Y', timestamp) AS year_num,
                ROUND(AVG(temperature), 2) AS temperature,
                strftime('%Y', timestamp) AS timestamp,
                COUNT(*) AS record_count
            FROM temperature
            GROUP BY year_num
            ORDER BY year_num ASC;
        """)
    
    result = db.session.execute(query)
    temperatures = result.mappings().all()
    # return render_template('index.html', temperatures=temperatures)
    return jsonify([dict(row) for row in temperatures])


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