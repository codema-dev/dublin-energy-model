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
from collections import defaultdict 
from pathlib import Path

from eppy import modeleditor
from eppy.modeleditor import IDF
import pandas as pd
```

```python
IDF.setiddname('/usr/local/bin/Energy+.idd')
epw_file = "IRL_Dublin.039690_IWEC.epw"
```

```python
archetype_dirpath = Path("archetypes")
```

```python
archetype_names = [
    "apartment_block_post.idf",
    "apartment_block_pre.idf",
    "bungalow_post.idf",
    "bungalow_pre.idf",
    "detatched_post.idf",
    "detatched_pre.idf",
    "mid_apt_post.idf",
    "mid_apt_pre.idf",
    "semi_d_post.idf",
    "semi_d_pre.idf",
    "terraced_post.idf",
    "terraced_pre.idf",
    "top_apt_post.idf",
    "top_apt_pre.idf"
]
```

```python
archetype_paths = [archetype_dirpath / name for name in archetype_names]
```

```python
for archetype_path in archetype_paths[:2]:
    
    idf = IDF(str(archetype_path))
    idf.epw = epw_file
    
    output_directory = f"design_days/{archetype_path.stem}"
    
    idf.run(
        output_directory=output_directory,
        readvars=True, # to convert eso output to csv
        design_day=True,
    )
```

```python
electricity_peaks = defaultdict()

for archetype_path in archetype_paths[:2]:
    
    output_directory = f"design_days/{archetype_path.stem}"
    
    electricity_peak = (
        pd.read_csv(f"{output_directory}/eplusmtr.csv")
        .loc[:, "Electricity:Facility [J](Hourly)"].max()
    )
    
    electricity_peaks[archetype_path.stem] = electricity_peak
```

```python
archetype_electricity_peaks = (
    pd.DataFrame.from_dict(archetype_peak_electricity_demands, orient="index")
    .reset_index()
    .rename(columns={"index": "name", 0: "peak_j_per_hour"})
    .assign(peak_kw=lambda df: df.peak_j_per_hour / 3600000)
    .drop(columns="peak_j_per_hour")
)
```

```python
archetype_electricity_peaks
```
