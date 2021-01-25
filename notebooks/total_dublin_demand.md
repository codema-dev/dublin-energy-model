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
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt
```

```python
resi_sa = pd.read_csv("data/outputs/residential_small_area_demands.csv")
```

```python
resi_pcode = pd.read_csv("data/outputs/residential_postcode_demands.csv")
```

```python
comm_sa = pd.read_csv("data/outputs/commercial_sa_demands.csv")
```

```python
comm_pcode = pd.read_csv("data/outputs/commercial_postcode_demands.csv")
```

```python
comm_pcode['postcode'] = comm_pcode['postcodes'].str.lower()
```

```python
total_sa = pd.merge(resi_sa, comm_sa, left_on="GEOGID", right_on="small_area", how="left", indicator=True)
```

```python
total_sa['sa_elec_demand_kwh'] = total_sa['sa_elec_demand_kwh'].fillna(0)
```

```python
total_sa['sa_energy_demand_kwh_y'] = total_sa['sa_energy_demand_kwh_y'].fillna(0)
```

```python
total_sa["comm_peak_elec(kVA)"] = (total_sa["sa_elec_demand_kwh"] / (3600))*0.85
```

```python
total_sa
```

```python
total_sa["total_sa_energy_demand(kWh)"] = total_sa["sa_energy_demand_kwh_x"] + total_sa["sa_energy_demand_kwh_y"]
```

```python
total_sa["total_sa_elec_peak(kVA)"] = total_sa["sa_peak_elec_demand(kVA)"] + total_sa["comm_peak_elec(kVA)"]
```

```python
total_sa = total_sa[["GEOGID", "total_sa_energy_demand(kWh)", "total_sa_elec_peak(kVA)", "geometry"]]
```

```python
total_sa['geometry'] = total_sa['geometry'].apply(wkt.loads)
```

```python
total_sa = gpd.GeoDataFrame(total_sa, geometry = total_sa.geometry)
```

```python
total_pcode = pd.merge(resi_pcode, comm_pcode, on="postcode")
```

```python
total_pcode["total_postcode_elec_demand(kWh)"] = total_pcode["elec_per_postcode_kwh"] + total_pcode["postcode_elec_demand_kwh"]
```

```python
total_pcode["total_peak_elec(kVA)"] = (total_pcode["total_postcode_elec_demand(kWh)"] / (3600))*0.85
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
total_sa.plot(column="total_sa_elec_peak(kVA)", legend=True, legend_kwds={'label': "Total Elec Peak by Small_Area (kVA)"})
```

```python
total_sa.plot(column="total_sa_energy_demand(kWh)",legend=True, cmap="ocean", legend_kwds={'label': "Total Energy Demand by Small_Area (kWh)"})
```

```python
total_pcode.plot(column="total_postcode_energy_demand(kWh)",legend=True, legend_kwds={'label': "Total Energy Demand by Postcode (kWh)"})
```

```python
total_pcode.plot(column="total_peak_elec(kVA)",legend=True, legend_kwds={'label': "Total Peak Elec Demand by Postcode (kVA)"})
```

```python

```
