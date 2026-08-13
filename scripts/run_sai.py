from __future__ import annotations

import argparse
from pathlib import Path

from sai_utils import run_sai_for_region


def parse_args() -> argparse.Namespace:
    default_region = "02_02"
    default_olrrp_version = "v1-1"
    default_export_crs = "EPSG:4269"
    default_signals_csv_name = "CLRH_ontario_alteration.csv"

    parser = argparse.ArgumentParser(
        description="Calculate Streamflow Alteration Index (SAI_I and SAI_II) for one CLRH name code (SSDA_NM)."
    )
    parser.add_argument(
        "--region",
        type=str,
        default=default_region,
        help="Name code: SSDA_NM in CLRH",
    )
    parser.add_argument(
        "--olrrp-version",
        type=str,
        default=default_olrrp_version,
        help="OLRRP version string used in shapefile names, e.g., v2-0-1",
    )
    parser.add_argument(
        "--export-crs",
        type=str,
        default=default_export_crs,
        help="Output CRS, e.g., EPSG:4269. Use empty string to keep native CRS.",
    )
    parser.add_argument(
        "--signals-csv-name",
        type=str,
        default=default_signals_csv_name,
        help="Filename of the Ontario-wide alteration signals CSV in the data folder.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]

    run_sai_for_region(
        project_root=project_root,
    region=args.region.strip().upper(),
        olrrp_version=args.olrrp_version.strip(),
        export_crs=args.export_crs.strip(),
        signals_csv_name=args.signals_csv_name.strip(),
    )


if __name__ == "__main__":
    main()