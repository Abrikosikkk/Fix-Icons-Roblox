markdown
# fix_iconsroblox

> A small Windows utility that restores broken thumbnails, avatars, and icons in Roblox by resolving `tr.rbxcdn.com` to a working IP address and patching the system `hosts` file.

---

## Table of Contents

- [The Problem](#the-problem)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [What Gets Changed](#what-gets-changed)
- [Troubleshooting](#troubleshooting)
- [Uninstalling / Reverting](#uninstalling--reverting)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## The Problem

Roblox serves all game thumbnails, user avatars, badges, and catalog images from its CDN:
tr.rbxcdn.com

text

In some regions (notably Russia and other countries with network filtering), this domain may resolve to a **blackholed or unreachable IP**. As a result:

- Game icons show as **grey squares** or **blank placeholders**
- User avatars **fail to load** in the friends list and on profiles
- Catalog, store, and inventory **images are missing**
- Some UI elements appear **broken** even though the game itself runs fine

This is **not a bug in Roblox** and **not a problem with your files**. It is a DNS / routing issue between your machine and the Roblox CDN.

---

## How It Works

The script performs three steps:

1. **Checks for administrator privileges.** Modifying the `hosts` file requires elevation.
2. **Resolves a working IP for `tr.rbxcdn.com`** by querying public DNS servers (`9.9.9.9` and `1.1.1.1`) that are typically not affected by regional filtering.
3. **Writes a static entry to the Windows `hosts` file** pinning the domain to the resolved IP, then **flushes the DNS cache** so the change takes effect immediately.

Once the entry is in place, Windows will always connect to a working CDN node for that domain — and your images will start loading again.

---

## Requirements

- **Windows 10 or Windows 11**
- **Python 3.8+** (only if running from source)
- **Administrator privileges** (required to edit `hosts`)
- An internet connection to a DNS resolver that isn't blocked (Quad9 / Cloudflare are used by default)

No third-party Python packages are needed — the script uses only the standard library.

---

## Installation

### Option 1 — Run from source

```bash
git clone https://github.com/<your-username>/fix_iconsroblox.git
cd fix_iconsroblox
python fix_iconsroblox.py
Option 2 — Download the raw script
Download fix_iconsroblox.py from this repository.

Save it anywhere (e.g. Desktop).

Usage
Right-click fix_iconsroblox.py → Run as administrator
(or open an elevated Command Prompt / PowerShell and run python fix_iconsroblox.py)

The script will:

Print environment info (target domain, hosts path, DNS servers)

Resolve the current IP for tr.rbxcdn.com

Patch the hosts file

Flush the DNS cache

Fully close Roblox (including the system tray icon) and relaunch it.

Images, avatars, and thumbnails should now load.

Example output
text
  ┌─────────────────────────────────────────────┐
  │  fix_iconsroblox.py                         │
  │  Roblox CDN Resolver · v1.0                 │
  └─────────────────────────────────────────────┘

  · target  : tr.rbxcdn.com
  · hosts   : C:\Windows\System32\drivers\etc\hosts
  · dns     : 9.9.9.9, 1.1.1.1

  [1/3] Резолвим актуальный IP…
        → запрос через 9.9.9.9
        ✓ ответ: 18.238.x.x

  [2/3] Обновляем системный hosts…
  ✓ hosts пропатчен → 18.238.x.x tr.rbxcdn.com

  [3/3] Сбрасываем кэш…
  ✓ DNS-кэш очищен

  ─────────────────────────────────────────────
  ✓ Готово. Перезапусти Roblox.
  ─────────────────────────────────────────────
What Gets Changed
The script appends one line to:

text
C:\Windows\System32\drivers\etc\hosts
It looks like this:

text
18.238.x.x tr.rbxcdn.com
The script also removes any previous entries it may have added for the same domain, so re-running it is always safe and idempotent.

Nothing else on your system is touched.

Troubleshooting
The script says "Нет прав на запись в hosts"
You did not launch it as administrator. Close the window and re-run it via Run as administrator.

"Не удалось получить IP ни от одного резолвера"
Both 9.9.9.9 and 1.1.1.1 failed to respond. This can happen if:

Your ISP blocks these DNS servers (try a VPN to reach the script's own download)

You are behind a captive portal

Firewall is blocking nslookup

Workaround: manually change your system DNS to 9.9.9.9 or 1.1.1.1 in Network Adapter Settings, then re-run the script.

Images still don't load after running the script
Make sure Roblox was fully restarted — not just minimized. Check Task Manager for any lingering RobloxPlayerBeta.exe processes.

Verify the entry landed in hosts:

text
type C:\Windows\System32\drivers\etc\hosts
Flush DNS manually:

text
ipconfig /flushdns
If it still fails, the resolved IP may have gone stale. Just re-run the script — it will grab a fresh IP.

Antivirus flags the script
Some AV products treat any hosts modification as suspicious. This script is fully open-source — read the code yourself, then whitelist it.

Uninstalling / Reverting
To undo everything the script did:

Open C:\Windows\System32\drivers\etc\hosts in Notepad as administrator.

Delete the line containing tr.rbxcdn.com.

Save the file.

Run ipconfig /flushdns in an elevated Command Prompt.

That's it. No registry keys, no services, no background processes — the script is a one-shot tool.

FAQ
Does this affect my Roblox account or get me banned?
No. It only changes how your computer resolves one image CDN hostname. It does not modify the game, its memory, or communicate with Roblox servers in any unauthorized way.

Will this break other websites?
No. The change is scoped to a single domain, tr.rbxcdn.com.

Do I need to run it every time I open Roblox?
No. The hosts entry is persistent. Re-run the script only if images stop loading again (CDN IPs occasionally rotate).

Why not just use a VPN?
A VPN works too, but it routes all your traffic and often adds latency to gameplay. Patching hosts is more surgical — you only fix the CDN connection while everything else stays on your normal route.

Does it work on macOS or Linux?
The current version targets Windows only. On macOS/Linux the same idea works — /etc/hosts instead of C:\Windows\...\hosts — but you'll need to adapt the script.

Disclaimer
This tool modifies a system file (hosts). It is provided as-is, with no warranty. Use it at your own risk. The author is not affiliated with Roblox Corporation and takes no responsibility for any consequences of using this software.

License
MIT License — see LICENSE for details.
