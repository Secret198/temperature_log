from models import db
from datetime import datetime
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def calculate_forecast(data_raw):
    df = pd.DataFrame(data_raw)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    df = df.resample("h").mean()
    df["temperature"] = df["temperature"].interpolate(method="linear", limit=3)

    print(len(df), df.index.min(), df.index.max())   

    if len(df) < 72:                     
        raise ValueError("Not enough hourly data for a seasonal forecast")

    model = SARIMAX(
        df["temperature"],
        order=(1, 0, 1),
        seasonal_order=(1, 1, 1, 24),   
        trend=None,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    results = model.fit(disp=False)
    print(results.summary())

    forecast_df = results.get_forecast(24).summary_frame()

    forecast_data = []
    for timestamp, row in forecast_df.iterrows():
        forecast_data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': round(float(row['mean']), 2),
            'lower_bound': round(float(row['mean_ci_lower']), 2),
            'upper_bound': round(float(row['mean_ci_upper']), 2)
        })
    

    return forecast_data