"""
Basic tests for the SCD parser and rule generation.

Run with:
    python3 -m pytest tests/

or

    python3 tests/test_parser.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from parser import parse_scd
from rulegen import to_suricata, to_zeek

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "sample_data", "example.scd")


def test_parses_all_assets():
    model = parse_scd(SAMPLE)
    assert len(model.assets) == 4
    names = {a.ied_name for a in model.assets}
    assert names == {"ProtRelay1", "ProtRelay2", "BayController1", "StationHMI"}


def test_asset_addresses_extracted():
    model = parse_scd(SAMPLE)
    relay1 = model.get_asset("ProtRelay1.P1")
    assert relay1 is not None
    assert relay1.ip == "192.168.10.11"
    assert relay1.mac == "00:0C:CD:01:00:11"


def test_goose_flows_extracted():
    model = parse_scd(SAMPLE)
    assert len(model.goose_flows) == 2
    appids = {f.appid for f in model.goose_flows}
    assert appids == {"1001", "1002"}


def test_suricata_output_has_expected_rule_count():
    model = parse_scd(SAMPLE)
    out = to_suricata(model)
    # 1 "unauthorized device" rule + 1 rule per GOOSE flow (2)
    assert out.count("alert ip") == 3


def test_zeek_output_contains_all_known_ips():
    model = parse_scd(SAMPLE)
    out = to_zeek(model)
    for ip in model.known_ips():
        assert ip in out


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
    print(f"\n{len(tests)} tests passed.")
