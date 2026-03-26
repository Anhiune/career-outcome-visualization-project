# Circos Setup On This Windows Machine

This project already has most of what we need:

- Perl is installed at `C:\Strawberry\perl\bin\perl.exe`
- Circos is installed at `C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10`

## 1. What Circos needs on Windows

1. Install Strawberry Perl.
2. Download and extract the Circos archive.
3. Run Circos through Perl, not by double-clicking `bin\circos`.

The command format on Windows is:

```powershell
perl C:\path\to\circos\bin\circos -conf C:\path\to\circos.conf
```

## 2. If you ever need to install the Perl modules manually

Open PowerShell and run:

```powershell
cpanm Config::General GD List::MoreUtils Math::Round Math::VecStat Params::Validate Readonly Regexp::Common Text::Format
```

Those are the common Circos dependencies referenced by the installed copy on this machine.

## 3. Render the portable example in this repo

From the project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\circos_windows\run_circos.ps1
```

That renders:

`major_industry_circos_draft1\portable_example\portable_major_industry.png`

## 4. Render a different config

```powershell
powershell -ExecutionPolicy Bypass -File .\circos_windows\run_circos.ps1 -Config .\path\to\circos.conf
```

You can also override the output location:

```powershell
powershell -ExecutionPolicy Bypass -File .\circos_windows\run_circos.ps1 -Config .\path\to\circos.conf -OutputDir .\renders -OutputFile example.png
```

## 5. How this example maps to the diagram style you showed

- `karyotype.txt` defines the arc segments around the circle
- `links.txt` defines the ribbons between source and destination groups
- `colors.conf` defines the palette
- `circos.conf` controls spacing, label position, ribbon styling, and image size

That image style is a ribbon-style Circos layout: category blocks around the perimeter, with weighted ribbons connecting majors to industries.
