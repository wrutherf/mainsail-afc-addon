# Mainsail AFC Add-on

This repository provides an AFC/AMS-style add-on for Mainsail (master branch) including:

- A Moonraker AFC backend plugin
- A Mainsail AFC widget
- A Pinia store module
- Patch-based integration
- Automated installer for KIAUH-based systems

## Installation

SSH into your printer and run:

```bash
git clone https://github.com/<your-username>/mainsail-afc-addon.git
cd mainsail-afc-addon
chmod +x install.sh
./install.sh
