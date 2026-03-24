#!/usr/bin/env bash
set -e

MAINSail_DIR="/home/pi/mainsail"
BUILD_DIR="/home/pi/mainsail-afc-build"
REPO_URL="https://github.com/mainsail-crew/mainsail.git"

echo "[AFC] Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "[AFC] Cloning Mainsail master..."
git clone --depth=1 "$REPO_URL" "$BUILD_DIR"

echo "[AFC] Copying AFC overlay..."
cp -r mainsail-overlay/src "$BUILD_DIR/src"
cp -r mainsail-overlay/patches "$BUILD_DIR/patches"

echo "[AFC] Applying patches..."
cd "$BUILD_DIR"
patch -p1 < patches/register-afc-store.patch
patch -p1 < patches/register-afc-widget.patch
patch -p1 < patches/register-afc-events.patch

echo "[AFC] Installing dependencies..."
npm install

echo "[AFC] Building Mainsail..."
npm run build

echo "[AFC] Backing up existing Mainsail..."
if [ -d "$MAINSail_DIR" ]; then
  mv "$MAINSail_DIR" "${MAINSail_DIR}.backup.$(date +%Y%m%d-%H%M%S)"
fi

echo "[AFC] Deploying new Mainsail..."
mkdir -p "$MAINSail_DIR"
cp -r dist/* "$MAINSail_DIR/"

echo "[AFC] Restarting services..."
sudo systemctl restart moonraker
sudo systemctl restart klipper
sudo systemctl restart nginx

echo "[AFC] Installation complete."
