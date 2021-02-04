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

```python
df = pd.concat(map(pd.read_csv, glob.glob('data/commercial/*.csv')))
```

```python
df['Area'] = df['Area'].fillna(0)
```

### Define area limits to remove outliers

```python
df_area = df[(df['Area'] > 5) & (df['Area'] <= 50000 )]
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
df_final["Uses_Clean"] = df_final['Uses'].str.replace(r', -', '')
```

### Extracting just data centres

```python
df_final = df_final.loc[df_final["Uses"] == "DATA CENTRE, -"]
```

```python
df_final
```

```python
missing = pd.read_csv("data/commercial/data_centres_missing_vo.csv")
```

```python
missing
```

```python
full_dc = pd.merge(df_final, missing, how="outer")
```

```python
full_dc
```

### Cibse benchmarks provide references values per floor area

```python
benchmarks = pd.read_csv("data/commercial/benchmark_use_links_usa.csv")
```

```python
bench_linked = pd.merge(df_final, benchmarks, left_on="Uses_Clean", right_on="Uses")
```

```python
bench_linked = bench_linked.reset_index(drop=True)
```

```python
bench_linked["ff_demand_kwh"] = bench_linked["property_total_area_y"] * bench_linked["typical_fossil_fuel_y"]
```

```python
bench_linked["elec_demand_kwh"] = bench_linked["property_total_area_y"] * bench_linked["typical_electricity_y"]
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
bench_linked
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
elec_sa["data_centre_peak_kw"] = (elec_sa["elec_demand_kwh"] / 8760) / elec_sa["alf_y"]
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
sa_demand_elec = elec_sa.groupby("small_area")["elec_demand_kwh"].sum().rename("sa_data_centre_elec_demand_kwh").reset_index()
```

```python
sa_demand_ff = elec_sa.groupby("small_area")["ff_demand_kwh"].sum().rename("sa_data_centre_ff_demand_kwh").reset_index()
```

### Peak elec values coming from ALF category computed from SME profiles & USA report

```python
sa_peak_elec = elec_sa.groupby("small_area")["data_centre_peak_kw"].sum().rename("sa_data_centre_elec_peak_kw").reset_index()
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
sa_demand_total["sa_dc_energy_demand_kwh"] = sa_demand_total["sa_data_centre_ff_demand_kwh"] + sa_demand_total["sa_data_centre_elec_demand_kwh"]
```

### Values in kWh are annual so divisible by 8760 to relate to kW

```python
sa_demand_total["sa_dc_elec_demand_kw"] = sa_demand_total["sa_data_centre_elec_demand_kwh"] / 8760
```

```python
sa_demand_final = sa_demand_total[["small_area", "sa_dc_energy_demand_kwh", "sa_data_centre_elec_demand_kwh", "sa_dc_elec_demand_kw", "sa_data_centre_elec_peak_kw", "geometry_x"]]
```

```python
sa_demand_final = gpd.GeoDataFrame(sa_demand_final, geometry="geometry_x")
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
pcode_demand_final.plot(column="postcode_energy_demand_kwh", legend=True, legend_kwds={'label': "Data Centre Energy Demand by Postcode (kWh)"})
```

```python
pcode_demand_final.plot(column="cibse_postcode_elec_demand_kwh", legend=True, legend_kwds={'label': "Data Centre Elec Demand by Postcode (kWh)"})
```

```python
pcode_demand_final.to_csv("data/interim/data_centre_postcode_demands.csv")
```

```python
sa_demand_final.plot(column="sa_dc_energy_demand_kwh", legend=True, legend_kwds={'label': "Data Centre Energy Demand by Small Area (kWh)"})
```

```python
sa_demand_final.plot(column="sa_data_centre_elec_demand_kwh", legend=True, legend_kwds={'label': "Data Centre Elec Demand by Small Area (kWh)"})
```

```python
sa_demand_final.to_csv("data/interim/data_centre_sa_demands.csv")
```

```python
sa_demand_final
```

### Checking all DC's accounted for

```python
test = df.loc[df["Uses"] == "DATA CENTRE, -"]
```

```python
test["Property Number"].nunique()
```

```python
test.columns
```

```python
elec_sa
```

```python
test_full = test[["Property Number", "Uses", "Address 2", "Area", " X ITM", " Y ITM"]]
```

```python
print(test_full.to_string())
```

```python
bench_linked
```

```python
test.loc[test["Area"] == 0]
```
