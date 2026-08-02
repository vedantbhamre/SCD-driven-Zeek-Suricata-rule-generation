"""
Defines the data model used by the project after parsing the SCD file.

The parser extracts information from the XML and stores it in this
AssetModel. The rule generators then use this model to generate
Suricata or Zeek rules.

Keeping this separate from the XML parser makes it easier to reuse the
same asset information for different outputs in the future, such as
IDS rules, asset inventories or network visualizations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class Asset:
    #Represents one network device extracted from the SCD
    ied_name: str
    ap_name: str
    ip: Optional[str] = None
    mac: Optional[str] = None
    subnet: Optional[str] = None
    ied_type: Optional[str] = None
    manufacturer: Optional[str] = None
    description: Optional[str] = None

    @property
    def id(self) -> str:
        #Unique identifier for this asset.
        return f"{self.ied_name}.{self.ap_name}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ied_name": self.ied_name,
            "ap_name": self.ap_name,
            "ip": self.ip,
            "mac": self.mac,
            "subnet": self.subnet,
            "ied_type": self.ied_type,
            "manufacturer": self.manufacturer,
            "description": self.description,
        }


@dataclass
class GooseFlow:
    """
    Represents a GOOSE message publisher extracted from the SCD.

    For this prototype, only the publishing information is stored.
    Subscriber information is not included because it requires parsing
    additional subscription data.
    """
    publisher_asset_id: str
    control_block: str
    dst_mac: Optional[str] = None
    appid: Optional[str] = None
    vlan_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "publisher_asset_id": self.publisher_asset_id,
            "control_block": self.control_block,
            "dst_mac": self.dst_mac,
            "appid": self.appid,
            "vlan_id": self.vlan_id,
        }


@dataclass
class AssetModel:
    #Stores all assets and GOOSE information extracted from one SCD file.
    assets: list[Asset] = field(default_factory=list)
    goose_flows: list[GooseFlow] = field(default_factory=list)

    def add_asset(self, asset: Asset) -> None:
        self.assets.append(asset)

    def add_goose_flow(self, flow: GooseFlow) -> None:
        self.goose_flows.append(flow)

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        for a in self.assets:
            if a.id == asset_id:
                return a
        return None

    def known_ips(self) -> set[str]:
        return {a.ip for a in self.assets if a.ip}

    def known_macs(self) -> set[str]:
        return {a.mac for a in self.assets if a.mac}

    def to_dict(self) -> dict:
        return {
            "assets": [a.to_dict() for a in self.assets],
            "goose_flows": [f.to_dict() for f in self.goose_flows],
        }

    def to_json(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def summary(self) -> str:
        lines = [f"Assets: {len(self.assets)}", f"GOOSE flows: {len(self.goose_flows)}", ""]
        for a in self.assets:
            lines.append(f"  - {a.id:30s} ip={a.ip or '-':16s} mac={a.mac or '-'}  ({a.ied_type or 'unknown type'})")
        if self.goose_flows:
            lines.append("")
            lines.append("GOOSE flows:")
            for gf in self.goose_flows:
                lines.append(
                    f"  - {gf.publisher_asset_id} -> {gf.control_block} "
                    f"dst_mac={gf.dst_mac} appid={gf.appid} vlan={gf.vlan_id}"
                )
        return "\n".join(lines)
