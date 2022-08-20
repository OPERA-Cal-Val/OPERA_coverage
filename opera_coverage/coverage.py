from typing import List
from shapely.geometry import Polygon
from datetime import datetime
import numpy as np
import geopandas as gpd
from . import formatting as f
from . import search as s

def get_coverage(sensor: List[str], aoi: Polygon, date: List[datetime] = None) -> gpd.GeoDataFrame:
    """Main function, returns a dataframe with search results from asf_search and hls_search

    Args:
        sensor (List[str]): choose sentinel1, sentinel2, landsat8
        aoi (Polygon): enter coordinates as Polygon object
        date (List[datetime], optional): leave as none if searching today, else enter time range as datetime tuple: datetime(YYYY,MM,DD). Defaults to None.

    Returns:
        coverage_df: gpd.GeoDataFrame with columns including sensor name, acquisition time, geometry, fileID, and timedelta between each acquisition
    """
    dataframes = []
    
    for sensor_name in sensor:
        
        if 'landsat8' in sensor_name.lower():
            results = s.hls_search('landsat8', aoi, date)
            df = f.format_results_for_hls(results,'landsat8')
        elif 'sentinel1' in sensor_name.lower():
            results = s.asf_search(aoi, date)
            df = f.format_results_for_sent1(results)
        elif 'sentinel2' in sensor_name.lower():
            results = s.hls_search('sentinel2', aoi, date)
            df = f.format_results_for_hls(results,'sentinel2')
        
        dataframes.append(df)

    coverage_df = s.get_sensor_cadence(dataframes)
    return coverage_df