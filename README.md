# Opera_coverage

Users can calculate spatial-temporal coverage of sensors used as input datasets for OPERA products. Outputs are formatted as a GeoPandas dataframes and can be plotted as a heatmap on a crs='EPSG:4326' world map.


# Installation

```
git clone https://github.com/angelviolinist/opera_coverage.git
conda env update -f environment.yml
conda activate opera_coverage
python -m ipykernel install --user --name opera_coverage
pip install .
```

# Usage

Please refer to notebooks/Demo.ipynb for example.

## get_coverage

This function queries the DAACs (ASF search and HLS search) for the user-specified sensors, processes duplicate search results appropriately, then sorts and returns the results as a GeoPandas dataframe. An example function call is:

```
df = get_coverage(sensor_list, aoi, daterange)
```
where sensor_list is a list with any number of sensors from ['sentinel1','sentinel2','landsat8_9'], aoi is formatted as a shapely Polygon, and daterange is a list of length 2 containing the start and end datetime. An example output dataframe is shown below:

<img width="982" alt="Screen Shot 2022-10-06 at 9 04 38 AM" src="https://user-images.githubusercontent.com/48765984/194362964-3b1de065-7250-43db-9071-39c01f7e79cc.png">

Please refer to notebooks/Basic Demo.ipynb for an example workflow of the below two functions.

<!-- ## get_area_coverage

This function is used when the user intends to run multiple searches over a broad area of interest. It queries the DAACs (ASF search and HLS search) for all available sensors in this package, processes duplicate search results appropriately, then sorts and returns the results as a GeoPandas dataframe. An example function call is:

```
df = get_area_coverage(aoi, daterange, x_res = 1, y_res = 1, radius = 0.1)
```

where aoi is formatted as a shapely Polygon, daterange as a list of length 2 containing the start and end datetime, x_res and y_res are the resolution in latitude and longitude degrees as floats, and radius of search area per query as a float. More explicitly, the function call can be written as:

```
df = get_area_coverage(shapely.geometry.Polygon(([-119, 38],[-116,38],[-116, 40],[-119,40],[-119,38])), [datetime.datetime(2022,1,1), datetime.datetime(2022,2,1)], x_res = 1, y_res = 1, radius = 0.1)
```

## get_boxes

This is the main function that takes the dataframe returned from get_area_coverage and returns a different GeoPandas dataframe that can be plotted with the GeoPandas built-in .plot() function to display the coverage as an array of 1 degree by 1 degree squares. An example function call is:

```
df_box = get_boxes(df)
```
where df is a GeoPandas dataframe from get_area_coverage.

## separate_sensors

After running get_boxes, results from specific sensors can be filtered out by calling this function:
```
df = separate_sensors(all_sensors_df, sensor_list)
```
where all_sensors_df is the GeoDataFrame with all sensor acquisitions, sensor_list is the list of sensors the user wants results for, and df is the GeoDataFrame output with only acquisitions from those sensors. -->

## Plotting

To display the heatmap, one can specify <code>column='av_cad_days',legend=True,legend_kwds={'label': "Sensor cadence (# of days)"}</code> for the plot to include cadence as a colorbar. An example plot is shown below:

<img width="606" alt="Screen Shot 2022-09-22 at 9 03 51 AM" src="https://user-images.githubusercontent.com/48765984/191796715-20cbd3c4-2434-422e-8667-2fa964d51606.png">

# Known issues

  - Northern Russia coverage: since single look complex (SLC) is specified for ASF search in opera_coverage/search.py asf_search(), there is no coverage over northern Russia. Other result formats exist for that region.
  - Random boxes get no data when querying a broad area of interest. The boxes without data differ every time.

# Useful links

  - [ASF search](https://search.asf.alaska.edu/#/)
  - [GeoPandas documentation](https://geopandas.org/en/stable/docs/user_guide.html)
