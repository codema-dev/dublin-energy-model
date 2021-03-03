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

# Eppy is a scripting language for EnergyPlus, used to run annual simulations and produce outputs from archetype idf files

```python
cd ..
```

```python
from eppy import modeleditor
from eppy.modeleditor import IDF
import pandas as pd
```

```python
IDF.setiddname('/usr/local/EnergyPlus-8-9-0/Energy+.idd')
```

### Weather file used is for Dublin, Ireland

```python
idf = IDF('data/resi_modelling/det_pre/detatched_pre.idf')
idf.epw = "data/resi_modelling/det_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/det_pre")
```

```python
df = pd.read_csv("data/resi_modelling/det_pre/eplusmtr.csv")
peak_demand_joule_det_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/det_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_det_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_det_pre = df3.iloc[16,1]
ann_heat_demand_kwh_det_pre = df3.iloc[16,5]
print(peak_demand_joule_det_pre, ann_energy_demand_kwh_det_pre, ann_elec_demand_kwh_det_pre, ann_heat_demand_kwh_det_pre)
```

### Hourly outputs here represent the sum of the entire hour

```python
idf = IDF('data/resi_modelling/det_post/detatched_post.idf')
idf.epw = "data/resi_modelling/det_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/det_post")
```

```python
df = pd.read_csv("data/resi_modelling/det_post/eplusmtr.csv")
peak_demand_joule_det_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/det_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_det_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_det_post = df3.iloc[16,1]
ann_heat_demand_kwh_det_post = df3.iloc[16,5]
print(peak_demand_joule_det_post, ann_energy_demand_kwh_det_post, ann_elec_demand_kwh_det_post, ann_heat_demand_kwh_det_post)
```

```python
idf = IDF('data/resi_modelling/semi_d_pre/semi_d_pre.idf')
idf.epw = "data/resi_modelling/semi_d_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/semid_pre")
```

```python
df = pd.read_csv("data/resi_modelling/semi_d_pre/eplusmtr.csv")
peak_demand_joule_semid_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/semi_d_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_semid_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_semid_pre = df3.iloc[16,1]
ann_heat_demand_kwh_semid_pre = df3.iloc[16,5]
print(peak_demand_joule_semid_pre, ann_energy_demand_kwh_semid_pre, ann_elec_demand_kwh_semid_pre, ann_heat_demand_kwh_semid_pre)
```

```python
idf = IDF('data/resi_modelling/semi_d_post/semi_d_post.idf')
idf.epw = "data/resi_modelling/semi_d_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/semid_post")
```

```python
df = pd.read_csv("data/resi_modelling/semi_d_post/eplusmtr.csv")
peak_demand_joule_semid_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/semi_d_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_semid_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_semid_post = df3.iloc[16,1]
ann_heat_demand_kwh_semid_post = df3.iloc[16,5]
print(peak_demand_joule_semid_post, ann_energy_demand_kwh_semid_post, ann_elec_demand_kwh_semid_post, ann_heat_demand_kwh_semid_post)
```

```python
idf = IDF('data/resi_modelling/terr_pre/terraced_pre.idf')
idf.epw = "data/resi_modelling/terr_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/terr_pre")
```

```python
df = pd.read_csv("data/resi_modelling/terr_pre/eplusmtr.csv")
peak_demand_joule_terr_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/terr_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_terr_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_terr_pre = df3.iloc[16,1]
ann_heat_demand_kwh_terr_pre = df3.iloc[16,5]
print(peak_demand_joule_terr_pre, ann_energy_demand_kwh_terr_pre, ann_elec_demand_kwh_terr_pre, ann_heat_demand_kwh_terr_pre)
```

```python
idf = IDF('data/resi_modelling/terr_post/terraced_post.idf')
idf.epw = "data/resi_modelling/terr_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/terr_post")
```

```python
df = pd.read_csv("data/resi_modelling/terr_post/eplusmtr.csv")
peak_demand_joule_terr_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/terr_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_terr_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_terr_post = df3.iloc[16,1]
ann_heat_demand_kwh_terr_post = df3.iloc[16,5]
print(peak_demand_joule_terr_post, ann_energy_demand_kwh_terr_post, ann_elec_demand_kwh_terr_post, ann_heat_demand_kwh_terr_post)
```

```python
idf = IDF('data/resi_modelling/mid_apt_pre/mid_apt_pre.idf')
idf.epw = "data/resi_modelling/mid_apt_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/mid_apt_pre")
```

```python
df = pd.read_csv("data/resi_modelling/mid_apt_pre/eplusmtr.csv")
peak_demand_joule_mid_apt_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/mid_apt_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_mid_apt_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_mid_apt_pre = df3.iloc[16,1]
ann_heat_demand_kwh_mid_apt_pre = df3.iloc[16,5]
print(peak_demand_joule_mid_apt_pre, ann_energy_demand_kwh_mid_apt_pre, ann_elec_demand_kwh_mid_apt_pre, ann_heat_demand_kwh_mid_apt_pre)
```

```python
idf = IDF('data/resi_modelling/mid_apt_post/mid_apt_post.idf')
idf.epw = "data/resi_modelling/mid_apt_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/mid_apt_post")
```

```python
df = pd.read_csv("data/resi_modelling/mid_apt_post/eplusmtr.csv")
peak_demand_joule_mid_apt_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/mid_apt_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_mid_apt_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_mid_apt_post = df3.iloc[16,1]
ann_heat_demand_kwh_mid_apt_post = df3.iloc[16,5]
print(peak_demand_joule_mid_apt_post, ann_energy_demand_kwh_mid_apt_post, ann_elec_demand_kwh_mid_apt_post, ann_heat_demand_kwh_mid_apt_post)
```

```python
idf = IDF('data/resi_modelling/top_apt_pre/top_apt_pre.idf')
idf.epw = "data/resi_modelling/top_apt_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/top_apt_pre")
```

```python
df = pd.read_csv("data/resi_modelling/top_apt_pre/eplusmtr.csv")
peak_demand_joule_top_apt_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/top_apt_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_top_apt_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_top_apt_pre = df3.iloc[16,1]
ann_heat_demand_kwh_top_apt_pre = df3.iloc[16,5]
print(peak_demand_joule_top_apt_pre, ann_energy_demand_kwh_top_apt_pre, ann_elec_demand_kwh_top_apt_pre, ann_heat_demand_kwh_top_apt_pre)
```

```python
idf = IDF('data/resi_modelling/top_apt_post/top_apt_post.idf')
idf.epw = "data/resi_modelling/top_apt_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/resi_modelling/top_apt_post")
```

```python
df = pd.read_csv("data/resi_modelling/top_apt_post/eplusmtr.csv")
peak_demand_joule_top_apt_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/resi_modelling/top_apt_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_top_apt_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_top_apt_post = df3.iloc[16,1]
ann_heat_demand_kwh_top_apt_post = df3.iloc[16,5]
print(peak_demand_joule_top_apt_post, ann_energy_demand_kwh_top_apt_post, ann_elec_demand_kwh_top_apt_post, ann_heat_demand_kwh_top_apt_post)
```

```python
peak_data = [['Detatched housepre', peak_demand_joule_det_pre, ann_energy_demand_kwh_det_pre, ann_elec_demand_kwh_det_pre, ann_heat_demand_kwh_det_pre], ['Detatched housepost', peak_demand_joule_det_post, ann_energy_demand_kwh_det_post, ann_elec_demand_kwh_det_post, ann_heat_demand_kwh_det_post], ['Semi detatched housepre', peak_demand_joule_semid_pre, ann_energy_demand_kwh_semid_pre, ann_elec_demand_kwh_semid_pre, ann_heat_demand_kwh_semid_pre],['Semi detatched housepost', peak_demand_joule_semid_post, ann_energy_demand_kwh_semid_post, ann_elec_demand_kwh_semid_post, ann_heat_demand_kwh_semid_post],['Terraced housepre', peak_demand_joule_terr_pre, ann_energy_demand_kwh_terr_pre, ann_elec_demand_kwh_terr_pre, ann_heat_demand_kwh_terr_pre], ['Terraced housepost', peak_demand_joule_terr_post, ann_energy_demand_kwh_terr_post, ann_elec_demand_kwh_terr_post, ann_heat_demand_kwh_terr_post], ['Apartmentpre', peak_demand_joule_mid_apt_pre, ann_energy_demand_kwh_mid_apt_pre, ann_elec_demand_kwh_mid_apt_pre, ann_heat_demand_kwh_mid_apt_pre],['Apartmentpost', peak_demand_joule_mid_apt_post, ann_energy_demand_kwh_mid_apt_post, ann_elec_demand_kwh_mid_apt_post, ann_heat_demand_kwh_mid_apt_post],['Top floor apt.pre', peak_demand_joule_top_apt_pre, ann_energy_demand_kwh_top_apt_pre, ann_elec_demand_kwh_top_apt_pre, ann_heat_demand_kwh_top_apt_pre],['Top floor apt.post', peak_demand_joule_top_apt_post, ann_energy_demand_kwh_top_apt_post, ann_elec_demand_kwh_top_apt_post, ann_heat_demand_kwh_top_apt_post], ] 
```

```python
df_peaks = pd.DataFrame(peak_data, columns = ['dwelling_type','peak_hourly_elec_demand(J)', "annual_energy_demand_kwh", "annual_elec_demand_kwh", "annual_heat_demand_kwh"]) 
```

```python
df_peaks
```

### Note that the hourly elec values in J are across an entire hour thus the conversion below

```python
df_peaks["peak_elec_demand(kW)"] = df_peaks["peak_hourly_elec_demand(J)"]/3600000
```

### Assume a power factor of 0.85

```python
df_peaks["peak_elec_demand(kVA)"] = df_peaks["peak_elec_demand(kW)"]*0.85
```

```python
df_peaks
```

```python
df_peaks.to_csv("data/interim/energy_demand_by_building_type_eppy.csv")
```

```python

```
