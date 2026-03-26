# Arts & Theology Native Circos

This folder builds a strict native Circos diagram from the row-level dataset.

Logic used:

- Major side uses only rows where `Major Cluster = ARTS, LANGUAGES & THEOLOGY`
- Left half is split across the individual majors in that cluster
- Major ordering is grouped by the three major subclusters:
  - `Arts & Theology`
  - `English & Writing`
  - `Languages`
- Right half is split across broad career clusters derived from each row's `Job Title`
- Each ribbon represents one row/person:
  - `Program Name/Major -> Job Title -> career large cluster`
- Only Arts & Theology majors have visible ribbons

Files:

- `build_native_circos.py` generates the native Circos inputs
- `karyotype.txt` defines all visible segments
- `links.txt` defines one ribbon per row
- `circos.conf` defines the layout and styling

Build the data files:

```powershell
python .\major_industry_circos_draft1\arts_theology_native_circos\build_native_circos.py
```

Render with Circos:

```powershell
powershell -ExecutionPolicy Bypass -File .\circos_windows\run_circos.ps1 -Config .\major_industry_circos_draft1\arts_theology_native_circos\circos.conf
```
