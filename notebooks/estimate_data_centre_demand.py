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

# %%
# cd ..

# %%
import pandas as pd
import geopandas as gpd
import glob
from pathlib import Path
import numpy as np
import pygeos
import rtree
import matplotlib.pyplot as plt

# %% [markdown]
# ### Read in data centre load information from Bitpower

# %%
dc = pd.read_csv("data/commercial/bitpower_data_centres.csv")

# %%
dc_built = dc.loc[dc["Stage of Development"] == "5 - Built"]

# %%
dc_geom = gpd.GeoDataFrame(dc_built, geometry=gpd.points_from_xy(dc_built.Longitude, dc_built.Latitude))

# %%
dc_geom["data_centre_peak_kw"] = (dc_geom["Annual Electrical Consumption (kWh)"] / 8760) / dc_geom["alf"]

# %%
dc_geom = dc_geom.set_crs(epsg="4326")

# %% [markdown]
# ### Annual Electrical Consumption is rated at 42.5% Utilisation of Capacity

# %%
postcode = gpd.read_parquet("data/spatial/dublin_postcodes.parquet")

# %%
small_areas = gpd.read_parquet("data/spatial/small_area_geometries_2016.parquet")

# %%
dc_pcode = gpd.sjoin(dc_geom, postcode, op="within")

# %%
dc_sa = gpd.sjoin(dc_geom, small_areas, op="within")

# %%
pcode_demand_dc = dc_pcode.groupby("postcodes")["Annual Electrical Consumption (kWh)"].sum().rename("postcode_elec_demand_dc_kwh").reset_index()

# %%
pcode_demand_dc = pd.merge(pcode_demand_dc, postcode, on="postcodes")

# %%
pcode_demand_dc  = gpd.GeoDataFrame(pcode_demand_dc)

# %%
sa_demand_dc = dc_sa.groupby("small_area")["Annual Electrical Consumption (kWh)"].sum().rename("sa_elec_demand_dc_kwh").reset_index()

# %%
sa_demand_dc = pd.merge(sa_demand_dc, small_areas, on="small_area")

# %%
sa_demand_dc = gpd.GeoDataFrame(sa_demand_dc)

# %% [markdown]
# ### Peak elec values coming from ALF category computed from SME profiles & USA report

# %%
pcode_peak_dc = dc_pcode.groupby("postcodes")["data_centre_peak_kw"].sum().rename("postcode_data_centre_elec_peak_kw").reset_index()

# %%
pcode_demand_dc = pd.merge(pcode_demand_dc, pcode_peak_dc, on="postcodes")

# %%
pcode_demand_dc["postcode_elec_demand_dc_kwh"].sum()

# %%
sa_peak_dc = dc_sa.groupby("small_area")["data_centre_peak_kw"].sum().rename("sa_data_centre_elec_peak_kw").reset_index()

# %%
sa_demand_dc = pd.merge(sa_demand_dc, sa_peak_dc, on="small_area")

# %%
sa_demand_dc

# %%
pcode_demand_dc.plot(column="postcode_elec_demand_dc_kwh", legend=True, legend_kwds={'label': "Annual Data Centre Elec Demand by Postcode (kWh)"})

# %%
pcode_demand_dc.to_csv("data/interim/data_centre_postcode_demands.csv")

# %%
sa_demand_dc.plot(column="sa_elec_demand_dc_kwh", legend=True, legend_kwds={'label': "Annual Data Centre Elec Demand by Small Area (kWh)"})

# %%
sa_demand_dc.to_csv("data/interim/data_centre_sa_demands.csv")
