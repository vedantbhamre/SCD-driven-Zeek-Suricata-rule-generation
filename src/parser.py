"""
Parses an IEC 61850 SCD (Substation Configuration Description) file
and extracts the information needed to build the AssetModel.

For this prototype, the parser focuses on:
  1. Network-connected devices (IEDs and AccessPoints)
  2. GOOSE publishers and their communication details

Other parts of the SCD, such as reports or sampled values, are not
handled here.
"""

from __future__ import annotations
import xml.etree.ElementTree as ET
from asset_model import AssetModel, Asset, GooseFlow

# Get the XML namespace from the root element so the parser works
# with different SCD namespace versions.
def _get_ns(root: ET.Element) -> dict:
    if root.tag.startswith("{"):
        uri = root.tag[1:].split("}")[0]
        return {"scl": uri}
    return {"scl": ""}


def parse_scd(path: str) -> AssetModel:
    tree = ET.parse(path)
    root = tree.getroot()
    ns = _get_ns(root)

    model = AssetModel()

    # Step 1: addresses, from Communication/SubNetwork/ConnectedAP
    
    # Collect some additional information about each IED that we'll combine with the communication information later.
    ied_meta = {}
    for ied in root.findall("scl:IED", ns):
        ied_meta[ied.get("name")] = {
            "type": ied.get("type"),
            "manufacturer": ied.get("manufacturer"),
            "desc": ied.get("desc"),
        }

    goose_publishers = {}  # (ied_name, ldInst, cbName) -> control block name, for cross-ref

    for ied in root.findall("scl:IED", ns):
        ied_name = ied.get("name")
        for gse_control in ied.findall(".//scl:GSEControl", ns):
            # find the enclosing LDevice inst so we can match it to the
            # <GSE ldInst="..." cbName="..."> in the Communication section
            ldevice = None
            for ld in ied.findall(".//scl:LDevice", ns):
                if gse_control in ld.iter():
                    ldevice = ld
                    break
            ld_inst = ldevice.get("inst") if ldevice is not None else None
            cb_name = gse_control.get("name")
            goose_publishers[(ied_name, ld_inst, cb_name)] = cb_name

    for subnet in root.findall(".//scl:Communication/scl:SubNetwork", ns):
        for cap in subnet.findall("scl:ConnectedAP", ns):
            ied_name = cap.get("iedName")
            ap_name = cap.get("apName")

            ip, subnet_mask, mac = None, None, None
            addr = cap.find("scl:Address", ns)
            if addr is not None:
                for p in addr.findall("scl:P", ns):
                    ptype = p.get("type")
                    if ptype == "IP":
                        ip = p.text
                    elif ptype == "IP-SUBNET":
                        subnet_mask = p.text
                    elif ptype == "MAC-Address":
                        mac = p.text

            meta = ied_meta.get(ied_name, {})
            asset = Asset(
                ied_name=ied_name,
                ap_name=ap_name,
                ip=ip,
                mac=mac,
                subnet=subnet_mask,
                ied_type=meta.get("type"),
                manufacturer=meta.get("manufacturer"),
                description=meta.get("desc"),
            )
            model.add_asset(asset)

            # Step 2: GOOSE flows, from <GSE> blocks under the same ConnectedAP
            
            for gse in cap.findall("scl:GSE", ns):
                ld_inst = gse.get("ldInst")
                cb_name = gse.get("cbName")

                dst_mac, appid, vlan = None, None, None
                gse_addr = gse.find("scl:Address", ns)
                if gse_addr is not None:
                    for p in gse_addr.findall("scl:P", ns):
                        ptype = p.get("type")
                        if ptype == "MAC-Address":
                            dst_mac = p.text
                        elif ptype == "APPID":
                            appid = p.text
                        elif ptype == "VLAN-ID":
                            vlan = p.text

                flow = GooseFlow(
                    publisher_asset_id=asset.id,
                    control_block=cb_name,
                    dst_mac=dst_mac,
                    appid=appid,
                    vlan_id=vlan,
                )
                model.add_goose_flow(flow)

    return model


if __name__ == "__main__":
    import sys
    scd_path = sys.argv[1] if len(sys.argv) > 1 else "../sample_data/example.scd"
    m = parse_scd(scd_path)
    print(m.summary())
