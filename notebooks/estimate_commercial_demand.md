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

# Commercial Modelling for Dublin using the VO Dataset

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

```python
df = pd.concat(map(pd.read_csv, glob.glob('data/commercial/vo/*.csv')))
```

```python
df['Area'] = df['Area'].fillna(0)
```

```python
df_area = df[(df['Area'] > 5) & (df['Area'] <= 50000 )]
```

### Need to define area limits to correct for VO input errors

```python
df_outliers = df[(df['Area'] < 5) | (df['Area'] >= 50000 )]
```

```python
df_outliers = df_outliers.drop_duplicates(subset="Property Number")
```

```python
mean_category_area = df_area.groupby("Uses")["Area"].mean().rename("property_total_area").to_frame().reset_index()
```

```python
df_outliers = pd.merge(df_outliers, mean_category_area, on="Uses")
```

```python
df_ext = df_area.drop_duplicates(subset=['Property Number', 'Area'])
```

```python
df_out = df_ext.groupby(by="Property Number", as_index=True)["Area"].sum().rename("property_total_area").to_frame().reset_index()
```

```python
df_merge = pd.merge(df, df_out, on="Property Number")
```

```python
df_final = df_merge.drop_duplicates(subset=['Property Number'])
```

```python
df_final = pd.concat([df_final, df_outliers])
```

```python
df_final["Uses_Clean"] = df_final['Uses'].str.replace(r', -', '')
```

### Remove Data Centres

```python
df_final = df_final.loc[df_final["Uses"] != "DATA CENTRE, -"]
```

### Cibse benchmarks provide references values per floor area

```python
benchmarks = pd.read_csv("data/commercial/benchmark_use_links_usa.csv")
```

```python
bench_linked = pd.merge(df_final, benchmarks, left_on="Uses_Clean", right_on="Uses")
```

```python
bench_linked["ff_demand_kwh"] = bench_linked["property_total_area"] * bench_linked["typical_fossil_fuel"]
```

```python
bench_linked["elec_demand_kwh"] = bench_linked["property_total_area"] * bench_linked["typical_electricity"]
```

```python
bench_linked = gpd.GeoDataFrame(bench_linked, geometry=gpd.points_from_xy(bench_linked[" X ITM"], bench_linked[" Y ITM"]))
```

```python
bench_linked = bench_linked.set_crs(epsg = "2157")
```

```python
bench_linked = bench_linked.to_crs(epsg = "4326")
```

```python
postcode = gpd.read_parquet("data/spatial/dublin_postcodes.parquet")
```

```python
small_areas = gpd.read_parquet("data/spatial/small_area_geometries_2016.parquet")
```

```python
elec_pcode = gpd.sjoin(bench_linked, postcode, op="within")
```

```python
elec_sa = gpd.sjoin(bench_linked, small_areas, op="within")
```

```python
elec_sa["comm_peak_kw"] = (elec_sa["elec_demand_kwh"] / 8760) / elec_sa["alf"]
```

```python
elec_sa["elec_demand_kwh"].sum()
```

```python
largest_consumer = elec_sa["elec_demand_kwh"].sort_values()
```

```python
pcode_demand_elec = elec_pcode.groupby("postcodes")["elec_demand_kwh"].sum().rename("cibse_postcode_elec_demand_kwh").reset_index()
```

```python
pcode_demand_ff = elec_pcode.groupby("postcodes")["ff_demand_kwh"].sum().rename("postcode_ff_demand_kwh").reset_index()
```

```python
pcode_demand_elec = pd.merge(pcode_demand_elec, postcode, on="postcodes")
```

```python
pcode_demand_elec = gpd.GeoDataFrame(pcode_demand_elec)
```

```python
pcode_demand_ff = pd.merge(pcode_demand_ff, postcode, on="postcodes")
```

```python
pcode_demand_ff = gpd.GeoDataFrame(pcode_demand_ff)
```

```python
sa_demand_elec = elec_sa.groupby("small_area")["elec_demand_kwh"].sum().rename("sa_elec_demand_kwh").reset_index()
```

```python
sa_demand_ff = elec_sa.groupby("small_area")["ff_demand_kwh"].sum().rename("sa_ff_demand_kwh").reset_index()
```

### Peak elec values coming from ALF category computed from SME profiles & USA report

```python
sa_peak_elec = elec_sa.groupby("small_area")["comm_peak_kw"].sum().rename("sa_comm_elec_peak_kw").reset_index()
```

```python
sa_demand_elec = pd.merge(sa_demand_elec, small_areas, on="small_area")
```

```python
sa_demand_elec = gpd.GeoDataFrame(sa_demand_elec)
```

```python
sa_demand_elec = pd.merge(sa_demand_elec, sa_peak_elec, on="small_area")
```

```python
sa_demand_ff = pd.merge(sa_demand_ff, small_areas, on="small_area")
```

```python
sa_demand_ff = gpd.GeoDataFrame(sa_demand_ff)
```

```python
sa_demand_total = pd.merge(sa_demand_ff, sa_demand_elec, on="small_area")
```

### Cibse Energy is the sum of the Elec & FF values

```python
sa_demand_total["sa_energy_demand_kwh"] = sa_demand_total["sa_ff_demand_kwh"] + sa_demand_total["sa_elec_demand_kwh"]
```

### Values in kWh are annual so divisible by 8760 to relate to kW

```python
sa_demand_total["sa_elec_demand_kw"] = sa_demand_total["sa_elec_demand_kwh"] / 8760
```

```python
sa_demand_total
```

```python
sa_demand_final = sa_demand_total[["small_area", "sa_energy_demand_kwh", "sa_elec_demand_kwh", "sa_elec_demand_kw", "sa_comm_elec_peak_kw", "geometry_x"]]
```

```python
sa_demand_final = gpd.GeoDataFrame(sa_demand_final, geometry="geometry_x")
```

```python
sa_demand_final
```

```python
pcode_demand_total = pd.merge(pcode_demand_ff, pcode_demand_elec, on="postcodes")
```

```python
pcode_demand_total["postcode_energy_demand_kwh"] = pcode_demand_total["postcode_ff_demand_kwh"] + pcode_demand_total["cibse_postcode_elec_demand_kwh"]
```

```python
pcode_demand_final = pcode_demand_total[["postcodes", "postcode_energy_demand_kwh", "cibse_postcode_elec_demand_kwh", "geometry_x"]]
```

```python
pcode_demand_final = gpd.GeoDataFrame(pcode_demand_final, geometry="geometry_x")
```

```python
pcode_demand_final.plot(column="postcode_energy_demand_kwh", figsize=(10, 10), legend=True, legend_kwds={'label': "Commercial Annual Energy Demand by Postcode (kWh)"})
```

```python
pcode_demand_final.plot(column="cibse_postcode_elec_demand_kwh", legend=True, legend_kwds={'label': "Commercial Elec Demand by Postcode (kWh)"})
```

```python
pcode_demand_final.to_csv("data/interim/commercial_postcode_demands.csv")
```

```python
sa_demand_final.plot(figsize=(10, 10), column="sa_energy_demand_kwh", legend=True, legend_kwds={'label': "Commercial Annual Energy Demand by Small Area (kWh)"})
```

```python
sa_demand_final.plot(figsize=(10, 10), column="sa_elec_demand_kwh", legend=True, legend_kwds={'label': "Commercial Elec Demand by Small Area (kWh)"})
```

```python
sa_demand_final.plot(figsize=(10, 10), column="sa_comm_elec_peak_kw", legend=True, legend_kwds={'label': "Commercial Peak Elec Demand by Small Area (kW)"})
```

```python
sa_demand_final.to_csv("data/interim/commercial_sa_demands.csv")
```

## Calculating Peak Demands from SME Profiles

```python
import matplotlib.pyplot as plt
import datetime as dt
```

```python
comm_peak = pd.read_csv("data/roughwork/cer_smart_meter/other-transportation-and-storage.csv")
```

```python
comm_peak = pd.DataFrame(comm_peak)
```

```python
comm_peak["datetime"] = pd.to_datetime(comm_peak['datetime'])
```

```python
comm_2010 = comm_peak[(comm_peak["datetime"].dt.year == 2010)]
```

```python
comm_hourly = comm_2010.iloc[::2, :].reset_index()
```

```python
comm_hourly
```

```python
plt.plot_date(comm_hourly["datetime"].loc[100:300], comm_hourly["demand"].loc[100:300], linestyle='--', marker='o', color='b')
```

```python
comm_demand = comm_hourly["demand"].sum()
```

```python
comm_peak = comm_hourly["demand"].max()
```

```python
comm_alf = ((comm_demand/8760)/comm_peak)
```

```python
comm_alf
```

### Wrangling the VO dataset

```python
df_zero_area = df_final.loc[df_final["Area"] == 0]
```

```python
df_zero_area["Uses"].value_counts()
```

```python
df[df["Category"].str.contains("HOSPITALITY", na=False)]
```

```python
df_test = df_final[(df_final['Uses'].str.contains("HOTEL")) & (df_final['property_total_area'] <= 10000 )]
```

```python
df_final["Floor Use"].value_counts()
```

```python
largest_props = df_final["property_total_area"].sort_values()
```

```python
use_group = df_final.groupby("Uses")["property_total_area"].sum().sort_values()
```

```python
print(largest_props.to_string())
```

```python
df_final.loc[72632]
```

```python
df_final.loc[df_final["Uses"] == "APART / HOTEL, -"]
```

```python
df.loc[df["Property Number"] == 447026.0]
```

```python
print(largest_consumer.to_string())
```

```python
elec_sa.loc[23224]
```

```python
consumer_groups = elec_sa.groupby("Uses_Clean")["elec_demand_kwh"].sum().sort_values()
```

```python
print(consumer_groups.to_string())
```

```python
elec_sa["comm_peak_kw"].sort_values()
```

```python
elec_sa.iloc[23246]
```

```python
elec_sa.loc[elec_sa["small_area"] == "267044009"]
```
