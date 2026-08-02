"""
Main entry point for the prototype.

Reads an IEC 61850 SCD file, builds the asset model, and generates
Suricata and Zeek rule files.

Usage:
    python3 main.py <path-to-scd> [--out-dir output/]
"""

import argparse
import os

from parser import parse_scd
from rulegen import to_suricata, to_zeek


def main():
    ap = argparse.ArgumentParser(description="Generate Zeek/Suricata rules from an IEC 61850 SCD file.")
    ap.add_argument("scd_path", help="Path to the SCD XML file")
    ap.add_argument("--out-dir", default="../output", help="Directory to write generated files to")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    print(f"[1/3] Parsing SCD: {args.scd_path}")
    model = parse_scd(args.scd_path)
    print(model.summary())

    model_path = os.path.join(args.out_dir, "asset_model.json")
    model.to_json(model_path)
    print(f"\n[2/3] Wrote asset model -> {model_path}")

    suricata_path = os.path.join(args.out_dir, "generated_suricata.rules")
    with open(suricata_path, "w") as f:
        f.write(to_suricata(model))
    print(f"[3/3] Wrote Suricata rules -> {suricata_path}")

    zeek_path = os.path.join(args.out_dir, "generated_zeek.zeek")
    with open(zeek_path, "w") as f:
        f.write(to_zeek(model))
    print(f"       Wrote Zeek script   -> {zeek_path}")


if __name__ == "__main__":
    main()
