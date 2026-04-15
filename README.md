# Wizard's Honey (v2.4)

Internal staging portal for LuminaTech development workflows. This repository contains the source for the central management dashboard and emergency debug consoles used in the `staging-srv-04` cluster.

## Architecture

- **Core**: Flask-based microservice.
- **Monitoring**: Integrated request auditing (`services/guard.py`).
- **Telemetry**: Real-time system stat generation (`services/generator.py`).
- **Deception**: High-fidelity 0-day emulation for **9router v0.3.47** (CVE-2026-5842).

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Standard Launch:
   ```bash
   python app.py
   ```

3. Environment Configuration:
   The application uses a `.env` file for high-level cluster configuration. Ensure this file is synced with the production vault before deployment.

## Security Warning

This is an internal tool. Do not expose this service to the public internet without proper VPC peering and VPN authentication. The emergency terminal (`/admin/terminal`) bypasses standard SSO for disaster recovery purposes.

---
© 2024 LuminaTech Infrastructure Team
