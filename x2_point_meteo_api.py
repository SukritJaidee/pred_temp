import pandas as pd
from meteostat import Point, Daily, Hourly, Stations
from datetime import datetime, timedelta, date, tzinfo

save_x2_filename = "x2_data"

def get_data(q, start, end):
  df_temp = pd.DataFrame([])
  df_temp['lat'], df_temp['lon'] = pd.Series(q[0]), pd.Series(q[1])
  station_point = Point(q[0],  q[1])
  data = Hourly(station_point, start, end, timezone="Asia/Bangkok")
  data = data.fetch()
  #print(data)
  data['lat'], data['lon'] = data['temp'].map(lambda x: df_temp['lat'][0]), data['temp'].map(lambda x: df_temp['lon'][0])
  return data

def x2_api(q1, start, end):
    x2 = get_data(q1, start, end)
    x2.drop(['snow', 'wpgt', 'tsun', 'coco', 'prcp'], axis=1, inplace=True)
    x2['datetime'] = x2.index.astype(str)
    x2['datetime'] = x2['datetime'].apply(lambda x: datetime.strptime(x[:-6], "%Y-%m-%d %H:%M:%S"))
    change_list = ['temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'lat', 'lon']
    for col_name in change_list: x2[col_name] =x2[col_name].astype('float32')
    x2["year"]   = x2['datetime'].astype('datetime64[ns]').apply(lambda x: x.year)
    x2["month"]  = x2['datetime'].astype('datetime64[ns]').apply(lambda x: x.month)
    x2["day"]    = x2['datetime'].astype('datetime64[ns]').apply(lambda x: x.day)
    x2["hour"]   = x2['datetime'].astype('datetime64[ns]').apply(lambda x: x.hour)
    x2["minute"] = x2['datetime'].astype('datetime64[ns]').apply(lambda x: x.minute)
    x2.index = x2['datetime']
    x2.drop(['datetime'], axis=1, inplace=True)
    x2.rename(columns={'temp':'temp_x2'}, inplace=True)
    x2.to_csv(save_x2_filename+'.csv' ,encoding='utf-8-sig')
    # print(x2.shape); display(x2.head(1)); display(x2.tail(1));
    # print('x2', end = ' '); print(x2.index[0], end = ' '); print(x2.index[-1]);
    return x2
    
def x1_station_x2(q1, start=0, end=1):
  s1 = near_station(q1[0], q1[1])
  now_datetime, format_date = datetime.now(pytz.timezone('Asia/Bangkok')),  "%Y-%m-%d %H:%M:%S"
  start = pd.to_datetime((now_datetime+timedelta(hours=start)).strftime(format_date))
  end = pd.to_datetime((now_datetime+timedelta(hours=end)).strftime(format_date))
  try: x1 = sel_col_r_x2(q1, s1, start, end)
  except: x1 = sol_error_x2(q1, start, end)
  x1.drop(['wmo', 'icao'], axis=1, inplace=True)
  x1['distance'] = x1['distance'].apply(lambda x: x/1000)
  data = []
  for i in range(x1.shape[0]):
    data.append(datetime(int(x1['year'][i]), int(x1['month'][i]), int(x1['day'][i]), int(x1['hour'][i]), int(x1['minute'][i])))
  datetime_df = pd.DataFrame(data, columns = ['datetime'])
  x1 = pd.concat((datetime_df, x1), axis=1)
  change_list = ['lat', 'lon', 'latitude','longitude', 'elevation', 'distance', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'year', 'month', 'day', 'hour', 'minute']
  for col_name in change_list:
    x1[col_name] =x1[col_name].astype('float32')
  x1.index = x1['datetime']
  x1.drop(['datetime'], axis=1, inplace=True)
  return x1