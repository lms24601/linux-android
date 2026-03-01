# Termux Linux Desktop Setup

Run a **full Linux desktop environment on your Android phone** — with hardware GPU acceleration, audio, a web browser, and optional Windows app support — using [Termux](https://termux.dev) and [Termux-X11](https://github.com/termux/termux-x11). No PC required.

> This script was created to accompany a YouTube video walkthrough. If you're following along, timestamps are referenced in the [video description](#).

---

## What This Does

The script automates the entire process of:

1. Setting up a Linux desktop environment (you choose which one)
2. Enabling GPU hardware acceleration for smooth graphics
3. Installing a display server so your desktop appears on screen
4. Installing apps like Firefox and VLC
5. Setting up Python 3
6. Optionally installing Wine to run Windows applications

Everything runs **natively on your Android phone** — no emulation, no PC, no cloud.

---

## Requirements

### Hardware
- Android phone with an **arm64 (64-bit)** processor
- **3 GB+ RAM** recommended (4 GB+ for KDE Plasma)
- **5–10 GB** of free storage (more if you install Wine)
- A **Qualcomm Snapdragon** chip is ideal — it enables the best GPU acceleration (Turnip/Adreno). The script still works on Mali/other GPUs but performance will differ.

### Software
| App | Where to Get It |
|---|---|
| **Termux** | [F-Droid](https://f-droid.org/en/packages/com.termux/) — **do not use the Play Store version, it is outdated** |
| **Termux-X11** | [GitHub Releases](https://github.com/termux/termux-x11/releases) — download the latest `.apk` |

> **Note on rooting / custom ROMs:** This script works on stock Android too, but the video demonstrates it running on **LineageOS** on a OnePlus 5T. Rooting is not required by the script itself.

---

## Desktop Environments — Which One to Choose?

The script will ask you to pick a desktop. Here's a quick guide:

| # | Desktop | Best For | Resource Usage |
|---|---|---|---|
| 1 | **XFCE4** *(default)* | Most users. Familiar, fast, has a macOS-style dock | Low–Medium |
| 2 | **LXQt** | Old or low-RAM phones (2–3 GB) | Very Low |
| 3 | **MATE** | Classic desktop feel, moderate power | Medium |
| 4 | **KDE Plasma** | Powerful phones only — Windows 11 style | High |

If you're unsure, go with **XFCE4**.

---

## Installation

### Step 1 — Install the required apps

Install **Termux** from F-Droid and **Termux-X11** from GitHub (links above). Do not use the Play Store version of Termux.

### Step 2 — Open Termux and download the script

```bash
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/termux-linux-setup.sh
chmod +x termux-linux-setup.sh
```

> Replace `YOUR_USERNAME/YOUR_REPO` with your actual GitHub path.

### Step 3 — Run the script

```bash
bash termux-linux-setup.sh
```

The script will:
- Detect your device and GPU automatically
- Ask you to choose a desktop environment
- Ask if you want Wine (Windows app support) — this is optional
- Install everything and create startup/stop scripts

Installation takes **10–30 minutes** depending on your internet speed and phone speed. A full log is saved to `~/termux-setup.log` if anything goes wrong.

### Step 4 — Start your desktop

Once installation finishes:

```bash
bash ~/start-linux.sh
```

Then **open the Termux-X11 app** on your phone. Your Linux desktop will appear.

To stop the desktop:

```bash
bash ~/stop-linux.sh
```

---

## What Gets Installed

| Component | Details |
|---|---|
| **Termux-X11** | Display server — renders your desktop |
| **Desktop Environment** | Your choice: XFCE4, LXQt, MATE, or KDE |
| **Mesa / Zink** | OpenGL via Vulkan — enables GPU-accelerated graphics |
| **Turnip driver** | Qualcomm Adreno open-source Vulkan driver (if detected) |
| **PulseAudio** | Audio server — enables sound in apps |
| **Firefox** | Full desktop web browser |
| **VLC** | Video and audio player |
| **Git, wget, curl** | Standard developer tools |
| **Python 3 + pip** | Python runtime and package manager |
| **Wine** *(optional)* | Run Windows x86 apps via Hangover + Box64 |

---

## GPU Acceleration — How It Works

The script detects your GPU automatically:

- **Qualcomm Adreno (Snapdragon phones):** Uses the open-source **Turnip** Vulkan driver + **Zink** (OpenGL on top of Vulkan). This gives near-native GPU performance.
- **Mali / Other GPUs:** Falls back to **Zink native Vulkan**. Performance is functional but lighter desktops (XFCE4, LXQt) are strongly recommended.

The GPU environment is saved in `~/.config/linux-gpu.sh` and is loaded automatically every time you run `start-linux.sh`. You can edit that file if you need to tweak Mesa flags.

---

## Windows App Support (Wine)

If you chose to install Wine, it uses the **Hangover** fork of Wine together with **Box64** to translate Windows x86 calls to ARM64. This is not perfect compatibility — simple apps and tools tend to work, heavier software like games or complex installers may not.

To configure Wine after installation, run `winecfg` in your desktop terminal or click the **Wine Config** shortcut on your desktop.

---

## Troubleshooting

**Desktop doesn't appear after running start-linux.sh**
Open the Termux-X11 app manually after running the script. The desktop renders inside that app, not in Termux itself.

**Black screen in Termux-X11**
Try stopping (`stop-linux.sh`) and starting again. On first boot KDE Plasma may take 20–30 seconds longer than other desktops.

**Package install failures**
Check `~/termux-setup.log` for details. Most failures are network timeouts — just re-run the script, Termux's package manager is idempotent and will skip already-installed packages.

**Audio not working**
PulseAudio sometimes needs a moment to initialize. Wait 5–10 seconds after the desktop appears and try playing audio again.

**Wine doesn't launch**
Make sure your desktop is running first (Wine needs a display). Run `winecfg` from the terminal inside your desktop.

---

## Advanced Notes

<details>
<summary>Customize GPU flags</summary>

The file `~/.config/linux-gpu.sh` is sourced on every desktop start. You can add or modify Mesa environment variables here. Common tweaks:

```bash
# Force software rendering (debugging)
export GALLIUM_DRIVER=llvmpipe

# Enable Mesa debug output
export MESA_DEBUG=1

# Change OpenGL version override
export MESA_GL_VERSION_OVERRIDE=3.3
```
</details>

<details>
<summary>Running Python scripts in your desktop</summary>

Open a terminal inside your Linux desktop and run:

```bash
python3 your_script.py
```

To install Python packages:

```bash
pip install requests numpy pandas
```
</details>

<details>
<summary>Autostarting the desktop when Termux opens</summary>

Add this to your `~/.bashrc` or `~/.zshrc` in Termux:

```bash
# Uncomment to auto-launch desktop on Termux open
# bash ~/start-linux.sh
```
</details>

<details>
<summary>About the Termux path</summary>

The script dynamically detects your Termux prefix using `$PREFIX` rather than hardcoding `/data/data/com.termux/files/usr`. This means it works on non-standard installs (e.g., Termux on secondary user profiles or custom ROM configurations).
</details>

---

## Contributing

PRs and issues are welcome. If a package name has changed or a DE has a better startup command, please open an issue with your device model and Android version.

---

## License

MIT — use and modify freely.
