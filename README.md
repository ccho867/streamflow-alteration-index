# streamflow-alteration-index

Python tools for calculating the Streamflow Alteration Index (SAI) from OLRRP routing products and alteration signal tables.

## Repository structure

```text
streamflow-alteration-index/
├── data/
├── results/
└── scripts/
```

## Data layout

Place each OLRRP region under:

```text
data/OLRRPv2/<REGION>/
```

Example for `SE`:

```text
data/OLRRPv2/SE/finalcat_info_v2-0-1.shp
data/OLRRPv2/SE/finalcat_info_riv_v2-0-1.shp
```

Place the Ontario-wide alteration signal table at:

```text
data/ontario_alteration_signals.csv
```

## Scripts

- `scripts/run_sai.py` — main driver
- `scripts/sai_utils.py` — library functions

## Usage

From the repository root:

```bash
python scripts/run_sai.py --region SE
```

To run another region:

```bash
python scripts/run_sai.py --region SW
python scripts/run_sai.py --region NE
```

## Output

Results are written to:

```text
results/<REGION>/
```

## Notes

- The scripts are general for all regions.
- The main driver controls which single region is processed.
- The river shapefile path is retained in the project structure, although it is not required for the current SAI calculation workflow.

## Citation

If you use the **SAI v1.0 dataset** associated with this repository, please cite:

Shen, H., Tolson, B., Craig, J., Metcalfe, R. A., Romero-Cuellar, J., & Luce, J. (2026). *Streamflow Alteration Index (SAI) v1.0 Database for Ontario, Canada* (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.19547932

If **OLRRP v2** is used as the routing product input to this workflow, please also cite:

Shen, H., Han, M., Tolson, B., & Metcalfe, R. A. (2024). *The Ontario Lake and River Routing Product Version 2 (OLRRP V2)* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14225103
