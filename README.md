# Opera_coverage

Users can calculate spatial-temporal coverage of sensors used as input datasets for OPERA products. Outputs are formatted as a GeoPandas dataframes and can be plotted as a heatmap on a crs='EPSG:4326' world map.


# Installation

```
conda env update -f environment.yml
conda activate opera_coverage
python -m ipykernel install --user --name opera_coverage
```

# Usage

Please refer to notebooks/Basic Demo.ipynb for an example workflow.

## get_area_coverage function

This is the main function that queries the DAACs (ASF search and HLS search), gets rid of duplicate search results, then sorts and returns the results as a GeoPandas dataframe. An example function call is:

```
df = get_area_coverage(aoi, daterange, x_res = 1, y_res = 1, radius = 0.1)
```

where aoi is formatted as a shapely Polygon, daterange as a list of length 2 containing the start and end datetime, x_res and y_res are the resolution in latitude and longitude degrees as floats, and radius of search area per query as a float. More explicitly, the function call can be written as:

```
df = get_area_coverage(shapely.geometry.Polygon(([-119, 38],[-116,38],[-116, 40],[-119,40],[-119,38])), [datetime.datetime(2022,1,1), datetime.datetime(2022,2,1)], x_res = 1, y_res = 1, radius = 0.1)
```

## get_boxes function

This is the main function that takes the dataframe returned from get_area_coverage and returns a different GeoPandas dataframe that can be plotted with the GeoPandas built-in .plot() function to display the coverage as an array of 1 degree by 1 degree squares. An example function call is:

```
df_box = get_boxes(df)
```
where df is a GeoPandas dataframe from get_area_coverage.

## Plotting

To display the heatmap, one can specify <code>column='av_cad_days',legend=True,legend_kwds={'label': "Sensor cadence (# of days)"}</code> for the plot to include cadence as a colorbar. An example plot is shown below:

<img width="606" alt="Screen Shot 2022-09-22 at 9 03 51 AM" src="https://user-images.githubusercontent.com/48765984/191796715-20cbd3c4-2434-422e-8667-2fa964d51606.png">

# Known issues

/*:
  - Northern Russia coverage: since single look complex (SLC) is specified for ASF search in opera_coverage/search.py asf_search(), there is no coverage over northern Russia. Other result formats exist for that region.

*/

# Useful links

/*:
  - [ASF search](https://search.asf.alaska.edu/#/)
  - [GeoPandas documentation](https://geopandas.org/en/stable/docs/user_guide.html)

*/
