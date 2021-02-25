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
# # Commercial Modelling for Dublin using the VO Dataset

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

# %%
df = pd.concat(map(pd.read_csv, glob.glob('data/commercial/vo/*.csv')))

# %%
df['Area'] = df['Area'].fillna(0)

# %%
df_area = df[(df['Area'] > 5) & (df['Area'] <= 50000 )]

# %% [markdown]
# ### Need to define area limits to correct for VO input errors

# %%
df_outliers = df[(df['Area'] < 5) | (df['Area'] >= 50000 )]

# %%
df_outliers = df_outliers.drop_duplicates(subset="Property Number")

# %%
mean_category_area = df_area.groupby("Uses")["Area"].mean().rename("property_total_area").to_frame().reset_index()

# %%
df_outliers = pd.merge(df_outliers, mean_category_area, on="Uses")

# %%
df_ext = df_area.drop_duplicates(subset=['Property Number', 'Area'])

# %%
df_out = df_ext.groupby(by="Property Number", as_index=True)["Area"].sum().rename("property_total_area").to_frame().reset_index()

# %%
df_merge = pd.merge(df, df_out, on="Property Number")

# %%
df_final = df_merge.drop_duplicates(subset=['Property Number'])

# %%
df_final = pd.concat([df_final, df_outliers])

# %%
df_final["Uses_Clean"] = df_final['Uses'].str.replace(r', -', '')

# %% [markdown]
# ### Remove Data Centres

# %%
df_final = df_final.loc[df_final["Uses"] != "DATA CENTRE, -"]

# %% [markdown]
# ### Cibse benchmarks provide references values per floor area

# %%
benchmarks = pd.read_csv("data/commercial/benchmark_use_links_usa.csv")

# %%
bench_linked = pd.merge(df_final, benchmarks, left_on="Uses_Clean", right_on="Uses")

# %%
bench_linked["ff_demand_kwh"] = bench_linked["property_total_area"] * bench_linked["typical_fossil_fuel"]

# %%
bench_linked["elec_demand_kwh"] = bench_linked["property_total_area"] * bench_linked["typical_electricity"]

# %%
bench_linked = gpd.GeoDataFrame(bench_linked, geometry=gpd.points_from_xy(bench_linked[" X ITM"], bench_linked[" Y ITM"]))

# %%
bench_linked = bench_linked.set_crs(epsg = "2157")

# %%
bench_linked = bench_linked.to_crs(epsg = "4326")

# %%
postcode = gpd.read_parquet("data/spatial/dublin_postcodes.parquet")

# %%
small_areas = gpd.read_parquet("data/spatial/small_area_geometries_2016.parquet")

# %%
elec_pcode = gpd.sjoin(bench_linked, postcode, op="within")

# %%
elec_sa = gpd.sjoin(bench_linked, small_areas, op="within")

# %%
elec_sa["comm_peak_kw"] = (elec_sa["elec_demand_kwh"] / 8760) / elec_sa["alf"]

# %%
elec_sa["elec_demand_kwh"].sum()

# %%
largest_consumer = elec_sa["elec_demand_kwh"].sort_values()

# %%
pcode_demand_elec = elec_pcode.groupby("postcodes")["elec_demand_kwh"].sum().rename("cibse_postcode_elec_demand_kwh").reset_index()

# %%
pcode_demand_ff = elec_pcode.groupby("postcodes")["ff_demand_kwh"].sum().rename("postcode_ff_demand_kwh").reset_index()

# %%
pcode_demand_elec = pd.merge(pcode_demand_elec, postcode, on="postcodes")

# %%
pcode_demand_elec = gpd.GeoDataFrame(pcode_demand_elec)

# %%
pcode_demand_ff = pd.merge(pcode_demand_ff, postcode, on="postcodes")

# %%
pcode_demand_ff = gpd.GeoDataFrame(pcode_demand_ff)

# %%
sa_demand_elec = elec_sa.groupby("small_area")["elec_demand_kwh"].sum().rename("sa_elec_demand_kwh").reset_index()

# %%
sa_demand_ff = elec_sa.groupby("small_area")["ff_demand_kwh"].sum().rename("sa_ff_demand_kwh").reset_index()

# %% [markdown]
# ### Peak elec values coming from ALF category computed from SME profiles & USA report

# %%
sa_peak_elec = elec_sa.groupby("small_area")["comm_peak_kw"].sum().rename("sa_comm_elec_peak_kw").reset_index()

# %%
sa_demand_elec = pd.merge(sa_demand_elec, small_areas, on="small_area")

# %%
sa_demand_elec = gpd.GeoDataFrame(sa_demand_elec)

# %%
sa_demand_elec = pd.merge(sa_demand_elec, sa_peak_elec, on="small_area")

# %%
sa_demand_ff = pd.merge(sa_demand_ff, small_areas, on="small_area")

# %%
sa_demand_ff = gpd.GeoDataFrame(sa_demand_ff)

# %%
sa_demand_total = pd.merge(sa_demand_ff, sa_demand_elec, on="small_area")

# %% [markdown]
# ### Cibse Energy is the sum of the Elec & FF values

# %%
sa_demand_total["sa_energy_demand_kwh"] = sa_demand_total["sa_ff_demand_kwh"] + sa_demand_total["sa_elec_demand_kwh"]

# %% [markdown]
# ### Values in kWh are annual so divisible by 8760 to relate to kW

# %%
sa_demand_total["sa_elec_demand_kw"] = sa_demand_total["sa_elec_demand_kwh"] / 8760

# %%
sa_demand_total

# %%
sa_demand_final = sa_demand_total[["small_area", "sa_energy_demand_kwh", "sa_elec_demand_kwh", "sa_elec_demand_kw", "sa_comm_elec_peak_kw", "geometry_x"]]

# %%
sa_demand_final = gpd.GeoDataFrame(sa_demand_final, geometry="geometry_x")

# %%
sa_demand_final["sa_elec_demand_kwh"].sum()

# %%
pcode_demand_total = pd.merge(pcode_demand_ff, pcode_demand_elec, on="postcodes")

# %%
pcode_demand_total["postcode_energy_demand_kwh"] = pcode_demand_total["postcode_ff_demand_kwh"] + pcode_demand_total["cibse_postcode_elec_demand_kwh"]

# %%
pcode_demand_final = pcode_demand_total[["postcodes", "postcode_energy_demand_kwh", "cibse_postcode_elec_demand_kwh", "geometry_x"]]

# %%
pcode_demand_final = gpd.GeoDataFrame(pcode_demand_final, geometry="geometry_x")

# %%
pcode_demand_final.plot(column="postcode_energy_demand_kwh", figsize=(10, 10), legend=True, legend_kwds={'label': "Commercial Annual Energy Demand by Postcode (kWh)"})

# %%
pcode_demand_final.plot(column="cibse_postcode_elec_demand_kwh", legend=True, legend_kwds={'label': "Commercial Elec Demand by Postcode (kWh)"})

# %%
pcode_demand_final.to_csv("data/interim/commercial_postcode_demands.csv")

# %%
sa_demand_final.plot(figsize=(10, 10), column="sa_energy_demand_kwh", legend=True, legend_kwds={'label': "Commercial Annual Energy Demand by Small Area (kWh)"})

# %%
sa_demand_final.plot(figsize=(10, 10), column="sa_elec_demand_kwh", legend=True, legend_kwds={'label': "Commercial Elec Demand by Small Area (kWh)"})

# %%
sa_demand_final.plot(figsize=(10, 10), column="sa_comm_elec_peak_kw", legend=True, legend_kwds={'label': "Commercial Peak Elec Demand by Small Area (kW)"})

# %%
sa_demand_final.to_csv("data/interim/commercial_sa_demands.csv")

# %% [markdown]
# ## Calculating Peak Demands from SME Profiles

# %%
import matplotlib.pyplot as plt
import datetime as dt

# %%
comm_peak = pd.read_csv("data/roughwork/cer_smart_meter/other-transportation-and-storage.csv")

# %%
comm_peak = pd.DataFrame(comm_peak)

# %%
comm_peak["datetime"] = pd.to_datetime(comm_peak['datetime'])

# %%
comm_2010 = comm_peak[(comm_peak["datetime"].dt.year == 2010)]

# %%
comm_hourly = comm_2010.iloc[::2, :].reset_index()

# %%
comm_hourly

# %%
plt.plot_date(comm_hourly["datetime"].loc[100:300], comm_hourly["demand"].loc[100:300], linestyle='--', marker='o', color='b')

# %%
comm_demand = comm_hourly["demand"].sum()

# %%
comm_peak = comm_hourly["demand"].max()

# %%
comm_alf = ((comm_demand/8760)/comm_peak)

# %%
comm_alf

# %% [markdown]
# ### Wrangling the VO dataset

# %%
df_zero_area = df_final.loc[df_final["Area"] == 0]

# %%
df_zero_area["Uses"].value_counts()

# %%
df[df["Category"].str.contains("HOSPITALITY", na=False)]

# %%
df_test = df_final[(df_final['Uses'].str.contains("HOTEL")) & (df_final['property_total_area'] <= 10000 )]

# %%
df_final["Floor Use"].value_counts()

# %%
largest_props = df_final["property_total_area"].sort_values()

# %%
use_group = df_final.groupby("Uses")["property_total_area"].sum().sort_values()

# %%
print(largest_props.to_string())

# %%
df_final.loc[72632]

# %%
df_final.loc[df_final["Uses"] == "APART / HOTEL, -"]

# %%
df.loc[df["Property Number"] == 447026.0]

# %%
print(largest_consumer.to_string())

# %%
elec_sa.loc[23224]

# %%
consumer_groups = elec_sa.groupby("Uses_Clean")["elec_demand_kwh"].sum().sort_values()

# %%
print(consumer_groups.to_string())

# %%
elec_sa["comm_peak_kw"].sort_values()

# %%
elec_sa.iloc[23246]

# %%
elec_sa.loc[elec_sa["small_area"] == "267044009"]
