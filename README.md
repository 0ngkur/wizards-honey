# Wizard's Honey v3.0 - Universal Security Suite

Advanced, AI-era web honeypot designed for high-interaction deception and proactive hardening of AI proxies (like 9router).

## System Architecture

The suite now operates in a **Dual-Mode** configuration, allowing it to adapt its personality based on the target environment:

- **STANDARD Mode**: Emulates a generic Linux/Apache environment with an IT maintenance portal, admin dashboards, and emergency terminals.
- **PROXY Mode**: Emulates an AI API Proxy (e.g., 9router), specifically targeting CVE-2026-5842 exploit attempts with high-fidelity bait.

## Key Features

- **Deep Packet Inspection (DPI)**: Analyzes AI payloads (JSON) for prompt injection strings, local file inclusion (LFI) attempts, and key exfiltration.
- **Wizard Shield**: An auto-patching CLI tool (`scripts/harden_proxy.py`) that injects hardware-bound encryption (HWID) into AI proxy source code.
- **SOC Alerting**: Real-time logging of security incidents to `logs/soc_alerts.json` with categorical threat levels.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launcher (Dual-Mode)**:
   Toggle the personality using the `HONEY_MODE` environment variable:

   - **For Standard Web Trap**:
     ```powershell
     $env:HONEY_MODE="STANDARD"; python app.py
     ```
   - **For AI Proxy Trap**:
     ```powershell
     $env:HONEY_MODE="PROXY"; python app.py
     ```

3. **Verify Status**:
   Access `http://localhost:5000/api/v1/health` to confirm the operational mode.

---
© 2024 Ikhtheir's DevLab | Secure by Deception.
