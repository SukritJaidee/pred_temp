import pytz
import json
import requests
import pandas as pd
from datetime import datetime, timedelta, date, tzinfo

save_x4_filename = "x4_data"
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
# now_datetime = datetime(2022, 12, 5, 0, 0, 0, tzinfo=pytz.timezone('Asia/Bangkok'))
format_date = "%Y-%m-%d"
start_date, end_date = 0, 1
DATE_MIN = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
DATE_MAX = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
# print(DATE_MIN, DATE_MAX)

def weather_history(lat, lon, DATE_MIN, DATE_MAX):
  #DATE_MIN, DATE_MAX = "2021-12-01", "2022-01-02"
  DATES = pd.date_range(start=DATE_MIN, end=DATE_MAX)
  API_KEY = "00045b3f7ee04112ae3170131231902"
  times, temp_cs, wind_mphs, wind_kphs = [], [], [], []
  wind_degrees, wind_dirs, pressure_mbs = [], [], []
  pressure_ins, precip_mms, precip_ins, humiditys = [], [], [], []
  clouds, feelslike_cs, windchill_cs, heatindex_cs, dewpoint_cs, will_it_rains = [],  [],  [],  [], [], []
  chance_of_rains, will_it_snows, chance_of_snows, vis_kms = [],  [], [], []
  vis_miless, gust_mphs, gust_kphs = [], [], []
  lats, lons = [], []
  for date in DATES:
    try:
      date = date.date()
      payload, headers={}, {}
      url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={lat},{lon}&dt={date}"
      response = requests.request("GET", url, headers=headers, data=payload)
      print(response)
      data = json.loads(response.text)  
      A = data['forecast']['forecastday'][0]['hour']
      for k in range(24):
        timex =    A[k]['time']
        temp_c = A[k]['temp_c']
        wind_kph = A[k]['wind_kph']
        wind_degree = A[k]['wind_degree']
        wind_dir =       A[k]['wind_dir']
        pressure_mb = A[k]['pressure_mb']
        precip_mm = A[k]['precip_mm']
        humidity = A[k]['humidity']
        cloud = A[k]['cloud']
        feelslike_c = A[k]['feelslike_c']
        windchill_c = A[k]['windchill_c']
        heatindex_c = A[k]['heatindex_c']
        dewpoint_c = A[k]['dewpoint_c']
        will_it_rain = A[k]['will_it_rain']
        chance_of_rain = A[k]['chance_of_rain']
        vis_km =  A[k]['vis_km']
        gust_kph = A[k]['gust_kph']
        lats.append(lat)
        lons.append(lon)
        times.append(timex)
        temp_cs.append(temp_c)
        wind_kphs.append(wind_kph)
        wind_degrees.append(wind_degree)
        wind_dirs.append(wind_dir)
        pressure_mbs.append(pressure_mb)
        precip_mms.append(precip_mm)
        humiditys.append(humidity)
        clouds.append(cloud)
        feelslike_cs.append(feelslike_c)
        windchill_cs.append(windchill_c)
        heatindex_cs.append(heatindex_c)
        dewpoint_cs.append(dewpoint_c)
        will_it_rains.append(will_it_rain)
        chance_of_rains.append(chance_of_rain)
        vis_kms.append(vis_km)
        gust_kphs.append(gust_kph)
    except:
      print('error')
  data_dic = {
      'times':times, 'lat':lats, 'lon':lons,
      'temp_cs':temp_cs, 'wind_kphs':wind_kphs, 'wind_degrees':wind_degrees, 'wind_dirs':wind_dirs, 'pressure_mbs':pressure_mbs,
      'precip_mms':precip_mms, 'humiditys':humiditys, 'clouds':clouds, 'feelslike_cs':feelslike_cs, 'windchill_cs':windchill_cs, 'heatindex_cs':heatindex_cs,
      'dewpoint_cs':dewpoint_cs, 'will_it_rains':will_it_rains, 'chance_of_rains':chance_of_rains, 'vis_kms':vis_kms, 'gust_kphs':gust_kphs
      }
  df = pd.DataFrame(data_dic)
  return df

def x4_api(q1, DATE_MIN, DATE_MAX):
    DATES = pd.date_range(start=DATE_MIN, end=DATE_MAX)
    x4 = weather_history(q1[0], q1[1], DATE_MIN, DATE_MAX)
    x4['wind_dirs'] = x4['wind_dirs'].astype('category').cat.codes
    x4['times'] = x4['times'].astype('datetime64[ns]')
    # this_time  = x2.index.to_list()[0].strftime("%Y-%m-%d %H:%M:%S")
    # x4 = x4[x4['times']==this_time]
    x4.index = x4['times']
    x4.drop(['times'], axis=1, inplace=True)
    x4['lat'] =x4['lat'].astype('float32')
    x4['lon'] =x4['lon'].astype('float32')
    x4.rename(columns={'temp_cs':'temp_x4'}, inplace=True)

    # x4.to_csv(save_x4_filename+'.csv' ,encoding='utf-8-sig')
    # print(x4.shape); display(x4.head(1)); display(x4.tail(1));
    # print('x4', end = ' '); print(x4.index[0], end = ' '); print(x4.index[-1]);
    return x4
