from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, unique=False, nullable=False)
    timestamp = db.Column(db.DateTime, unique=True, nullable=False)

    def __repr__(self):
        return f''

    @classmethod
    def get_today_count(cls):
        query = text("""
                SELECT count(temperature)     
                    FROM temperature
                    WHERE timestamp >= datetime('now', '-1 day', 'localtime')
            """)
        
        return db.session().execute(query).scalar()

    @classmethod
    def get_all_today(cls):
        query = text("""SELECT 
                        temperature,
                        strftime('%Y-%m-%d %H:%M:%S', timestamp) AS timestamp
                    FROM temperature
                    WHERE timestamp >= datetime('now', '-1 day', 'localtime')
                    ORDER BY timestamp ASC
                    """)
        return db.session.execute(query).mappings()

    @classmethod
    def get_hourly_today(cls):
        query = text("""
                SELECT 
                    strftime('%H', timestamp) AS hour_num,
                    ROUND(AVG(temperature), 2) AS temperature,
                    strftime('%Y-%m-%d %H:%M:%S', timestamp) AS timestamp,
                    COUNT(*) AS record_count
                FROM temperature
                WHERE timestamp >= datetime('now', '-1 day', 'localtime')
                GROUP BY hour_num
                ORDER BY timestamp ASC;
            """)
        
        result = db.session.execute(query)
        return result.mappings().all()

    @classmethod
    def based_on_year(cls, year):
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
        return result.mappings().all()

    @classmethod
    def based_on_year_month(cls, year_month):
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
        return result.mappings().all()

    @classmethod
    def based_on_year_month_day(cls, year_month_day):
        query = text("""
                SELECT 
                    strftime('%H', timestamp) AS hour_num,
                    ROUND(AVG(temperature), 2) AS temperature,
                    strftime('%Y-%m-%d %H', timestamp) AS timestamp,
                    COUNT(*) AS record_count
                FROM temperature
                WHERE strftime('%Y-%m-%d', timestamp) = :year_month_day
                GROUP BY hour_num
                ORDER BY timestamp ASC;
            """)
        result = db.session.execute(query, {"year_month_day": year_month_day})
        return result.mappings().all()

    @classmethod
    def last_week(cls):
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
        return result.mappings().all()

    @classmethod
    def last_month(cls):
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
        return result.mappings().all()

    @classmethod
    def last_year(cls):
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
        return result.mappings().all()

    @classmethod
    def yearly(cls):
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
        return result.mappings().all()

    @classmethod
    def get_all_records(cls):
        query = text("""
                SELECT * FROM temperature;
            """)
        result = db.session.execute(query)
        return result.mappings().all()