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

# Calculate Dublin total emissions by sector

```python
cd ..
```

```python
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
```

```python
cso = pd.read_csv("data/roughwork/cso_heating_type.csv")
```

```python
df_demands = pd.read_csv("data/outputs/total_demands_sa.csv")
```

```python
cso_dub = pd.merge(df_demands, cso, left_on="GEOGID", right_on="SMALL_AREA", how="inner")
```

```python
df_demands["sa_energy_demand_resi_kwh"].sum()
```

```python
df_demands["sa_energy_demand_comm_kwh"].sum()
```

```python
df_em = df_demands[["GEOGID", "sa_annual_elec_demand_resi_kwh", "sa_heat_demand_resi_kwh", "sa_elec_demand_comm_kwh", "sa_ff_demand_kwh", "sa_elec_demand_dc_kwh", "geometry"]]
```

```python
df_em["sa_resi_elec_emissions_TCO2"] = (df_em["sa_annual_elec_demand_resi_kwh"]*324.5)*1e-6
```

```python
df_em["sa_resi_elec_emissions_TCO2"].sum()
```

```python
df_em["sa_resi_heat_emissions_TCO2"] = (df_em["sa_heat_demand_resi_kwh"]*cso_dub["sa_emissions_gCO2/kwh"])*1e-6
```

```python
df_em["sa_resi_heat_emissions_TCO2"].sum()
```

```python
df_em["sa_comm_elec_emissions_TCO2"] = (df_em["sa_elec_demand_comm_kwh"]*324.5)*1e-6
```

```python
df_em["sa_comm_elec_emissions_TCO2"].sum()
```

```python
df_em["sa_comm_heat_emissions_TCO2"] = (df_em["sa_ff_demand_kwh"]*251.9)*1e-6
```

```python
df_em["sa_comm_heat_emissions_TCO2"].sum()
```

```python
df_em["sa_data_centre_elec_emissions_TCO2"] = (df_em["sa_elec_demand_dc_kwh"]*324.5)*1e-6
```

```python
df_em["total_sa_emissions_TCO2"] = df_em["sa_resi_elec_emissions_TCO2"] + df_em["sa_resi_heat_emissions_TCO2"] + df_em["sa_comm_elec_emissions_TCO2"] + df_em["sa_comm_heat_emissions_TCO2"] + df_em["sa_data_centre_elec_emissions_TCO2"]
```

```python
df_em["total_sa_resi_emissions_TCO2"] = df_em["sa_resi_elec_emissions_TCO2"] + df_em["sa_resi_heat_emissions_TCO2"]
```

```python
df_em["total_sa_resi_emissions_TCO2"].sum()
```

```python
df_em["total_sa_comm_emissions_TCO2"] = df_em["sa_comm_elec_emissions_TCO2"] + df_em["sa_comm_heat_emissions_TCO2"]
```

```python
df_em["total_sa_comm_emissions_TCO2"].sum()
```

```python
df_em["total_no_data_centre_TCO2"] = df_em["total_sa_emissions_TCO2"] - df_em["sa_data_centre_elec_emissions_TCO2"]
```

```python
emissions = gpd.GeoDataFrame(df_em)
```

```python
emissions['geometry'] = emissions['geometry'].apply(wkt.loads)
```

```python
emissions["centroids"] = emissions.geometry.centroid
```

```python
emissions_centroid = emissions.rename(columns={"centroids": "geometry_x"})
```

```python
emissions_centroid.columns
```

```python
emissions_centroid = emissions_centroid[['GEOGID', 'sa_annual_elec_demand_resi_kwh', 'sa_heat_demand_resi_kwh', 'sa_elec_demand_comm_kwh', 'sa_ff_demand_kwh', 'sa_elec_demand_dc_kwh', 'sa_resi_elec_emissions_TCO2','sa_resi_heat_emissions_TCO2', 'sa_comm_elec_emissions_TCO2', 'sa_comm_heat_emissions_TCO2', 'sa_data_centre_elec_emissions_TCO2', 'total_sa_emissions_TCO2', 'total_sa_resi_emissions_TCO2', 'total_sa_comm_emissions_TCO2', 'total_no_data_centre_TCO2', 'geometry_x']]


```
```python
emissions_centroid = emissions.rename(columns={"geometry_x": "geometry"})
```

```python
df_em = emissions_centroid.set_crs(epsg="4326")
```

```python
bound = gpd.read_file("data/roughwork/dublin_admin/Census2011_Admin_Counties_generalised20m.shp")
```

```python
bound = bound.to_crs(epsg="4326")
```

```python
dublin_em = gpd.sjoin(df_em, bound, op="intersects")
```

```python
dublin_em = dublin_em[['GEOGID_left', 'COUNTYNAME', 'sa_annual_elec_demand_resi_kwh',
       'sa_heat_demand_resi_kwh', 'sa_elec_demand_comm_kwh',
       'sa_ff_demand_kwh', 'sa_elec_demand_dc_kwh',
       'sa_resi_elec_emissions_TCO2', 'sa_resi_heat_emissions_TCO2',
       'sa_comm_elec_emissions_TCO2', 'sa_comm_heat_emissions_TCO2',
       'sa_data_centre_elec_emissions_TCO2', 'total_sa_emissions_TCO2',
       'total_sa_resi_emissions_TCO2', 'total_sa_comm_emissions_TCO2', 'total_no_data_centre_TCO2','geometry']]
```

```python
dublin_em = gpd.GeoDataFrame(dublin_em)
```

```python
dublin_em = dublin_em.drop_duplicates(subset="GEOGID_left")
```

```python
dublin_em.to_file("data/outputs/dublin_sa_emissions_decarbzone.geojson", driver='GeoJSON')
```

```python
dublin_em.plot(figsize=(10, 10), column="total_sa_emissions_TCO2", legend=True, legend_kwds={'label': "Total Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
dublin_em.plot(figsize=(10, 10), column="total_sa_resi_emissions_TCO2", legend=True, legend_kwds={'label': "Total Annual Residential Carbon Emissions by Small Area (tCO2)"},)
```

```python
dublin_em.plot(figsize=(10, 10), column="total_sa_comm_emissions_TCO2", legend=True, legend_kwds={'label': "Total Annual Commercial Carbon Emissions by Small Area (tCO2)"},)
```

```python
dublin_em.plot(figsize=(10, 10), column="sa_data_centre_elec_emissions_TCO2", legend=True, legend_kwds={'label': "Total Data Centre Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
dublin_em.plot(figsize=(10, 10), column="total_no_data_centre_TCO2", legend=True, legend_kwds={'label': "Total w/out DC's Annual Carbon Emissions by Small Area (tCO2)"},)
dublin_em
```

```python
dublin_em.to_csv("data/outputs/total_sa_outputs.csv")
```

```python
dublin_em.to_excel("data/outputs/total_sa_outputs.xlsx")
```

dublin_em.to_file("data/outputs/dublin_sa_emissions.geojson", driver='GeoJSON')


## LA Analysis

```python
dublin_em["COUNTYNAME"].value_counts()
```

```python
sdcc_em = dublin_em[dublin_em["COUNTYNAME"].str.contains("Dún Laoghaire-Rathdown")]
sdcc_em = dublin_em[dublin_em["COUNTYNAME"].str.contains("South Dublin")]
```

```python
sdcc_em
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_resi_emissions_TCO2", legend=True, legend_kwds={'label': "Total Residential DLR Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_comm_emissions_TCO2", legend=True, legend_kwds={'label': "Total Commercial DLR Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_emissions_TCO2", legend=True, legend_kwds={'label': "Total DLR Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="sa_data_centre_elec_emissions_TCO2", legend=True, legend_kwds={'label': "Total Data Centre DLR Annual Carbon Emissions by Small Area (tCO2)"},)
=======
sdcc_em.plot(figsize=(10, 10), column="total_sa_resi_emissions_TCO2", legend=True, legend_kwds={'label': "Total Residential SDCC Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_comm_emissions_TCO2", legend=True, legend_kwds={'label': "Total Commercial SDCC Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_emissions_TCO2", legend=True, legend_kwds={'label': "Total SDCC Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python
sdcc_em.plot(figsize=(10, 10), column="sa_data_centre_elec_emissions_TCO2", legend=True, legend_kwds={'label': "Total Data Centre SDCC Annual Carbon Emissions by Small Area (tCO2)"},)
```

```python

```
