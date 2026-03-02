# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Termux Linux Desktop Setup — a bash automation script that installs and configures a full Linux desktop environment with GPU acceleration on Android phones via Termux and Termux-X11. No PC or root required.

The project is two files: `termux-linux-setup.sh` (the main script) and `README.md`.

## Running the Script

The script runs inside Termux on Android:
```bash
bash termux-linux-setup.sh
```
There is no build system, test suite, or linter. The script is interactive — it prompts the user to choose a desktop environment (XFCE4/LXQt/MATE/KDE Plasma) and optionally Wine.

All operations are logged to `~/termux-setup.log`.

## Architecture

### Script Flow (11 steps)

The script follows a linear installation pipeline:
1. **Environment detection** — GPU type (Adreno vs Mali/other via hardware properties), device info, user choices
2. **System update** — handles the libpcre/libandroid-selinux conflict that can kill Termux mid-install
3. **Repository setup** — adds `x11-repo` and `tur-repo`
4. **Termux-X11** — display server and XRandR
5. **Desktop environment** — installs chosen DE with appropriate components
6. **GPU drivers** — mesa-zink, vulkan loaders, and GPU-specific ICDs (freedreno for Adreno, swrast otherwise)
7. **Audio** — PulseAudio
8. **Applications** — Firefox, VLC, git, wget, curl, OpenSSH
9. **Python** — Python 3 + pip
10. **Wine (optional)** — Hangover Wine + Box64
11. **Launcher scripts** — creates `start-linux.sh`, `stop-linux.sh`, GPU config, desktop shortcuts

### Key Design Decisions

- **No `set -e` or `set -u`**: Intentionally avoided. `set -e` silently kills the script on any failed package install; `set -u` crashes on legitimately empty Termux variables. Only `set -o pipefail` is used.
- **`safe_install_pkg` function**: Checks if a package is already installed, reads `Conflicts` from `apt-cache` before installing, and prevents silent script exits from package conflicts (critical for vulkan-loader-android vs vulkan-loader-generic).
- **GPU detection via hardware properties**: Uses `ro.hardware.egl` and `ro.hardware` instead of brand name to correctly identify Adreno (Turnip/Zink) vs Mali/PowerVR (SwRast) GPUs.
- **Dynamic paths**: Uses `$PREFIX` and `$HOME` instead of hardcoded Termux paths to support non-standard installs.

### Generated Files

The script creates these on the user's device:
- `~/.config/linux-gpu.sh` — Mesa/GPU environment variables
- `~/start-linux.sh` / `~/stop-linux.sh` — session management
- `~/.config/autostart/plank.desktop` — dock autostart (XFCE4/MATE)
- `~/.config/plasma-workspace/env/xdg_fix.sh` — KDE Plasma XDG fix
- `~/Desktop/*.desktop` — application shortcuts

## Conventions

- Shebang targets Termux: `#!/data/data/com.termux/files/usr/bin/bash`
- Color-coded output: GREEN=success, RED=error, YELLOW=warning, CYAN=info
- All package installs should go through `safe_install_pkg` to handle conflicts
- Desktop-environment-specific logic branches on `$DE_CHOICE` (1=XFCE4, 2=LXQt, 3=MATE, 4=KDE)
