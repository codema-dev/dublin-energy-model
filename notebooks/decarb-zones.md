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
```

```python
df = pd.read_csv("data/roughwork/dublin_indiv_hh.csv")
```

```python
saps = pd.read_csv("data/spatial/SAPS2016_SA2017.csv")
```

```python
saps["GEOGID"] = saps["GEOGID"].str.replace("SA2017_", "")
```

```python
zone = gpd.read_file("data/spatial/decarb_zones/clondalkin-revised.gpkg")
```

```python
zone
```

```python
zone_resi = pd.merge(df, zone, left_on="SMALL_AREA_2016", right_on="GEOGID_left")
```

```python
zone_period = zone_resi["period_built"].value_counts().to_frame().reset_index()
```

```python
zone_period
```

```python
zone_period.plot(x="index", y=["period_built"], kind="bar")
plt.title("Clondalkin Decarb Zone Residential Periods of Construction from CSO 2016")
plt.xlabel("Period of Construction")
plt.ylabel("Count")
```

```python
zone_period = zone_resi["BERBand"].value_counts().to_frame().reset_index()
```

```python
zone_period.plot(x="index", y=["BERBand"], kind="bar")
plt.title("Clondalkin Decarb Zone Residential BER Bands")
plt.xlabel("BER Rating Band")
plt.ylabel("Count")
```

```python
zone_saps = pd.merge(zone, saps, left_on="GEOGID_left", right_on="GEOGID")
```

```python
zone_dwelling = zone_saps[["GEOGID_left", "T6_3_OMLH", "T6_3_OOH", "T6_3_RPLH", "T6_3_RLAH", "T6_3_RVCHBH", "T6_3_OFRH", "T6_3_NSH", "T6_3_TH"]]
```

```python
zone_dwelling = zone_dwelling.rename(columns = {'GEOGID_left':'GEOGID', "T6_3_OMLH":"Owned with mortgage or loan", "T6_3_OOH":"Owned outright", "T6_3_RPLH":"Rented from private landlord", "T6_3_RLAH":"Rented from Local Authority", "T6_3_RVCHBH":"Rented from voluntary/co-operative housing body", "T6_3_OFRH":"Occupied free of rent", "T6_3_NSH":"Not Stated", "T6_3_TH":"Total"})
```

```python
zone_dwelling.loc['Total']= zone_dwelling.sum()
```

```python
zone_dwelling_total = zone_dwelling.loc[["Total"]]
```

```python
zone_dwelling_transpose = zone_dwelling_total.transpose()
```

```python
zone_dwelling_transpose = zone_dwelling_transpose.reset_index()
```

```python
zone_dwelling_transpose.at[0, 'Total'] = "total"
```

```python
zone_dwelling_transpose = zone_dwelling_transpose[1:7]
```

```python
zone_dwelling_transpose
```

```python
zone_dwelling_transpose.plot(x="index", y=["Total"], kind="barh")
plt.title("Clondalkin Decarb Zone Housing by Occupancy")
plt.xlabel("Occupancy Type")
plt.ylabel("Count")
```

```python
(zone_saps["T6_3_OMLH"].sum() + zone_saps["T6_3_OOH"].sum()) / zone_saps["T6_3_TH"].sum() 
```

```python
zone_saps["T6_3_TH"].sum()
```

```python

```
