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

# Combining Residential & Commercial Demands for a City-Wide Model

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

### Call csv outputs from other notebooks

```python
resi_sa = pd.read_csv("data/interim/residential_small_area_demands.csv")
```

```python
resi_pcode = pd.read_csv("data/interim/residential_postcode_demands.csv")
```

```python
comm_sa = pd.read_csv("data/interim/commercial_sa_demands.csv")
```

```python
comm_pcode = pd.read_csv("data/interim/commercial_postcode_demands.csv")
```

```python
dc_sa = pd.read_csv("data/interim/data_centre_sa_demands.csv")
```

```python
dc_sa["small_area"] = dc_sa['small_area'].astype(str)
```

```python
dc_pcode = pd.read_csv("data/interim/data_centre_postcode_demands.csv")
```

```python
comm_pcode['postcode'] = comm_pcode['postcodes'].str.lower()
```

```python
total_sa = pd.merge(resi_sa, comm_sa, left_on="GEOGID", right_on="small_area", how="left", indicator=True)
```

```python
total_sa = pd.merge(total_sa, dc_sa, left_on="GEOGID", right_on="small_area", how="left")
```

```python
total_sa = total_sa.rename(columns={'geometry_x': 'geometry'})
```

```python
total_sa["sa_data_centre_elec_peak_kw"] = total_sa['sa_data_centre_elec_peak_kw'].fillna(0)
```

```python
total_sa['sa_elec_demand_kwh'] = total_sa['sa_elec_demand_kwh'].fillna(0)
```

```python
total_sa['sa_elec_demand_kw'] = total_sa['sa_elec_demand_kw'].fillna(0)
```

```python
total_sa['sa_energy_demand_kwh_y'] = total_sa['sa_energy_demand_kwh_y'].fillna(0)
```

```python
total_sa["sa_comm_elec_peak_kw"] = total_sa["sa_comm_elec_peak_kw"].fillna(0)
```

### Need to adopt for peak elec demands

```python
total_sa["total_sa_energy_demand(kWh)"] = total_sa["sa_energy_demand_kwh_x"] + total_sa["sa_energy_demand_kwh_y"] 
```

```python
total_sa["total_sa_elec_peak(kW)"] = total_sa["sa_peak_elec_demand(kW)"] + total_sa["sa_comm_elec_peak_kw"] + total_sa["sa_data_centre_elec_peak_kw"]
```

```python
total_sa["sa_peak_elec_demand(kW)"].sum()
```

```python
total_sa["sa_comm_elec_peak_kw"].sum()
```

```python
total_sa = total_sa[["GEOGID", "total_sa_energy_demand(kWh)", "total_sa_elec_peak(kW)", "geometry"]]
```

```python
total_sa = total_sa.iloc[:,0:5]
```

```python
total_sa['geometry'] = total_sa['geometry'].apply(wkt.loads)
```

```python
total_sa = gpd.GeoDataFrame(total_sa, geometry = total_sa.geometry)
```

```python
total_sa
```

```python
total_sa.to_file("data/outputs/sa_total_demands.geojson", driver="GeoJSON")
```

```python
total_pcode = pd.merge(resi_pcode, comm_pcode, on="postcode")
```

```python
total_pcode["total_postcode_elec_demand(kWh)"] = total_pcode["elec_per_postcode_kwh"] + total_pcode["cibse_postcode_elec_demand_kwh"]
```

### First converting kWh to kW, then to kVA assuming PF of 0.85

```python
total_pcode["total_peak_elec(kVA)"] = (total_pcode["total_postcode_elec_demand(kWh)"] / (8760))*0.85
```

```python
total_pcode["total_postcode_energy_demand(kWh)"] = total_pcode["energy_per_postcode_kwh"] + total_pcode["postcode_energy_demand_kwh"]
```

```python
total_pcode = total_pcode[["postcode", "total_postcode_energy_demand(kWh)", "total_postcode_elec_demand(kWh)", "total_peak_elec(kVA)", "geometry_x"]]
```

```python
total_pcode['geometry'] = total_pcode['geometry_x'].apply(wkt.loads)
```

```python
total_pcode = gpd.GeoDataFrame(total_pcode, geometry = total_pcode.geometry)
```

```python
total_sa.plot(figsize=(10, 10), column="total_sa_elec_peak(kW)", legend=True, cmap="cividis", legend_kwds={'label': "Electricity Demands Peaks by Small Area (kW)"},)
```

```python
total_sa.plot(column="total_sa_energy_demand(kWh)",figsize=(10, 10), legend=True, cmap="cividis", legend_kwds={'label': "Total Energy Demand by Small_Area (kWh)"})
```

```python
total_pcode.plot(column="total_postcode_energy_demand(kWh)",legend=True, legend_kwds={'label': "Total Energy Demand by Postcode (kWh)"})
```

```python
total_pcode.plot(column="total_peak_elec(kVA)",legend=True, legend_kwds={'label': "Total Peak Elec Demand by Postcode (kVA)"})
```

```python

```

### Calculating totals

```python
resi_pcode["elec_per_postcode_kwh"].sum()
```

```python

```
