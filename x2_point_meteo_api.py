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