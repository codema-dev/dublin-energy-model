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
total_sa['sa_elec_demand_comm_kwh'] = total_sa['sa_elec_demand_comm_kwh'].fillna(0)
```


```python
total_sa['sa_elec_demand_comm_kw'] = total_sa['sa_elec_demand_comm_kw'].fillna(0)
```


```python
total_sa['sa_energy_demand_comm_kwh'] = total_sa['sa_energy_demand_comm_kwh'].fillna(0)
```


```python
total_sa["sa_comm_elec_peak_kw"] = total_sa["sa_comm_elec_peak_kw"].fillna(0)
```


```python
total_sa["sa_annual_elec_demand_resi_kwh"] = total_sa["sa_annual_elec_demand_resi_kwh"].fillna(0)
```


```python
total_sa["sa_elec_demand_dc_kwh"] = total_sa["sa_elec_demand_dc_kwh"].fillna(0)
```

```python
total_sa["sa_ff_demand_kwh"] = total_sa["sa_ff_demand_kwh"].fillna(0)
```

### Need to adopt for peak elec demands


```python
total_sa["total_sa_energy_demand_kWh"] = total_sa["sa_energy_demand_resi_kwh"] + total_sa["sa_energy_demand_comm_kwh"] 
```


```python
total_sa["total_sa_elec_peak_kW"] = total_sa["sa_peak_elec_demand_resi_kw"] + total_sa["sa_comm_elec_peak_kw"] + total_sa["sa_data_centre_elec_peak_kw"]
```


```python
total_sa["total_sa_elec_demand_kWh"] = total_sa["sa_annual_elec_demand_resi_kwh"] + total_sa["sa_elec_demand_comm_kwh"] + total_sa["sa_elec_demand_dc_kwh"]
```

```python
total_sa["sa_heat_demand_resi_kwh"] = total_sa["sa_energy_demand_resi_kwh"] - total_sa["sa_annual_elec_demand_resi_kwh"]
```

```python
total_sa["total_sa_heat_demand_kwh"] = total_sa["sa_heat_demand_resi_kwh"] + total_sa["sa_ff_demand_kwh"]
```

```python
total_sa.columns
```

```python
total_excel = total_sa[["GEOGID", "sa_energy_demand_resi_kwh", "sa_annual_elec_demand_resi_kwh", "sa_heat_demand_resi_kwh", "sa_peak_elec_demand_resi_kw", "sa_energy_demand_comm_kwh", "sa_ff_demand_kwh", "sa_elec_demand_comm_kwh", "sa_comm_elec_peak_kw", "sa_elec_demand_dc_kwh", "sa_data_centre_elec_peak_kw", "total_sa_energy_demand_kWh", "total_sa_elec_demand_kWh", "total_sa_heat_demand_kwh", "total_sa_elec_peak_kW", "geometry"]]
```

```python
pip install openpyxl
```

```python
total_excel.to_csv("data/outputs/total_demands_sa.csv")
```

```python
total_excel.to_excel("data/outputs/total_demands_sa.xlsx")
```

### Heat Demands for Tableau

```python
heat_map = total_sa[["GEOGID", "sa_heat_demand_resi_kwh", "sa_ff_demand_kwh", "total_sa_heat_demand_kwh", "geometry"]]
```

```python
heat_map = heat_map.iloc[:,0:5]
```

```python
heat_map['geometry'] = heat_map['geometry'].apply(wkt.loads)
```

```python
heat_map = gpd.GeoDataFrame(heat_map)
```

```python
heat_map['area'] = heat_map.area/ 10**6
```

```python
heat_map["sa_heat_demand_density_kWh/km2"] = (heat_map["total_sa_heat_demand_kwh"] / heat_map["area"])
```

```python
heat_map["sa_heat_demand_density_J/km2"] = heat_map["sa_heat_demand_density_kWh/km2"] / 3.6e6 
```

```python
heat_map["sa_heat_demand_density_TJ/km2"] = heat_map["sa_heat_demand_density_J/km2"] / (8760*3600)
```

```python
heat_map
```

```python
heat_map["sa_heat_demand_density_TJ/km2"].sort_values(ascending=False)
```

```python
heat_map["sa_heat_demand_density_TJ/km2"].mean()
```

```python
heat_map.plot(column="sa_heat_demand_density_TJ/km2", legend=True, cmap="cividis")
```

heat_map.to_file("data/outputs/sa_heat_demands.geojson", driver="GeoJSON")


### Extract values for Tableau Plotting


```python
tableau = total_sa[["GEOGID", "sa_energy_demand_resi_kwh", "sa_energy_demand_comm_kwh", "total_sa_energy_demand_kWh", "geometry"]]
```


```python
tableau = tableau.iloc[:,0:5]
```


```python
tableau['geometry'] = tableau['geometry'].apply(wkt.loads)
```


```python
tableau = gpd.GeoDataFrame(tableau)
```


tableau.to_file("data/outputs/sa_energy_tableau.geojson", driver="GeoJSON")


### Final GeoJSON Extraction


```python
total_sa = total_sa[["GEOGID", "total_sa_energy_demand_kWh", "total_sa_heat_demand_kwh", "total_sa_elec_peak_kW", "total_sa_elec_demand_kWh", "geometry"]]
```


```python
total_sa = total_sa.iloc[:,0:6]
```


```python
total_sa["total_sa_elec_demand_kWh"].sum()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GEOGID</th>
      <th>total_sa_energy_demand_kWh</th>
      <th>total_sa_elec_peak_kW</th>
      <th>total_sa_elec_demand_kWh</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>267001001</td>
      <td>7.532080e+05</td>
      <td>73.422667</td>
      <td>165849.996891</td>
      <td>POLYGON ((-6.24743299521722 53.4050672260164, ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>267001002</td>
      <td>1.130719e+06</td>
      <td>110.222462</td>
      <td>248974.814609</td>
      <td>POLYGON ((-6.2476758614919 53.4048398880569, -...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>267001003</td>
      <td>1.292251e+06</td>
      <td>125.968528</td>
      <td>284542.645268</td>
      <td>POLYGON ((-6.2491199410528 53.4066893345153, -...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>267001004</td>
      <td>1.165204e+06</td>
      <td>113.583981</td>
      <td>256567.946997</td>
      <td>POLYGON ((-6.24870968077833 53.4053268048826, ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>267001005</td>
      <td>1.190613e+06</td>
      <td>116.060891</td>
      <td>262162.886651</td>
      <td>POLYGON ((-6.25107997638216 53.4068130764238, ...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4871</th>
      <td>268137011</td>
      <td>7.290248e+05</td>
      <td>90.413400</td>
      <td>142978.639000</td>
      <td>POLYGON ((-6.27256553001906 53.3227864269897, ...</td>
    </tr>
    <tr>
      <th>4872</th>
      <td>268137012</td>
      <td>9.586431e+05</td>
      <td>129.235604</td>
      <td>239134.423493</td>
      <td>POLYGON ((-6.26812824346867 53.3224690939469, ...</td>
    </tr>
    <tr>
      <th>4873</th>
      <td>268137013</td>
      <td>1.856850e+06</td>
      <td>317.510010</td>
      <td>684287.127476</td>
      <td>POLYGON ((-6.26560658628045 53.3228032240522, ...</td>
    </tr>
    <tr>
      <th>4874</th>
      <td>268137014</td>
      <td>6.996944e+05</td>
      <td>80.877414</td>
      <td>128668.221261</td>
      <td>POLYGON ((-6.26906730720534 53.323741486111, -...</td>
    </tr>
    <tr>
      <th>4875</th>
      <td>268137015</td>
      <td>8.521063e+05</td>
      <td>102.694479</td>
      <td>162383.871370</td>
      <td>POLYGON ((-6.26807200173066 53.3221638940925, ...</td>
    </tr>
  </tbody>
</table>
<p>4876 rows × 5 columns</p>
</div>




```python
total_sa['geometry'] = total_sa['geometry'].apply(wkt.loads)
```


```python
total_sa = gpd.GeoDataFrame(total_sa, geometry = total_sa.geometry)
```


```python
total_sa.loc[total_sa["GEOGID"] == "267028004/02"]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GEOGID</th>
      <th>total_sa_energy_demand_kWh</th>
      <th>total_sa_elec_peak_kW</th>
      <th>total_sa_elec_demand_kWh</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1856</th>
      <td>267028004/02</td>
      <td>4.510863e+06</td>
      <td>543.325443</td>
      <td>2.226321e+06</td>
      <td>POLYGON ((-6.46233 53.38587, -6.46230 53.38592...</td>
    </tr>
  </tbody>
</table>
</div>





total_sa.to_file("data/outputs/sa_total_demands.geojson", driver="GeoJSON")



```python
total_pcode = pd.merge(resi_pcode, comm_pcode, on="postcode")
```


```python
total_pcode["total_postcode_elec_demand_kWh"] = total_pcode["elec_per_postcode_kwh"] + total_pcode["cibse_postcode_elec_demand_kwh"]
```

### First converting kWh to kW, then to kVA assuming PF of 0.85


```python
total_pcode["total_peak_elec_kVA"] = (total_pcode["total_postcode_elec_demand_kWh"] / (8760))*0.85
```


```python
total_pcode["total_postcode_energy_demand_kWh"] = total_pcode["energy_per_postcode_kwh"] + total_pcode["postcode_energy_demand_kwh"]
```


```python
total_pcode = total_pcode[["postcode", "total_postcode_energy_demand_kWh", "total_postcode_elec_demand_kWh", "total_peak_elec_kVA", "geometry_x"]]
```


```python
total_pcode['geometry'] = total_pcode['geometry_x'].apply(wkt.loads)
```


```python
total_pcode = gpd.GeoDataFrame(total_pcode, geometry = total_pcode.geometry)
```


```python
total_sa.plot(figsize=(10, 10), column="total_sa_elec_demand_kWh", legend=True, cmap="cividis", legend_kwds={'label': "Annual Electricity Demand by Small Area (kW)"},)
```
```python
total_sa.plot(column="total_sa_energy_demand_kWh",figsize=(10, 10), legend=True, cmap="cividis", legend_kwds={'label': "Total Energy Demand by Small_Area (kWh)"})
```
```python
total_pcode.plot(column="total_postcode_energy_demand_kWh",legend=True, legend_kwds={'label': "Total Energy Demand by Postcode (kWh)"})
```
```python
total_pcode.plot(column="total_peak_elec_kVA",legend=True, legend_kwds={'label': "Total Peak Elec Demand by Postcode (kVA)"})
```
### Deprevation Index


```python
dep = pd.read_csv("data/roughwork/dublin-ed-dep-index.csv")
```

```python
dep
```

```python
ber = pd.read_csv("data/resi_modelling/BER.09.06.2020.csv", encoding="unicode_escape", error_bad_lines=False, engine="python").drop_duplicates()
```

```python
ber = ber[ber["CountyName2"].str.contains("DUBLIN")]
```

```python
ber["Energy_Number"] = ber["Energy Rating"].map({
            "A1": 1,
            "A2": 2,
            "A3": 3,
            "B1": 4,
            "B2": 5,
            "B3": 6,
            "C1": 7,
            "C2": 8,
            "C3": 9,
            "D1": 10,
            "D2": 11,
            "E1": 12,
            "E2": 13,
            "F": 14,
            "G": 15,
        })
```

```python
ed_ber = ber.groupby("ED_Name")["Energy_Number"].mean().to_frame().reset_index()
```

```python
ed_ber["Energy_Number"] = ed_ber["Energy_Number"].fillna(0.0).astype(int)
```

```python
dep_ber = pd.merge(dep, ed_ber, on="ED_Name")
```

```python
dep_ber = pd.merge(dep, ed_ber, on="ED_Name")
```

```python
ed_geom = gpd.read_file("data/spatial/dublin_ed_geometries_cso.shp")
```

```python
dep_final = pd.merge(dep_ber, ed_geom, left_on="ED_Name", right_on="ED_ENGLISH")
```

```python
dep_final["BER_Rating"] = dep_final["Energy_Number"].map({
           1 : "A1",
           2 : "A2",
           3 : "A3",
           4 : "B1",
           5 : "B2",
           6 : "B3",
           7 : "C1",
           8 : "C2",
           9 : "C3",
           10 : "D1",
           11 : "D2",
           12 : "E1",
           13 : "E2",
           14 : "F",
           15 : "G",
        })
```

```python
dep_final = gpd.GeoDataFrame(dep_final)
```

```python
dep_final = dep_final.to_crs(epsg="4326")
```

```python
bound = gpd.read_file("data/roughwork/dublin_admin/Census2011_Admin_Counties_generalised20m.shp")
```

```python
bound = bound.to_crs(epsg="4326")
```

```python
dep_final = gpd.sjoin(dep_final, bound, op="within")
```

```python
pov = dep_final[(dep_final['UNEMP16'] > 25) & (dep_final['Energy_Number'] <= 12 )]
```

```python
pov = dep_final[(dep_final['Energy_Number'] <= 12 ) & (dep_final['HP2016abs'] <= -20 )]
```

```python
pov = dep_final[(dep_final['UNEMP16'] > 25) & (dep_final['HP2016abs'] <= -20 )]
```

```python
pov
```

```python
dep_final.to_file("data/outputs/ed_deprevation_index.geojson", driver="GeoJSON")
```

```python

```

```python
sa = gpd.read_parquet("data/spatial/small_area_geometries_2016.parquet")
```

```python
sa.to_csv("data/spatial/sa_geometries.csv")
```

```python
dep = pd.read_csv("data/resi_modelling/dublin_deprevation_index_by_sa.csv")
```
```python
dep_geom = pd.merge(dep, sa, left_on="cso_small_area", right_on="small_area", how="inner")
```

```python
dep_geom = dep_geom[["cso_small_area", "COUNTY", "Population_2011", "Score_2011", "Decile_2011", "Population_2016", "Score_2016", "Decile_2016", "geometry"]]
```

```python
dep_geom = dep_geom.iloc[:,0:9]
```

```python
dep_geom = gpd.GeoDataFrame(dep_geom)
```

```python
dep_geom.plot(column="Decile_2016", legend=True, cmap="cividis", legend_kwds={'label': "Decile Rating by SA"})
```

```python
dep_geom.to_file("data/outputs/sa_deprevation_index.geojson", driver="GeoJSON")
```

# Emissions

```python
df_demands = pd.read_csv("data/outputs/total_demands_sa.csv")
```

```python
df_demands
```

```python
df_em = df_demands[["GEOGID", "sa_annual_elec_demand_resi_kwh", "sa_heat_demand_resi_kwh", "sa_elec_demand_comm_kwh", "sa_ff_demand_kwh", "sa_elec_demand_dc_kwh", "geometry"]]
```

```python
df_em.columns
```

```python
df_em["sa_resi_elec_emissions_TCO2"] = (df_em["sa_annual_elec_demand_resi_kwh"]*324.5)*1e-6
```

```python
df_em["sa_resi_heat_emissions_TCO2"] = (df_em["sa_heat_demand_resi_kwh"]*267.939)*1e-6
```

```python
df_em["sa_comm_elec_emissions_TCO2"] = (df_em["sa_elec_demand_comm_kwh"]*324.5)*1e-6
```

```python
df_em["sa_comm_heat_emissions_TCO2"] = (df_em["sa_ff_demand_kwh"]*251.9)*1e-6
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
df_em = gpd.GeoDataFrame(df_em)
```

```python
df_em['geometry'] = df_em['geometry'].apply(wkt.loads)
```

```python
df_em["centroids"] = df_em.geometry.centroid
```

```python
df_em = df_em.rename(columns={"centroids": "geometry"})
```

```python
import sys
sys.setrecursionlimit(100000) # 10000 is an example, try with different values
```

```python
df_em
```

```python
df_em = df_em.set_crs(epsg="4326")
```

```python
dublin_em = gpd.sjoin(df_em, bound, op="within")
```

```python
dublin_em["COUNTYNAME"].value_counts()
```

```python
sdcc_em = dublin_em[dublin_em["COUNTYNAME"].str.contains("South Dublin")]
```

```python
sdcc_em
```

```python
dublin_em["COUNTYNAME"].value_counts()
```

```python
sdcc_em.plot()
```

```python
sdcc_em.plot(figsize=(10, 10), column="total_sa_resi_emissions_TCO2", legend=True, legend_kwds={'label': "Total SDCC Annual Carbon Emissions by Small Area (kW)"},)
```

```python
sdcc_em.plot(column="total_sa_resi_emissions_TCO2")
```

```python

```
