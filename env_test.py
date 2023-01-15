import pycaret
from platform import python_version
print('pycaret', pycaret.__version__)
print("Python", python_version())

import pytz
import warnings
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from pycaret.regression import *
from datetime import datetime, timedelta, date, tzinfo
from tmd_api import tmd_weather
from x3_ibm_api import x3_api
from x4_weather_api import x4_api
from x1_station_meteo_api import x1_api
from x2_point_meteo_api import x2_api, x1_station_x2
from loc_level10 import get_level10_pos
warnings.filterwarnings("ignore")

def cal_from_source(q1, now_datetime, format_date, saved_lr):
  #### x0
  diff_time, hour, duration = 0, 0, 24
  day = (datetime.now(pytz.timezone('Asia/Bangkok'))+timedelta(diff_time)).strftime("%Y-%m-%d")
  x0 = tmd_weather(lat, lon, day, hour, duration)
  #### x1
  start_date, end_date = -1, 1
  start = pd.to_datetime((now_datetime+timedelta(start_date)).strftime(format_date))
  end = pd.to_datetime((now_datetime+timedelta(end_date)).strftime(format_date))
  x1 = x1_api(q1, start, end)
  #### x2
  x2 = x2_api(q1, start, end)
  if x2.shape[0] == 0:
    x2 = x1_station_x2(q1, start=-1, end=1)
    x2.drop(['latitude', 'longitude', 'elevation', 'distance'], axis=1, inplace=True)
    x2 = x2.reindex(columns=['temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'lat', 'lon', 'year', 'month', 'day', 'hour', 'minute'])
  #### x3
  apikey =  "2601b3bc3f684d2681b3bc3f687d26f8"
  format_date, start_date, end_date  = "%Y-%m-%d", 0, 1
  start = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
  end = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
  x3 = x3_api(q1, start, end, apikey)
  #### x4
  x4  = x4_api(q1, start, end)
  res = pd.concat([x0, x1, x2, x3, x4], axis=1,  join="inner")
  res  = res.iloc[-1:,:]
  return res

### Debug
df = get_level10_pos()
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
format_date = "%Y-%m-%d %H:%M:%S"
models = r"C:/Users/EGAT/PycharmProjects/pred_temp/Blend"

lats, lons, datetimes, pred_vals, tmd_vals = [], [], [],  [], []
saved_lr = load_model(models)
start_cp = datetime.now(pytz.timezone('Asia/Bangkok'))

i_1, i_2 = 10, 11
lat, lon = df['lat_south'][i_1], df['lon_east'][i_1]
res_update = cal_from_source((lat, lon), now_datetime, format_date, saved_lr)

lat, lon = df['lat_south'][i_2], df['lon_east'][i_2]
res = cal_from_source((lat, lon), now_datetime, format_date, saved_lr)

res_update_v, res_v = res_update.values, res.values
cols_raw = res_update.columns
data = np.concatenate((res_update_v, res_v), axis=0)
data = pd.DataFrame(data, columns=cols_raw)
print('shape:', data.shape); print(data);

cols = ['lat', 'lon', 'latitude', 'longitude', 'elevation', 'distance', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'year', 'month', 'day', 'hour', 'minute', 'temp.1', 'dwpt.1', 'rhum.1', 'wdir.1', 'wspd.1',
                  'pres', 'lat.1', 'lon.1', 'year.1', 'month.1', 'day.1', 'hour.1', 'minute.1', 'requestedLatitude', 'requestedLongitude', 'latitude.1', 'longitude.1', 'precip1Hour', 'precip6Hour', 'precip24Hour', 'pressureChange',
                  'pressureMeanSeaLevel', 'relativeHumidity', 'temperature', 'temperatureChange24Hour', 'temperatureMax24Hour', 'temperatureMin24Hour', 'temperatureDewPoint', 'temperatureFeelsLike', 'uvIndex',
                  'visibility', 'windDirection', 'windSpeed', 'lat.2', 'lon.2', 'lats', 'lons', 'temp_cs', 'wind_kphs', 'wind_degrees', 'wind_dirs', 'pressure_mbs', 'precip_mms', 'humiditys', 'clouds', 'feelslike_cs',
                  'windchill_cs', 'heatindex_cs', 'dewpoint_cs', 'will_it_rains', 'chance_of_rains', 'vis_kms', 'gust_kphs']

res1 = data.drop(['tc', 'rh', 'datatime'], axis=1)
res1.columns = cols
res1.reset_index(drop=True, inplace=True)
unseen_pred = predict_model(saved_lr, data=res1)
print('unseen_pred', unseen_pred)