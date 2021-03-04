# Combining Residential & Commercial Demands for a City-Wide Model


```python
cd ..
```

    /workspaces/energyplus-archetypes-main



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
total_sa
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
      <th>Unnamed: 0_x</th>
      <th>GEOGID</th>
      <th>sa_energy_demand_resi_kwh</th>
      <th>sa_peak_elec_demand_resi_kw</th>
      <th>sa_annual_elec_demand_resi_kwh</th>
      <th>geometry</th>
      <th>sa_peak_elec(kVA)</th>
      <th>Unnamed: 0_y</th>
      <th>small_area_x</th>
      <th>sa_energy_demand_comm_kwh</th>
      <th>sa_elec_demand_comm_kwh</th>
      <th>sa_elec_demand_comm_kw</th>
      <th>sa_comm_elec_peak_kw</th>
      <th>geometry</th>
      <th>_merge</th>
      <th>Unnamed: 0</th>
      <th>small_area_y</th>
      <th>sa_elec_demand_dc_kwh</th>
      <th>geometry_y</th>
      <th>sa_data_centre_elec_peak_kw</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>267001001</td>
      <td>7.532080e+05</td>
      <td>73.422667</td>
      <td>165849.996891</td>
      <td>POLYGON ((-6.24743299521722 53.4050672260164, ...</td>
      <td>62.409267</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>left_only</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>267001002</td>
      <td>1.130719e+06</td>
      <td>110.222462</td>
      <td>248974.814609</td>
      <td>POLYGON ((-6.2476758614919 53.4048398880569, -...</td>
      <td>93.689092</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>left_only</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>267001003</td>
      <td>1.292251e+06</td>
      <td>125.968528</td>
      <td>284542.645268</td>
      <td>POLYGON ((-6.2491199410528 53.4066893345153, -...</td>
      <td>107.073248</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>left_only</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>267001004</td>
      <td>1.165204e+06</td>
      <td>113.583981</td>
      <td>256567.946997</td>
      <td>POLYGON ((-6.24870968077833 53.4053268048826, ...</td>
      <td>96.546384</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>left_only</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>267001005</td>
      <td>1.190613e+06</td>
      <td>116.060891</td>
      <td>262162.886651</td>
      <td>POLYGON ((-6.25107997638216 53.4068130764238, ...</td>
      <td>98.651757</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>left_only</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4871</th>
      <td>4871</td>
      <td>268137011</td>
      <td>6.903900e+05</td>
      <td>85.583791</td>
      <td>131344.112507</td>
      <td>POLYGON ((-6.27256553001906 53.3227864269897, ...</td>
      <td>72.746223</td>
      <td>2402.0</td>
      <td>268137011</td>
      <td>3.863475e+04</td>
      <td>11634.526493</td>
      <td>1.328142</td>
      <td>4.829608</td>
      <td>POLYGON ((-6.27256553001906 53.3227864269897, ...</td>
      <td>both</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4872</th>
      <td>4872</td>
      <td>268137012</td>
      <td>6.309006e+05</td>
      <td>78.209224</td>
      <td>120026.479230</td>
      <td>POLYGON ((-6.26812824346867 53.3224690939469, ...</td>
      <td>66.477841</td>
      <td>2403.0</td>
      <td>268137012</td>
      <td>3.277424e+05</td>
      <td>119107.944264</td>
      <td>13.596797</td>
      <td>51.026380</td>
      <td>POLYGON ((-6.26812824346867 53.3224690939469, ...</td>
      <td>both</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4873</th>
      <td>4873</td>
      <td>268137013</td>
      <td>6.168110e+05</td>
      <td>76.462616</td>
      <td>117345.987138</td>
      <td>POLYGON ((-6.26560658628045 53.3228032240522, ...</td>
      <td>64.993224</td>
      <td>2404.0</td>
      <td>268137013</td>
      <td>1.240039e+06</td>
      <td>566941.140338</td>
      <td>64.719308</td>
      <td>241.047394</td>
      <td>POLYGON ((-6.26560658628045 53.3228032240522, ...</td>
      <td>both</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4874</th>
      <td>4874</td>
      <td>268137014</td>
      <td>6.042870e+05</td>
      <td>74.910076</td>
      <td>114963.327500</td>
      <td>POLYGON ((-6.26906730720534 53.323741486111, -...</td>
      <td>63.673564</td>
      <td>2405.0</td>
      <td>268137014</td>
      <td>9.540743e+04</td>
      <td>13704.893760</td>
      <td>1.564486</td>
      <td>5.967338</td>
      <td>POLYGON ((-6.26906730720534 53.323741486111, -...</td>
      <td>both</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4875</th>
      <td>4875</td>
      <td>268137015</td>
      <td>7.811896e+05</td>
      <td>96.839709</td>
      <td>148618.394877</td>
      <td>POLYGON ((-6.26807200173066 53.3221638940925, ...</td>
      <td>82.313753</td>
      <td>2406.0</td>
      <td>268137015</td>
      <td>7.091666e+04</td>
      <td>13765.476493</td>
      <td>1.571401</td>
      <td>5.854769</td>
      <td>POLYGON ((-6.26807200173066 53.3221638940925, ...</td>
      <td>both</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>4876 rows × 20 columns</p>
</div>




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


```python
tableau.to_file("data/outputs/sa_energy_tableau.geojson", driver="GeoJSON")
```

### Final GeoJSON Extraction


```python
total_sa = total_sa[["GEOGID", "total_sa_energy_demand_kWh", "total_sa_elec_peak_kW", "total_sa_elec_demand_kWh", "geometry"]]
```


```python
total_sa = total_sa.iloc[:,0:5]
```


```python
total_sa
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




```python
total_sa.to_file("data/outputs/sa_total_demands.geojson", driver="GeoJSON")
```


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




    <AxesSubplot:>




    
![png](output_49_1.png)
    



```python
total_sa.plot(column="total_sa_energy_demand_kWh",figsize=(10, 10), legend=True, cmap="cividis", legend_kwds={'label': "Total Energy Demand by Small_Area (kWh)"})
```




    <AxesSubplot:>




    
![png](output_50_1.png)
    



```python
total_pcode.plot(column="total_postcode_energy_demand_kWh",legend=True, legend_kwds={'label': "Total Energy Demand by Postcode (kWh)"})
```




    <AxesSubplot:>




    
![png](output_51_1.png)
    



```python
total_pcode.plot(column="total_peak_elec_kVA",legend=True, legend_kwds={'label': "Total Peak Elec Demand by Postcode (kVA)"})
```




    <AxesSubplot:>




    
![png](output_52_1.png)
    


### Calculating totals


```python
resi_pcode["elec_per_postcode_kwh"].sum()
```




    1209330555.7895122




```python
bhill = total_sa.loc[total_sa["GEOGID"] == "267034001/01"]
```


```python
bhill
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
      <th>2061</th>
      <td>267034001/01</td>
      <td>2.091150e+08</td>
      <td>53836.841596</td>
      <td>1.167064e+08</td>
      <td>POLYGON ((-6.42205 53.41650, -6.42198 53.41646...</td>
    </tr>
  </tbody>
</table>
</div>


