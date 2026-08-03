# SCD to IDS Rule Generation (Prototype)

A small proof-of-concept exploring the idea of automatically generating IDS rules from an IEC 61850 Substation Configuration Description (SCD) file.

Instead of manually maintaining IDS rules whenever the substation configuration changes, this prototype parses the SCD, builds an intermediate asset model, and uses that model to generate basic Suricata and Zeek rule templates.

---

## Motivation

The SCD file already contains the information needed to describe the network:

- Which devices (IEDs) exist
- Their network addresses (IP/MAC)
- Their communication configuration
- GOOSE publishers and their associated APPIDs

Rather than generating IDS rules directly from the XML, this prototype first converts the SCD into an intermediate **AssetModel**.

This separation keeps the parser independent from the rule generators and allows the same asset model to be reused for different outputs.

```
SCD File
    │
    ▼
 parser.py
    │
    ▼
 AssetModel
    │
    ├──────────────┐
    ▼              ▼
Suricata       Zeek
 Rule Gen      Rule Gen
```

This design also makes it possible to extend the project later with additional outputs such as NetBox asset imports or network visualizations.

---

## Project Structure

```
IDS/
├── sample_data/
│   └── example.scd
│
├── src/
│   ├── parser.py
│   ├── asset_model.py
│   ├── rulegen.py
│   └── main.py
│
├── output/
│   ├── asset_model.json
│   ├── generated_suricata.rules
│   └── generated_zeek.zeek
│
└── tests/
    └── test_parser.py
```

---

## Pipeline

### 1. Parse the SCD

The parser extracts:

- IEDs and Access Points
- IP addresses
- MAC addresses
- GOOSE publishers
- APPIDs
- VLAN information

---

### 2. Build the Asset Model

The extracted information is converted into a simple internal representation.

The AssetModel acts as a clean description of the substation assets and their communication information, without being tied to XML or to a specific IDS engine.

---

### 3. Generate IDS Rules

The AssetModel is then used to generate outputs for two different IDS engines.

### Suricata

Suricata is signature-based.

The prototype generates:

- Known asset IP list
- Rule to detect unknown IP addresses
- Rule to detect unexpected GOOSE APPIDs

---

### Zeek

Zeek is event-driven.

Instead of generating many individual rules, the prototype generates:

- one reusable Zeek script
- populated asset tables derived from the AssetModel

The detection logic remains the same while only the asset data changes for different substations.

---

## Running the Prototype

From the `src` directory:

```bash
python3 main.py ../sample_data/example.scd --out-dir ../output
```

Generated files are written to:

```
output/
```

---

## Running the Tests

```
python3 tests/test_parser.py
```

The tests verify that the parser extracts the expected assets from the sample SCD file.

---

## Validation

### Suricata

The generated rules were validated using:

```bash
suricata -T
```

The rules loaded successfully without syntax errors.

### Zeek

The Zeek script was generated from the AssetModel but was not validated against a live Zeek/Malcolm installation.

The GOOSE event handler is intentionally left as a placeholder because the exact event exposed by the Malcolm/Zeek setup was not available during development.

---

## Current Scope

This prototype currently focuses on:

- Asset extraction from SCD
- GOOSE publisher extraction
- Asset model generation
- Basic Suricata rule generation
- Basic Zeek rule generation

---

## Future Work

Possible extensions include:

- Parsing GOOSE subscriber information (ExtRef)
- MMS and Report Control Blocks
- Sampled Values (SV)
- Integration with NetBox
- Validation against a complete Malcolm deployment
- Additional IDS rules based on the generated asset model

---

## Notes

This repository is intended as a small proof-of-concept to explore one possible pipeline for transforming an IEC 61850 SCD file into IDS configuration.

The focus was on understanding the overall architecture—from SCD parsing, to asset modelling, to IDS rule generation—rather than implementing a complete production-ready solution.