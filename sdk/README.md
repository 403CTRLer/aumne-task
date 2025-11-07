# Python SDK Generation

The SDK is generated from the FastAPI OpenAPI specification using the [OpenAPI Generator CLI](https://openapi-generator.tech/).

## Prerequisites

- Java 11+
- OpenAPI Generator CLI jar or Docker (see scripts below)

## Generate the SDK

Two helper scripts are provided:

### PowerShell

```powershell
./scripts/generate-sdk.ps1
```

### Bash

```bash
./scripts/generate-sdk.sh
```

Both scripts download the OpenAPI spec from a running FastAPI instance on `http://localhost:8000`, then run the official generator to produce a Python client SDK inside `sdk/python-client`.

## Sample Usage

After generating the SDK, install it in editable mode and run the sample script:

```bash
pip install -e sdk/python-client
python sdk/sample_usage.py
```

This script demonstrates creating, listing, and canceling appointments through the SDK layer.

