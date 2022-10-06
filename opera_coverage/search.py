from shapely.geometry import Polygon
from typing import List
from datetime import datetime, timedelta
from pystac_client import Client
from . import formatting as f
import asf_search as asf
import pandas as pd
import geopandas as gpd

def hls_search(sensor: str, aoi: Polygon, date: List[datetime] = None) -> list:
    """For searching for sentinel2 and landsat8 data

    Args:
        sensor (str): singular sensor name, can be 'landsat8' or 'sentinel2'
        aoi (Polygon): area of interest as shapely Polygon
        date (List[datetime], optional): leave as none if searching today, else enter time range as datetime tuple: datetime(YYYY,MM,DD). Defaults to None.

    Returns:
        list: search results from HLS
    """
    STAC_URL = 'https://cmr.earthdata.nasa.gov/stac'
    api = Client.open(f'{STAC_URL}/LPCLOUD/')
    
    if 'sentinel2' in sensor.lower():
        hls_collections = ['HLSS30.v2.0']
    elif 'landsat8_9' in sensor.lower():
        hls_collections = ['HLSL30.v2.0']
    
    if date == None:
        search_datetime = [datetime.combine(date.today(), datetime.min.time()), datetime.now()]
    else:
        search_datetime = date
    
    x, y = aoi.exterior.coords.xy
    
    search_params = {
        "collections": hls_collections,
        "bbox": [min(x),min(y),max(x),max(y)], # list of xmin, ymin, xmax, ymax
        "datetime": search_datetime,
    }
    search_hls = api.search(**search_params)
    hls_collection = search_hls.get_all_items()
    d = list(hls_collection)
    
    return d

def asf_search(aoi: Polygon, date: datetime = None):
    """For searching sentinel1 data

    Args:
        aoi (Polygon): area of interest as shapely Polygon
        date (datetime, optional): leave as none if searching today, else enter time range as datetime tuple: datetime(YYYY,MM,DD). Defaults to None.

    Returns:
        results: search results from ASF
    """
    if date == None:
        today = date.today()
        start = str(today) + 'T00:00:00Z'
        end = str(today) + 'T23:59:59Z'
    else:
        start = f.datetime2asfsearch(date[0])
        end = f.datetime2asfsearch(date[1])

    wkt = aoi.wkt
    opts = {
        'platform': asf.PLATFORM.SENTINEL1,
        'processingLevel': [asf.PRODUCT_TYPE.SLC],
        'beamMode': [asf.BEAMMODE.IW],
        'start': start,
        'end': end
    }
    results = asf.geo_search(intersectsWith=wkt,**opts)
    
    return results

def get_sensor_cadence(dfs: List[gpd.GeoDataFrame]) -> gpd.GeoDataFrame:
    """Return dataframe with all sensor acquisitions and their timedeltas

    Args:
        dfs (List[gpd.GeoDataFrame]): list of geodataframes from asf or hls search

    Returns:
        gpd.GeoDataFrame: dataframe with all sensor acquisitions and their timedeltas
    """
    coverage_df = pd.concat(dfs)
    coverage_df.sort_values(by=['startTime'], inplace=True)
    coverage_df['cadence'] = coverage_df.startTime.diff()
    coverage_df.reset_index(drop=True,inplace=True)

    return coverage_df