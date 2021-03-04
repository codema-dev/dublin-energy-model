# ---
# jupyter:
#   jupytext:
#     formats: ipynb,md
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.10.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Combining Residential & Commercial Demands for a City-Wide Model

# %%
# cd ..

# %%
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely import wkt

# %% [markdown]
# ### Call csv outputs from other notebooks

# %%
resi_sa = pd.read_csv("data/interim/residential_small_area_demands.csv")

# %%
resi_pcode = pd.read_csv("data/interim/residential_postcode_demands.csv")

# %%
comm_sa = pd.read_csv("data/interim/commercial_sa_demands.csv")

# %%
comm_pcode = pd.read_csv("data/interim/commercial_postcode_demands.csv")

# %%
dc_sa = pd.read_csv("data/interim/data_centre_sa_demands.csv")

# %%
dc_sa["small_area"] = dc_sa['small_area'].astype(str)

# %%
dc_pcode = pd.read_csv("data/interim/data_centre_postcode_demands.csv")

# %%
comm_pcode['postcode'] = comm_pcode['postcodes'].str.lower()

# %%
total_sa = pd.merge(resi_sa, comm_sa, left_on="GEOGID", right_on="small_area", how="left", indicator=True)

# %%
total_sa = pd.merge(total_sa, dc_sa, left_on="GEOGID", right_on="small_area", how="left")

# %%
total_sa = total_sa.rename(columns={'geometry_x': 'geometry'})

# %%
total_sa["sa_data_centre_elec_peak_kw"] = total_sa['sa_data_centre_elec_peak_kw'].fillna(0)

# %%
total_sa['sa_elec_demand_kwh'] = total_sa['sa_elec_demand_kwh'].fillna(0)

# %%
total_sa['sa_elec_demand_kw'] = total_sa['sa_elec_demand_kw'].fillna(0)

# %%
total_sa['sa_energy_demand_kwh_y'] = total_sa['sa_energy_demand_kwh_y'].fillna(0)

# %%
total_sa["sa_comm_elec_peak_kw"] = total_sa["sa_comm_elec_peak_kw"].fillna(0)

# %% [markdown]
# ### Need to adopt for peak elec demands

# %%
total_sa["total_sa_energy_demand(kWh)"] = total_sa["sa_energy_demand_kwh_x"] + total_sa["sa_energy_demand_kwh_y"] 

# %%
total_sa["total_sa_elec_peak(kW)"] = total_sa["sa_peak_elec_demand(kW)"] + total_sa["sa_comm_elec_peak_kw"] + total_sa["sa_data_centre_elec_peak_kw"]

# %%
total_sa["sa_peak_elec_demand(kW)"].sum()

# %%
total_sa["sa_comm_elec_peak_kw"].sum()

# %%
total_sa = total_sa[["GEOGID", "total_sa_energy_demand(kWh)", "total_sa_elec_peak(kW)", "geometry"]]

# %%
total_sa = total_sa.iloc[:,0:5]

# %%
total_sa['geometry'] = total_sa['geometry'].apply(wkt.loads)

# %%
total_sa = gpd.GeoDataFrame(total_sa, geometry = total_sa.geometry)

# %%
total_sa

# %%
total_sa.to_file("data/outputs/sa_total_demands.geojson", driver="GeoJSON")

# %%
total_pcode = pd.merge(resi_pcode, comm_pcode, on="postcode")

# %%
total_pcode["total_postcode_elec_demand(kWh)"] = total_pcode["elec_per_postcode_kwh"] + total_pcode["cibse_postcode_elec_demand_kwh"]

# %% [markdown]
# ### First converting kWh to kW, then to kVA assuming PF of 0.85

# %%
total_pcode["total_peak_elec(kVA)"] = (total_pcode["total_postcode_elec_demand(kWh)"] / (8760))*0.85

# %%
total_pcode["total_postcode_energy_demand(kWh)"] = total_pcode["energy_per_postcode_kwh"] + total_pcode["postcode_energy_demand_kwh"]

# %%
total_pcode = total_pcode[["postcode", "total_postcode_energy_demand(kWh)", "total_postcode_elec_demand(kWh)", "total_peak_elec(kVA)", "geometry_x"]]

# %%
total_pcode['geometry'] = total_pcode['geometry_x'].apply(wkt.loads)

# %%
total_pcode = gpd.GeoDataFrame(total_pcode, geometry = total_pcode.geometry)

# %%
total_sa.plot(figsize=(10, 10), column="total_sa_elec_peak(kW)", legend=True, cmap="cividis", legend_kwds={'label': "Electricity Demands Peaks by Small Area (kW)"},)

# %%
total_sa.plot(column="total_sa_energy_demand(kWh)",figsize=(10, 10), legend=True, cmap="cividis", legend_kwds={'label': "Total Energy Demand by Small_Area (kWh)"})

# %%
total_pcode.plot(column="total_postcode_energy_demand(kWh)",legend=True, legend_kwds={'label': "Total Energy Demand by Postcode (kWh)"})

# %%
total_pcode.plot(column="total_peak_elec(kVA)",legend=True, legend_kwds={'label': "Total Peak Elec Demand by Postcode (kVA)"})

# %%

# %% [markdown]
# ### Calculating totals

# %%
resi_pcode["elec_per_postcode_kwh"].sum()

# %%
