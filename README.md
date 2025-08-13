# Ender‑3 V3 Plus Language Switcher

A small Python utility to switch the Creality Ender‑3 V3 Plus Creality OS display from Chinese to English over SSH.

Inspired by the works of Cyril Guislain have a look at their work [here](https://github.com/Guilouz)

Made for one of my Friends that was having an issues with a Creality 3D printer they bought.
Thank you Nati, for the opportunity to work on this project 

Please Star the project if you like it, thanks.


## 🖥️ Overview

Some Ender‑3 V3 Plus units ship with a Chinese‑only Creality OS build. This script:

1. Connects to your printer via SSH (requires root access).
2. Backs up the existing `system_config.json`.
3. Modifies the `"user_info.language"` value from `0` → `1`.
4. Pushes the updated JSON back to the printer.
5. Restarts the UI so the change takes effect immediately.

## ⚙️ Prerequisites

- **Python 3.6+**  
- [Paramiko](https://pypi.org/project/paramiko/) (`pip install paramiko`)
- SSH access to your Ender‑3 V3 Plus as **root**  
- Printer must be on the same network (know its IP/hostname)

> **Tested on**  
> – Mainboard: `CR4CU220812S12`  
> – MCU: GD32F303XXX series  
> – SoC: Ingenic X2000E  

## 🚀 Installation
**Note:** 
Before proceeding with this guide, make sure that root access is enabled on your Ender3 V3 Plus 3D printer.
You can find detailed instructions on how to do this on Guislain's Wiki [here](https://guilouz.github.io/Creality-Helper-Script-Wiki/firmwares/install-and-update-rooted-firmware-ender3/#:~:text=config/system_config.json-,Enable%20Root%20Access,-Note)

You would need to use google translate to find your way arround for this step.
In addtion the computer you are running this script on and the 3D printer must be on the same Wi-Fi network.

1. Clone this repo:

   ```bash
      git clone https://github.com/Amha-Endrayes/ender3v3-plus-language-switcher.git
      cd ender3v3-plus-language-switcher
   ```

2. Install dependencies:

   ```bash
   pip install paramiko
   ```

## 💻 Usage

   ```bash
   python set_printer_language.py \
     --host   192.168.1.123 \
     --user   root \
     --password Creality2023
   ```

* `--host`      Printer IP or hostname
* `--user`      SSH username (usually `root`)
* `--password`  SSH password (omit if you use key‑based auth)
* `--port`      SSH port (default `22`)

Example output:

   ```
   → Backing up JSON …
   ✔ Backup created → /usr/data/creality/userdata/config/system_config.json.bak.20250729140530
   → Downloading JSON …
   → Modifying language …
   → Uploading modified JSON …
   → Restarting UI …
    Done! Screen should reload in English.
   ```

## 🔍 What’s inside?

* **`REMOTE_JSON`**
  Path to the settings file on the printer:

  ```text
  /usr/data/creality/userdata/config/system_config.json
  ```
* **Backup**
  A timestamped `.bak.YYYYMMDDHHMMSS` copy is created before editing.
* **Restart UI**
  Kills any running `crealityui` or `creality-launcher` process so it picks up the new language setting.

## 📄 Example `system_config.json`

```json
{
  "device_info": {
    "device_sn":   "YOUR_SERIAL",
    "device_mac":  "YOUR_MAC",
    "model":         1108,
    "model_str":   "F002",
    "bed_length":    300,
    "bed_width":     300,
    "bed_hight":     330,
    "ui_direction":   3,
    "z_direction":    0
  },
  "user_info": {
    "swap_way":        1,
    "deploy_setting":  1,
    "customer":        0,
    "language":        1,   <— `1` = English
    "sound_size":     10,
    "sound_sw":        1,
    "sounde_ffect":    1,
    "light_sw":        1,
    "light_value":   100,
    "wifi_sw":         1,
    "theme_mode":      1,
    "self_test_sw":    0,
    "screensaver":     0,
    "screen_value":   60,
    "full_screen":     0,
    "auto_power_off":  0,
    "enableselftest":  0,
    "time_zone":    "UTC+08:00",
    "server_config":   1,
    "upgrade_remind":  1,
    "server_local":    1,
    "agree_privacy":   1,
    "host_name":   "Ender-3 V3 Plus-A9BF",
    "data_collect":    0,
    "irlight":       -1
  }
}
```

## 🐞 Troubleshooting

* **SSH connection fails**

  * Verify printer’s IP, port, credentials.
  * Ensure “Root Mode” is enabled in the Creality UI.
* **Backup or upload errors**

  * Check available disk space and permissions on the printer.
* **UI doesn’t restart**

  * Manually reboot the printer.

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b my-feature`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin my-feature`)
5. Open a Pull Request

## 📄 License

[MIT](LICENSE) © [Amha Endrayes](https://github.com/Amha-Endrayes)


