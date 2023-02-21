# -*- coding: utf-8 -*-
"""weather_submit_v1_04025566_1250.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hSSRyLhanIMrE4L9xIknK1uW0atAmFT_
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Import libraries
#!git clone https://github.com/SukritJaidee/pred_temp.git 
# %cd /content/pred_temp

#!pip install -q meteostat
#!pip install -q mercantile
#!pip install -q mpmath

import pytz
import json
import warnings
import requests
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
# from pycaret.regression import *
from tqdm.notebook import tqdm
from datetime import datetime, timedelta, date, tzinfo
warnings.filterwarnings("ignore")

from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from pred_temp.x3_ibm_api import x3_api
from pred_temp.tmd_api import tmd_weather
from pred_temp.x4_weather_api import x4_api
from pred_temp.x6_meteo import open_meteo_v1
from pred_temp.loc_level10 import get_level10_pos
from pred_temp.x1_station_meteo_api import x1_api
from pred_temp.x2_point_meteo_api import x2_api, x1_station_x2

path_save = 'drive/MyDrive/result_weather/'
path = '/content/drive/MyDrive/chula_weather/one_model/keras_model/'
root_path =  '/content/drive/MyDrive/chula_weather/one_model/last_dataset/'
df = get_level10_pos()

#@title Model
def ann_model_api(X_train):
      input_shape = X_train.shape[1:]
      normalizer = layers.Normalization()
      normalizer.adapt(X_train)
      inputs = keras.Input(shape=input_shape)
      x = normalizer(inputs)
      x = layers.Dense(64, activation="relu")(x)
      x = layers.Dropout(0.2)(x)
      x = layers.Dense(32, activation="relu")(x)
      x = layers.Dropout(0.2)(x)
      outputs = layers.Dense(1, activation="relu")(x)
      model = keras.Model(inputs, outputs)
      loss = tf.keras.losses.MeanSquaredError(name="mse")
      optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
      m1 = tf.keras.metrics.RootMeanSquaredError()
      m2 = tf.keras.metrics.MeanAbsoluteError()
      model.compile( optimizer=optimizer,  loss = loss, metrics = [m1, m2])
      return model

#@title Model v1
df = pd.read_csv(root_path+'data_pmwa.csv')
x, y = df.drop("temp_2m", axis = 1), df[["temp_2m"]]
x.drop(['wspeed_100m', 'wdirection_100m', 'soil_temp_0_to_7cm', 'soil_temp_7_to_28cm'], axis =1, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(x, y,  test_size=0.2, shuffle=True)

models = 'keras_api_best_model2_v1.h5'
model = ann_model_api(X_train)
model.load_weights(path+models)

format_date = "%Y-%m-%d %H:%M:%S"
start_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
lats, lons, datetimes, pred_vals, tmd_vals, x_tiles, y_tiles = [], [], [],  [], [],  [], []

cols =  [
              'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'lat', 'lon', 'year', 'month', 'day', 'hour', 'minute',  #x2 point meteostat
              'temp_2m', 'rh_2m', 'dewpoint_2m', 'apparent_temp', 'rain', 'cloudcover', 'cloudcover_low', 'cloudcover_mid', 'cloudcover_high', #x6 meteo
              'shortwave_rad', 'direct_rad', 'diffuse_rad', 'direct_normal_irr', 'wspeed_10m', 
              # 'wspeed_100m',
              'wdirection_10m',
              # 'wdirection_100m',
              'wgusts_10m', #x6 meteo
              # 'soil_temp_0_to_7cm', 'soil_temp_7_to_28cm', #x6 meteo
              'lat.1', 'lon.1', 'elevation', 'lat_res', 
              'lon_res', 'lats', 'lons', 'temp_cs', 'wind_kphs', 'wind_degrees', 'wind_dirs', 'pressure_mbs', 'precip_mms', 'humiditys', #x4 weatherapi
             'clouds', 'feelslike_cs', 'windchill_cs', 'heatindex_cs', 'dewpoint_cs', 'will_it_rains', 'chance_of_rains', 'vis_kms', 'gust_kphs' #x4 weatherapi
              ]

def cal_from_source(q1, now_datetime, format_date, model):
  #### x0 tmd
  diff_time, hour, duration = 0, 0, 24
  day = (datetime.now(pytz.timezone('Asia/Bangkok'))+timedelta(diff_time)).strftime("%Y-%m-%d")
  x0 = tmd_weather(q1[0], q1[1], day, hour, duration)
  #### x2 point meteostat
  start_date, end_date = -1, 1
  start = pd.to_datetime((now_datetime+timedelta(start_date)).strftime(format_date)) 
  end = pd.to_datetime((now_datetime+timedelta(end_date)).strftime(format_date))
  x2 = x2_api(q1, start, end)
  if x2.shape[0] == 0:
    x2 = x1_station_x2(q1, start=-1, end=0)
    x2.drop(['latitude', 'longitude', 'elevation', 'distance'], axis=1, inplace=True)
    x2 = x2.reindex(columns=['temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'lat', 'lon', 'year', 'month', 'day', 'hour', 'minute'])
  #### x6 meteo
  format_date, start_date, end_date = "%Y-%m-%d", 0, 0
  start = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
  end = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
  x6 = open_meteo_v1(q1[0], q1[1], start, end)
  x6.index = x6['datetime1']
  x6.drop(['indexs', 'time', 'datetime1'], axis =1, inplace=True)
  #### x4 weatherapi
  format_date, start_date, end_date = "%Y-%m-%d", -1, 1
  start = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
  end = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
  x4  = x4_api(q1, start, end)
  #### concat
  res = pd.concat([x2, x6, x4], axis=1,  join="inner")
  res.columns = cols
  temp_po = res[['temp_2m']].iloc[-1:,:]
  temp_po.reset_index(drop=True, inplace=True)
  res = res.drop(['temp_2m'], axis=1)
  one_res = res.iloc[-1:,:]
  
  y_pred = model.predict(one_res, verbose=0)
  y_pred = pd.DataFrame(y_pred, columns = ['ypred'])

  actual = x0[['tc', 'datatime']]
  one_actual = actual.iloc[-1:,:]
  one_actual.reset_index(drop=True, inplace=True)

  res2 = pd.concat([y_pred, one_actual, temp_po], axis=1,  join="inner")
  data = res2.iloc[-1:,:]
  return data

for  i in tqdm(range(len(df))):
  lat, lon = df['lat_south'][i], df['lon_east'][i]
  x_tile, y_tile = df['x_tiles'][i], df['y_tiles'][i]
  q1 = (lat, lon)
  try:
      data = cal_from_source(q1, now_datetime, format_date, model)
      pred_val, tmd = data['ypred'][0], data['tc'][0]
      x_tiles.append(x_tile); y_tiles.append(y_tile); 
      lats.append(lat); lons.append(lon); pred_vals.append(pred_val); tmd_vals.append(tmd);
  except Exception as e:
      print(e)
      pred_val, tmd = data['temp_2m'][0], data['tc'][0]
      lats.append(lat); lons.append(lon);
      x_tiles.append(x_tile); y_tiles.append(y_tile); 
      pred_vals.append(pred_val); tmd_vals.append(tmd);
      print(f"Error  lat = {round(q1[0],2)} lon = {round(q1[1],2)}")

success = True
end_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
min = ((end_cp - start_cp).total_seconds())/60
print('minutes:', min)

format_save = "%d%m%Y-%H:%M"
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
save_datetime = now_datetime.strftime(format_save) 
info_data = {'success':[success], 'datetime':[save_datetime],'start_compute':[start_cp],'end_compute':[end_cp]}
df5 = pd.DataFrame({'lat':lats,'lon':lons,'x_tiles':x_tiles, 'y_tiles':y_tiles, 'blend temp':pred_vals,'TMD temp':tmd_vals,})
df6 = pd.DataFrame(info_data)
df5.to_csv('/content/'+path_save+'data/onetime/'+save_datetime+'_data.csv' ,encoding='utf-8-sig')
df6.to_csv('/content/'+path_save+'data/onetime/'+save_datetime+'_info.csv' ,encoding='utf-8-sig')