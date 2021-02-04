---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.9.1
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
```

### Read in data centre load information from Bitpower

```python
dc = pd.read_csv("data/commercial/bitpower_data_centres.csv")
```

```python
dc_built = dc.loc[dc["Stage of Development"] == "5 - Built"]
```

```python
dc_geom = gpd.GeoDataFrame(dc_built, geometry=gpd.points_from_xy(dc_built.Longitude, dc_built.Latitude))
```

```python
dc_geom["data_centre_peak_kw"] = (dc_geom["Annual Electrical Consumption (kWh)"] / 8760) / dc_geom["alf"]
```

```python
dc_geom = dc_geom.set_crs(epsg="4326")
```

### Annual Electrical Consumption is rated at 42.5% Utilisation of Capacity

```python
postcode = gpd.read_parquet("data/spatial/dublin_postcodes.parquet")
```

```python
small_areas = gpd.read_parquet("data/spatial/small_area_geometries_2016.parquet")
```

```python
dc_pcode = gpd.sjoin(dc_geom, postcode, op="within")
```

```python
dc_sa = gpd.sjoin(dc_geom, small_areas, op="within")
```

```python
pcode_demand_dc = dc_pcode.groupby("postcodes")["Annual Electrical Consumption (kWh)"].sum().rename("postcode_elec_demand_dc_kwh").reset_index()
```

```python
pcode_demand_dc = pd.merge(pcode_demand_dc, postcode, on="postcodes")
```

```python
pcode_demand_dc  = gpd.GeoDataFrame(pcode_demand_dc)
```

```python
sa_demand_dc = dc_sa.groupby("small_area")["Annual Electrical Consumption (kWh)"].sum().rename("sa_elec_demand_dc_kwh").reset_index()
```

```python
sa_demand_dc = pd.merge(sa_demand_dc, small_areas, on="small_area")
```

```python
sa_demand_dc = gpd.GeoDataFrame(sa_demand_dc)
```

### Peak elec values coming from ALF category computed from SME profiles & USA report

```python
pcode_peak_dc = dc_pcode.groupby("postcodes")["data_centre_peak_kw"].sum().rename("postcode_data_centre_elec_peak_kw").reset_index()
```

```python
pcode_demand_dc = pd.merge(pcode_demand_dc, pcode_peak_dc, on="postcodes")
```

```python
pcode_demand_dc
```

```python
sa_peak_dc = dc_sa.groupby("small_area")["data_centre_peak_kw"].sum().rename("sa_data_centre_elec_peak_kw").reset_index()
```

```python
sa_demand_dc = pd.merge(sa_demand_dc, sa_peak_dc, on="small_area")
```

```python
sa_demand_dc
```

```python
pcode_demand_dc.plot(column="postcode_elec_demand_dc_kwh", legend=True, legend_kwds={'label': "Annual Data Centre Elec Demand by Postcode (kWh)"})
```

```python
pcode_demand_dc.to_csv("data/interim/data_centre_postcode_demands.csv")
```

```python
sa_demand_dc.plot(column="sa_elec_demand_dc_kwh", legend=True, legend_kwds={'label': "Annual Data Centre Elec Demand by Small Area (kWh)"})
```

```python
sa_demand_dc.to_csv("data/interim/data_centre_sa_demands.csv")
```
