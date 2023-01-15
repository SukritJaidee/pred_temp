import time
import pytz
import schedule
import warnings
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from pycaret.regression import *
from datetime import datetime, timedelta, date, tzinfo
warnings.filterwarnings("ignore")

from x3_ibm_api import x3_api
from tmd_api import tmd_weather
from x4_weather_api import x4_api
from x1_station_meteo_api import x1_api
from loc_level10 import get_level10_pos
from x2_point_meteo_api import x2_api, x1_station_x2

def cal_from_source(q1, now_datetime, format_date, saved_lr):
  #### x0
  diff_time, hour, duration = 0, 0, 24
  day = (datetime.now(pytz.timezone('Asia/Bangkok'))+timedelta(diff_time)).strftime("%Y-%m-%d")
  x0 = tmd_weather(q1[0], q1[1], day, hour, duration)
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
  
## Initial value
df = get_level10_pos()
models = 'Blend'
saved_lr = load_model(models)
cols = ['lat', 'lon', 'latitude', 'longitude', 'elevation', 'distance', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'year', 'month', 'day', 'hour', 'minute', 'temp.1', 'dwpt.1', 'rhum.1', 'wdir.1', 'wspd.1',
                  'pres', 'lat.1', 'lon.1', 'year.1', 'month.1', 'day.1', 'hour.1', 'minute.1', 'requestedLatitude', 'requestedLongitude', 'latitude.1', 'longitude.1', 'precip1Hour', 'precip6Hour', 'precip24Hour', 'pressureChange',
                  'pressureMeanSeaLevel', 'relativeHumidity', 'temperature', 'temperatureChange24Hour', 'temperatureMax24Hour', 'temperatureMin24Hour', 'temperatureDewPoint', 'temperatureFeelsLike', 'uvIndex',
                  'visibility', 'windDirection', 'windSpeed', 'lat.2', 'lon.2', 'lats', 'lons', 'temp_cs', 'wind_kphs', 'wind_degrees', 'wind_dirs', 'pressure_mbs', 'precip_mms', 'humiditys', 'clouds', 'feelslike_cs',
                  'windchill_cs', 'heatindex_cs', 'dewpoint_cs', 'will_it_rains', 'chance_of_rains', 'vis_kms', 'gust_kphs']

def deploy_schedule(df, now_datetime, format_date, saved_lr, start_cp):
    k = 0
    for  i in tqdm(range(len(df))):
        lat, lon = df['lat_south'][i], df['lon_east'][i]
        q1 = (lat, lon)
        try:
            if k == 0:
              res_update = cal_from_source(q1, now_datetime, format_date, saved_lr)
            else:
              res = cal_from_source(q1, now_datetime, format_date, saved_lr)
              res_update = pd.concat([res_update, res], axis=0)
            k+=1
        except:
            try:
                res_update_v, res_v = res_update.values, res.values
                cols_raw = res_update.columns
                res_update = np.concatenate((res_update_v, res_v), axis=0)
                res_update = pd.DataFrame(res_update, columns=cols_raw)
            except:
                print(f'error i ={i}, lat = {lat}, lon = {lon}')
    #calculate
    res1 = res_update.drop(['tc', 'rh', 'datatime'], axis=1)
    res1.columns = cols
    res1.reset_index(drop=True, inplace=True)
    
    unseen_pred = predict_model(saved_lr, data=res1)
    actual = res_update[['tc', 'datatime']]
    actual.reset_index(drop=True, inplace=True)
    res2 = pd.concat([unseen_pred, actual], axis=1,  join="inner")

    df_val = res2[['prediction_label', 'tc', 'temperature', 'datatime']]
    df_loc = res1[['lat', 'lon']]
    result = pd.concat([df_loc, df_val], axis=1,  join="inner")

    success = True
    end_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
    delta = end_cp - start_cp
    min = (delta.total_seconds()) / 60
    print('minutes:', min)
    start_cp, end_cp = start_cp.strftime("%d_%m_%Y_%H_%M"), end_cp.strftime("%d_%m_%Y_%H_%M")
    info = pd.DataFrame({'success':[str(success)], 'datetime':[str(start_cp)], 'start_compute':[str(start_cp)], 'end_compute':[str(end_cp)]})
    info.to_csv('/data/'+'data_'+start_cp+'_info.csv' ,encoding='utf-8-sig')
    result.to_csv('/data/'+'data_'+start_cp+'_data.csv' ,encoding='utf-8-sig')
    return True

def job():
    format_date = "%Y-%m-%d %H:%M:%S"
    now_datetime = datetime.now(pytz.timezone('Asia/Bangkok'))
    start_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
    print("I'm working...")
    print("I'm working %s"%(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    success_r = deploy_schedule(df, now_datetime, format_date, saved_lr, start_cp)
    print(success_r)

# Run job every hour at the 42rd minute
schedule.every().hour.at(":05").do(job)

# Run jobs every 5th hour, 20 minutes and 30 seconds in.
# If current time is 02:00, first execution is at 06:20:30
# schedule.every(5).hours.at("20:30").do(job)

# Run job every day at specific HH:MM and next HH:MM:SS
# schedule.every().day.at("10:30").do(job)
# schedule.every().day.at("10:30:42").do(job)

while True:
    schedule.run_pending()
    # time.sleep(1)