from math import *
import mercantile
import pandas as pd
from mpmath import sec
from tqdm.notebook import tqdm

thai_dict, zoom = {'North':{'lat_min':17.298, 'lat_max':20.530, 'lon_min':97.262, 'lon_max':101.382},
             'Center':{'lat_min':14.169 , 'lat_max':18.480, 'lon_min':98.141, 'lon_max':105.667},
             'Center_bottom':{'lat_min':11.351 , 'lat_max':14.169, 'lon_min':98.646, 'lon_max':103.107},
             'South':{'lat_min':5.567 , 'lat_max':11.351, 'lon_min':97.690, 'lon_max':102.112},
             'Thai': {'lat_min':5.69138418215 , 'lat_max':20.4178496363, 'lon_min':97.3758964376, 'lon_max':105.589038527},
             }, 10

def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return (int(tile_count*x), int(tile_count*y))

def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return (floor(x_min), floor(x_max), floor(y_min), floor(y_max))

def get_level10_pos():
    x_list, y_list  = [], []
    lon_west, lon_east, lat_south, lat_north  = [], [], [], []
    x_min, x_max, y_min, y_max = bbox_to_xyz(thai_dict['Thai']['lon_min'], thai_dict['Thai']['lon_max'], thai_dict['Thai']['lat_min'], thai_dict['Thai']['lat_max'], zoom)
    print(f"Downloading {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

    for x in tqdm(range(x_min, x_max + 1)):
        for y in range(y_min, y_max + 1):
          lat_lon = mercantile.bounds(mercantile.Tile(x=x, y=y, z=10))
          x_list.append(x); y_list.append(y);
          lon_west.append(lat_lon[0]); lat_south.append(lat_lon[1]);
          lon_east.append(lat_lon[2]); lat_north.append(lat_lon[3]);
    df = pd.DataFrame({'lon_west': lon_west, 'lat_north':lat_north, 'lat_south':lat_south, 'lon_east':lon_east})
    print(df.shape); print(df.head(1));
    return df