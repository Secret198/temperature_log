from models import db
from datetime import datetime
from sqlalchemy import text
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def calculate_forecast(data_raw):
    df = pd.DataFrame(data_raw)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    df = df.sort_index()
    df = df[~df.index.duplicated(keep='first')]
    
    df = df.resample('h').mean()
    df['temperature'] = df['temperature'].interpolate(method='linear')
    
    df['temperature'] = df['temperature'].ffill().bfill()
    
    model = ARIMA(df["temperature"])
    results = model.fit()
    return results.get_forecast(24).summary_frame()
