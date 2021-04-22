---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
cd ..
```

```python
import pandas as pd
import geopandas as gpd
import glob
from pathlib import Path
import numpy as np
import pygeos
import rtree
import matplotlib.pyplot as plt
import pandas_bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.plotting import gmap
from shapely.geometry import Point
from bokeh.models import ColumnDataSource
import fiona
```

```python
pd.set_option('plotting.backend', 'pandas_bokeh')
```

```python
pandas_bokeh.output_notebook()
```

# Change This

```python
gdf = gpd.read_file("data/spatial/usspv/USSPV-10.shp")
```

```python
waste_poly = gpd.read_file("data/spatial/waste_heat/waste_heat_polys_090421.geojson")
```

```python
waste_poly = waste_poly.to_crs(epsg="29902")
```

```python
waste_poly.plot()
```

```python
waste_point = gpd.read_file("data/roughwork/heat_source_points130421.geojson")
```

```python
waste_point.plot()
```

```python
waste = pd.concat([waste_point, waste_poly], ignore_index=True)
```

```python
pd.set_option('display.max_columns', 500)
```

### Waste Heat Sources

```python
from shapely.geometry import Point
from shapely.geometry import MultiPolygon
```

```python
mask = waste["geometry"].apply(lambda x: isinstance(x, Point))
```

```python
waste["heat_source"].value_counts()
```

```python
waste["kW"] = waste["kW"].fillna(0)
```

```python
waste["kW"] = waste["kW"].str.strip()
```

```python
waste["kW"] = pd.to_numeric(waste["kW"], errors='coerce')
```

```python
waste["kW"] = waste["kW"].fillna(0)
```

```python
waste = waste.sort_values(by =['kW'])
```

```python
waste["size"] = pd.qcut(waste['kW'], q = 8, labels = False, duplicates='drop')
```

```python
waste["size"] = waste["size"]*2
```

```python
chp = waste.query("heat_source=='chp'")
```

```python
data_centre = waste.query("heat_source=='data_centre'")
```

```python
industrial = waste.query("heat_source=='industrial'")
```

```python
electricity_transformers = waste.query("heat_source=='electricity_transformers'")
```

```python
rivers_dublin_basin = waste.query("heat_source=='rivers_dublin_basin'")
```

```python
surface_water = waste.query("heat_source=='surface_water'")
```

```python
biomass = waste.query("heat_source=='biomass'")
```

```python
wwtw = waste.query("heat_source=='wwtw'")
```

```python
cold_storage = waste.query("heat_source=='cold_storage'")
```

```python
power_stations = waste.query("heat_source=='power_stations'")
```

```python
waste_point = waste[mask].copy()
```

```python
waste_poly = waste[~mask].copy()
```

```python
mask_geom = waste_poly["geometry"].apply(lambda x: isinstance(x, MultiPolygon))
```

```python
waste_poly = waste_poly[mask_geom].copy()
```

```python
waste_poly
```

```python
dlr_sea_water = waste_poly.query("layer=='DLR_Sea_Water_Heat_Source_Area'")
```

```python
deep_geothermal = waste_poly.query("layer=='Are_of_Deep_Geothermal_Potential'")
```

```python
sea_water = waste_poly.query("layer=='Sea_Water_Heat_Source_Area'")
```

```python
hovertool_string_poly=("""
<table>
    <tr>
        <th>Heat Source</th>
        <td>@layer</td>
    </tr>
</table>""")
```

```python
pandas_bokeh.output_file("data/roughwork/heat_sources/waste_heat_poly_130421.html")
```

```python
figure = dlr_sea_water.plot_bokeh(hovertool_string=hovertool_string_poly, legend="dlr_sea_water", color="#e41a1c")
deep_geothermal.plot_bokeh(figure=figure, hovertool_string=hovertool_string_poly, legend="deep_geothermal", color="#377eb8", fill_alpha=0.1)
sea_water.plot_bokeh(figure=figure, hovertool_string=hovertool_string_poly, legend="sea_water", color="#4daf4a")
```

```python
pandas_bokeh.output_notebook()
```

```python
hovertool_string_point=("""
<table>
    <tr>
        <th>Heat Source</th>
        <td>@heat_source</td>
    </tr>
    <tr>
        <th>kW</th>
        <td>@kW</td>
    </tr>
</table>""")
```

```python
pandas_bokeh.output_file("data/roughwork/heat_sources/waste_heat_sources_130421.html")
```

```python
figure = chp.plot_bokeh(hovertool_string=hovertool_string_point, title="Dublin Waste Heat Sources", figsize=(900, 600), size="size", legend="chp", xlim=[-6.5, -6], ylim=[53.2, 53.6], marker="circle", color="#a6cee3")
data_centre.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="data_centre", marker="inverted_triangle", color="#1f78b4")
industrial.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="industrial", marker="triangle", color="#b2df8a")
electricity_transformers.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="electricity_transformers", marker="asterisk", color="#33a02c")
rivers_dublin_basin.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="rivers_dublin_basin", marker="circle_x", color="#fb9a99")
surface_water.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="surface_water", marker="square_x", color="#e31a1c")
biomass.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="biomass", marker="x", color="#fdbf6f")
wwtw.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="wwtw", marker="circle_cross", color="#ff7f00")
cold_storage.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="cold_storage", marker="square_cross", color="#cab2d6")
power_stations.plot_bokeh(figure=figure, hovertool_string=hovertool_string_point, size="size", legend="power_stations", marker="diamond", color="#6a3d9a")
dlr_sea_water.plot_bokeh(figure=figure, hovertool_string=hovertool_string_poly, legend="sea_water", color="#4daf4a")
deep_geothermal.plot_bokeh(figure=figure, hovertool_string=hovertool_string_poly, legend="deep_geothermal", color="#377eb8", fill_alpha=0.1)
sea_water.plot_bokeh(figure=figure, hovertool_string=hovertool_string_poly, legend="sea_water", color="#4daf4a")
```

```python

```
