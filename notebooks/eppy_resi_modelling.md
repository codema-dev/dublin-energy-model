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
from eppy import modeleditor
from eppy.modeleditor import IDF
import pandas as pd
```

```python
IDF.setiddname('/usr/local/EnergyPlus-8-9-0/Energy+.idd')
```

```python
idf = IDF('data/det_pre/detatched_pre.idf')
idf.epw = "data/det_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/det_pre")
```

```python
df = pd.read_csv("data/det_pre/eplusmtr.csv")
peak_demand_joule_det_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/det_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_det_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_det_pre = df3.iloc[16,1]
ann_heat_demand_kwh_det_pre = df3.iloc[16,5]
print(peak_demand_joule_det_pre, ann_energy_demand_kwh_det_pre, ann_elec_demand_kwh_det_pre, ann_heat_demand_kwh_det_pre)
```

```python
idf = IDF('data/det_post/detatched_post.idf')
idf.epw = "data/det_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/det_post")
```

```python
df = pd.read_csv("data/det_post/eplusmtr.csv")
peak_demand_joule_det_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/det_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_det_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_det_post = df3.iloc[16,1]
ann_heat_demand_kwh_det_post = df3.iloc[16,5]
print(peak_demand_joule_det_post, ann_energy_demand_kwh_det_post, ann_elec_demand_kwh_det_post, ann_heat_demand_kwh_det_post)
```

```python
idf = IDF('data/semi_d_pre/semi_d_pre.idf')
idf.epw = "data/semi_d_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/semid_pre")
```

```python
df = pd.read_csv("data/semi_d_pre/eplusmtr.csv")
peak_demand_joule_semid_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/semi_d_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_semid_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_semid_pre = df3.iloc[16,1]
ann_heat_demand_kwh_semid_pre = df3.iloc[16,5]
print(peak_demand_joule_semid_pre, ann_energy_demand_kwh_semid_pre, ann_elec_demand_kwh_semid_pre, ann_heat_demand_kwh_semid_pre)
```

```python
idf = IDF('data/semi_d_post/semi_d_post.idf')
idf.epw = "data/semi_d_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/semid_post")
```

```python
df = pd.read_csv("data/semi_d_post/eplusmtr.csv")
peak_demand_joule_semid_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/semi_d_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_semid_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_semid_post = df3.iloc[16,1]
ann_heat_demand_kwh_semid_post = df3.iloc[16,5]
print(peak_demand_joule_semid_post, ann_energy_demand_kwh_semid_post, ann_elec_demand_kwh_semid_post, ann_heat_demand_kwh_semid_post)
```

```python
idf = IDF('data/terr_pre/terraced_pre.idf')
idf.epw = "data/terr_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/terr_pre")
```

```python
df = pd.read_csv("data/terr_pre/eplusmtr.csv")
peak_demand_joule_terr_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/terr_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_terr_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_terr_pre = df3.iloc[16,1]
ann_heat_demand_kwh_terr_pre = df3.iloc[16,5]
print(peak_demand_joule_terr_pre, ann_energy_demand_kwh_terr_pre, ann_elec_demand_kwh_terr_pre, ann_heat_demand_kwh_terr_pre)
```

```python
idf = IDF('data/terr_post/terraced_post.idf')
idf.epw = "data/terr_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/terr_post")
```

```python
df = pd.read_csv("data/terr_post/eplusmtr.csv")
peak_demand_joule_terr_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/terr_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_terr_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_terr_post = df3.iloc[16,1]
ann_heat_demand_kwh_terr_post = df3.iloc[16,5]
print(peak_demand_joule_terr_post, ann_energy_demand_kwh_terr_post, ann_elec_demand_kwh_terr_post, ann_heat_demand_kwh_terr_post)
```

```python
idf = IDF('data/mid_apt_pre/mid_apt_pre.idf')
idf.epw = "data/mid_apt_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/mid_apt_pre")
```

```python
df = pd.read_csv("data/mid_apt_pre/eplusmtr.csv")
peak_demand_joule_mid_apt_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/mid_apt_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_mid_apt_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_mid_apt_pre = df3.iloc[16,1]
ann_heat_demand_kwh_mid_apt_pre = df3.iloc[16,5]
print(peak_demand_joule_mid_apt_pre, ann_energy_demand_kwh_mid_apt_pre, ann_elec_demand_kwh_mid_apt_pre, ann_heat_demand_kwh_mid_apt_pre)
```

```python
idf = IDF('data/mid_apt_post/mid_apt_post.idf')
idf.epw = "data/mid_apt_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/mid_apt_post")
```

```python
df = pd.read_csv("data/mid_apt_post/eplusmtr.csv")
peak_demand_joule_mid_apt_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/mid_apt_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_mid_apt_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_mid_apt_post = df3.iloc[16,1]
ann_heat_demand_kwh_mid_apt_post = df3.iloc[16,5]
print(peak_demand_joule_mid_apt_post, ann_energy_demand_kwh_mid_apt_post, ann_elec_demand_kwh_mid_apt_post, ann_heat_demand_kwh_mid_apt_post)
```

```python
idf = IDF('data/top_apt_pre/top_apt_pre.idf')
idf.epw = "data/top_apt_pre/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/top_apt_pre")
```

```python
df = pd.read_csv("data/top_apt_pre/eplusmtr.csv")
peak_demand_joule_top_apt_pre = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/top_apt_pre/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_top_apt_pre = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_top_apt_pre = df3.iloc[16,1]
ann_heat_demand_kwh_top_apt_pre = df3.iloc[16,5]
print(peak_demand_joule_top_apt_pre, ann_energy_demand_kwh_top_apt_pre, ann_elec_demand_kwh_top_apt_pre, ann_heat_demand_kwh_top_apt_pre)
```

```python
idf = IDF('data/top_apt_post/top_apt_post.idf')
idf.epw = "data/top_apt_post/IRL_Dublin.039690_IWEC.epw"
idf.run(expandobjects=True, readvars=True, output_directory="data/top_apt_post")
```

```python
df = pd.read_csv("data/top_apt_post/eplusmtr.csv")
peak_demand_joule_top_apt_post = df["Electricity:Facility [J](Hourly)"].max()
df2 = pd.read_html("data/top_apt_post/eplustbl.htm")
df_e = pd.DataFrame(df2[0])
ann_energy_demand_kwh_top_apt_post = df_e.iloc[1,1]
df3 = pd.DataFrame(df2[3])
ann_elec_demand_kwh_top_apt_post = df3.iloc[16,1]
ann_heat_demand_kwh_top_apt_post = df3.iloc[16,5]
print(peak_demand_joule_top_apt_post, ann_energy_demand_kwh_top_apt_post, ann_elec_demand_kwh_top_apt_post, ann_heat_demand_kwh_top_apt_post)
```

```python
peak_demand_joule_top_apt_post
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

```python
df_peaks["peak_elec_demand(kW)"] = df_peaks["peak_hourly_elec_demand(J)"]/3600000
```

```python
df_peaks["peak_elec_demand(kVA)"] = df_peaks["peak_elec_demand(kW)"]*0.85
```

```python
df_peaks
```

```python
df_peaks.to_csv("data/outputs/energy_demand_by_building_type.csv")
```

```python

```
